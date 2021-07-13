from django.conf.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/createTeams/view_team/(?P<room_id>[0-9]+)/$',consumers.ChatConsumer.as_asgi()),
]