from django.views.generic.base import ContextMixin, View
from django.views.generic.dates import BaseArchiveIndexView, BaseYearArchiveView, BaseMonthArchiveView, \
    BaseWeekArchiveView, BaseDayArchiveView, BaseTodayArchiveView, \
    BaseDateDetailView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import FormMixin, ProcessFormView, BaseCreateView, BaseUpdateView, \
    BaseDeleteView
from django.views.generic.list import BaseListView

from serverside.response import NodeResponse


class NodeResponseMixin:
    """Mixin class for integrating a Node.js based response, intended for class-based views."""
    filename = None
    response_class = NodeResponse
    content_type = None

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        return self.response_class(
            request=self.request,
            filename=self.get_filename(),
            context=context
        )

    def get_filename(self):
        return self.filename


class NodeView(NodeResponseMixin, ContextMixin, View):
    """Superclass to all class-based, Node.js based views."""

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ListNodeView(NodeResponseMixin, BaseListView):
    """Convenience class for listing views."""
    pass


class DetailNodeView(NodeResponseMixin, BaseDetailView):
    pass


class BaseFormNodeView(FormMixin, ProcessFormView):
    pass


class FormNodeView(NodeResponseMixin, BaseFormNodeView):
    pass


class CreateNodeView(NodeResponseMixin, BaseCreateView):
    pass


class UpdateNodeView(NodeResponseMixin, BaseUpdateView):
    pass


class DeleteNodeView(NodeResponseMixin, BaseDeleteView):
    pass


class ArchiveIndexNodeView(NodeResponseMixin, BaseArchiveIndexView):
    pass


class YearArchiveNodeView(NodeResponseMixin, BaseYearArchiveView):
    pass


class MonthArchiveNodeView(NodeResponseMixin, BaseMonthArchiveView):
    pass


class WeekArchiveNodeView(NodeResponseMixin, BaseWeekArchiveView):
    pass


class DayArchiveNodeView(NodeResponseMixin, BaseDayArchiveView):
    pass


class TodayArchiveNodeView(NodeResponseMixin, BaseTodayArchiveView):
    pass


class DateDetailNodeView(NodeResponseMixin, BaseDateDetailView):
    pass
