from django.urls import path
from .views import *
app_name = 'video_call'
urlpatterns = [
    path('<int:team_id>/<uuid:room_id>',main_view,name="main_view"),
    path('invite_people/',invite_people,name="invite_people")
]