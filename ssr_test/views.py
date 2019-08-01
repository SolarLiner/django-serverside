import os

# Create your views here.
from serverside.views import ListNodeView, DetailNodeView
from ssr_test.models import Player

FILE_DIRNAME = os.path.dirname(__file__)


class IndexView(ListNodeView):
    model = Player
    queryset = Player.objects.order_by("-created_at").all()
    filename = os.path.join(FILE_DIRNAME, "node/index.js")


class PlayerView(DetailNodeView):
    model = Player
    queryset = Player.objects.all()
    filename = os.path.join(FILE_DIRNAME, "node/player.js")
