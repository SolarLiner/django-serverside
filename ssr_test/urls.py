from django.urls import path

from ssr_test.views import IndexView, PlayerView

urlpatterns = [
    path("", IndexView.as_view()),
    path("player/<pk>", PlayerView.as_view())
]
