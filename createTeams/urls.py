from django.urls import path
from . import views
app_name='createTeams'

urlpatterns=[
    path('create_new_team/',views.create_new_team, name="new_team"),
    path('create_team/<int:par_id>', views.create_team, name="create_team"),
    path('display_teams/',views.display_teams, name="display_teams"),
    path('edit_team/<int:org_id>', views.edit_team, name="edit_team"),
    path('view_team/<int:team_id>', views.view_team,name = 'view_team'),
    path('change_role/<int:org_id>', views.change_role,name = 'change_role'),
    path('dismiss_admin/<int:org_id>', views.dismiss_admin,name = 'dismiss_admin'),
    path('leave_team/<int:org_id>', views.leave_team,name = 'leave_team'),
    path('delete_team/<int:org_id>', views.delete_team,name = 'delete_team'),
    path('add_members/<int:org_id>', views.add_members,name = 'add_members'),
    path('send_invite/<int:org_id>', views.send_invite,name = 'send_invite'),
]