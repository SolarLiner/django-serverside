import json
import subprocess
from datetime import datetime
from subprocess import PIPE

import sys
from django.conf import settings
from django.db.models import QuerySet, Model
from django.http import HttpResponse
from django.template.response import ContentNotRenderedError


class SimpleNodeResponse(HttpResponse):
    """Response object for rendering transferred to a Node process. Modelled after the TemplateResponse object."""
    timeout = None
    render_attributes = ["context_data", "_post_render_callbacks"]

    def __init__(self, filename, context=None, content_type=None, status=None, charset=None):
        self.js_filename = filename
        self.context_data = context
        self._post_render_callbacks = []
        self._request = None

        super().__init__('', content_type, status, charset=charset)
        self._is_rendered = False

    def __getstate__(self):
        obj_dict = self.__dict__.copy()
        if not self._is_rendered:
            raise ContentNotRenderedError("The response content must be rendered before it can be pickled.")
        for attr in self.render_attributes:
            if attr in obj_dict:
                del obj_dict[attr]

        return obj_dict

    @staticmethod
    def resolve_context(context):
        return context

    def get_process_args(self):
        node_exe = getattr(settings, "NODE_PATH", "node")
        filename = self.js_filename

        return [node_exe, filename]

    def get_timeout(self):
        return self.timeout

    @property
    def is_rendered(self):
        return self._is_rendered

    @property
    def content(self):
        if not self._is_rendered:
            raise ContentNotRenderedError("The response content must be rendered before it can be accessed.")
        return super().content

    @content.setter
    def content(self, value):
        HttpResponse.content.fset(self, value)
        self._is_rendered = True

    @property
    def rendered_content(self):
        context = self.resolve_context(self.context_data)
        ctx_data = json.dumps(context, ensure_ascii=True, default=serialize_django_obj).encode("ascii")
        ctx_data_len = str(len(ctx_data))
        args = self.get_process_args()
        process = subprocess.run(
            args,
            input=ctx_data,
            capture_output=True,
            timeout=self.get_timeout(),
            env={'NODE_CTX_LEN': ctx_data_len}
        )
        sys.stdout.write(process.stderr.decode())
        if process.returncode != 0:
            raise Exception("Node.js process did not return successfully")
        return process.stdout

    def add_post_render_callback(self, callback):
        if self._is_rendered:
            callback(self)
        else:
            self._post_render_callbacks.append(callback)

    def render(self):
        ret_val = self
        if not self._is_rendered:
            self.content = self.rendered_content
            for cb in self._post_render_callbacks:
                new_ret_val = cb(ret_val)
                if new_ret_val is not None:
                    ret_val = new_ret_val
        return ret_val


class NodeResponse(SimpleNodeResponse):
    render_attributes = SimpleNodeResponse.render_attributes + ["_request"]

    def __init__(self, request, filename, context=None, content_type=None, status=None, charset=None):
        super().__init__(filename, context, content_type, status, charset)
        self._request = request

    @property
    def request(self):
        return self._request


def serialize_django_obj(obj, level=0):
    if isinstance(obj, QuerySet):
        return list(obj.values())
    elif isinstance(obj, Model):
        if level > 2:
            fields = [f.name for f in obj._meta.get_fields() if not f.is_relation]
            return {k: getattr(obj, k) for k in fields}
        return serialize_model(obj, level)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, (dict, list, tuple, str, int, float, bool)) or (obj is None):
        return obj
    return str(obj)


def serialize_model(inst: Model, level=0):
    obj = dict()
    for field in inst._meta.get_fields():
        value = getattr(inst, field.name)
        if field.many_to_many or field.many_to_one or field.one_to_many:
            if isinstance(value, Model):
                obj[field.name] = serialize_model(value, level=level + 1)
            elif hasattr(value, "all"):
                obj[field.name] = [serialize_django_obj(m, level=level + 1) for m in value.all()]
            else:
                obj[field.name] = serialize_django_obj(value, level=level + 1)
        else:
            obj[field.name] = serialize_django_obj(value, level=level + 1)
    return obj
