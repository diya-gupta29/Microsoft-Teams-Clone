from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Organization,Membershiplevel, Team_Messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
import uuid
import json

'''
View being called to display all the teams, user is a part of.
'''
def display_teams(request):
    if not request.user.is_authenticated:
        return redirect('/')
    memberships = Membershiplevel.objects.filter(user__username = request.user.username)
    teams = []
    for membership in memberships:
        org_id = membership.organization.id
        org = Organization.objects.get(pk=org_id)
        if org.parent_org_id is None:
            teams.append(org)
    return render(request,'createTeams/display_teams.html',{'teams':teams,'username':request.user.username})


'''
Function being called by other views to retrieve all the channels( child organizations) for the team.
As sub-channels may also exist for other channels,
so we are calling recursive function to retrieve all the channels
''' 
def retrieve_child_org(parent,child):
    count = Organization.objects.filter(parent_org = parent).count()
    if count!=0:
        child_org = Organization.objects.filter(parent_org = parent)
        for i in child_org:
            retrieve_child_org(i.id,child)
            child.append(i.id)


'''
View being called for creating the channel(sub-organisation of Team).
It checks if the channel with the same name already exists,
if exists, then it gives the warning "Channel cannot be created"
else it successfully creates the new channel.
'''
def create_team(request,par_id) :
    if request.user.is_authenticated:
        warning = ''
        if request.method == 'POST':
            channel_name = request.POST['team_name']
            members = request.POST.getlist('checks')
            print(members)
            user=request.user
            description = request.POST['description']
            if Organization.objects.filter(name = channel_name,parent_org__id = par_id).exists():
                warning = "Channel with this name already exists"
            else: 
                channel = Organization.objects.create(name = channel_name,parent_org_id = par_id,description=description)
                members = User.objects.filter(pk__in = members)
                Membershiplevel.create_team(members,channel,par_id,request.user.id)
                warning = "Channel created"
                return redirect(reverse("createTeams:view_team",kwargs={'team_id':channel.id}))
        memberships = Membershiplevel.objects.filter(organization__id = par_id)
        return render(request,'createTeams/create_channel.html',{'memberships':memberships,'warning':warning,'user':request.user},)
    else:
        return redirect('/')


'''
View being called for creating the new team.
It checks if the team with the same name already exists, it gives warning "Team cannot be created"
else it successfully creates the new team.
'''
def create_new_team(request):
    if request.user.is_authenticated:
        warning = ''
        if request.method == 'POST':
            team_name = request.POST['team_name']
            members = request.POST.getlist('checks')
            user=request.user
            description = request.POST['description']
            print(members)
            if Organization.objects.filter(name = team_name,parent_org__id = None).exists():
                warning = "Team with this name already exists"
            else:
                team = Organization.objects.create(name = team_name,parent_org_id = None,description=description)
                members = User.objects.filter(pk__in = members)
                Membershiplevel.create_team(members,team,None,request.user.id)
                warning = "team created"
                return redirect(reverse("createTeams:view_team",kwargs={'team_id':team.id}))
        memberships = User.objects.all()
        print(memberships)
        return render(request,'createTeams/create_team.html',{'memberships':memberships,'warning':warning,'user':request.user},)
    else:
        return redirect('/')


'''
View used to change the status of members from participant to admin(owner) 
'''
def change_role(request,org_id):
    if request.user.is_authenticated:
        warning = ''
        role = Membershiplevel.objects.get(organization__id = org_id , user_id = request.user.id).role
        if request.method == 'POST':
            members = request.POST.getlist('checks')
            members = User.objects.filter(pk__in = members)
            Membershiplevel.change_role(members,org_id)
            warning = "Role changed to admin successfully!!"
        memberships = Membershiplevel.objects.filter(organization__id = org_id, role = 2)
        return render(request,'createTeams/status_to_admin.html',{'memberships':memberships,'warning':warning,'user':request.user},)
    else:
        return redirect('/')


'''
View used to change the status of members from admin(owner) to participant.
'''
def dismiss_admin(request,org_id):
    if request.user.is_authenticated:
        warning = ''
        admin = Membershiplevel.objects.filter(organization__id = org_id,role = 1).count()
        if request.method == 'POST':
            members = request.POST.getlist('checks')
            count = 0
            for member in members:
                count+=1
            if count==admin :
                warning = "Sorry, we can't change the status to participant!!"
            else:
                members = User.objects.filter(pk__in = members)
                Membershiplevel.change_role_participant(members,org_id)
                warning = "Role changed to participant successfully!!"

        memberships = Membershiplevel.objects.filter(organization__id = org_id, role = 1)
        return render(request,'createTeams/status_to_participant.html',{'memberships':memberships,'warning':warning,'user':request.user},)
    else:
        return redirect('/')


'''
View being called for leaving the team.
If the user leaving the team is admin of the team or any of its parent organizations,
then on leaving, some other person should be made as admin
if count of admins(owners) for the team equals 1(i.e. the user himself)
if count of admins(owners) for the team > 1, then user could easily leave the team
if user is participant and if he is the only person left in the team, then on leaving,
team and all its child organizations(channels) are deleted.
else the user could leave the team easily
'''
def leave_team(request,org_id):
    if request.method == 'POST':
        team = Organization.objects.get(pk=org_id)
        if request.POST.get('confirmation')=='clicked_yes':
            team = Organization.objects.get(pk=org_id)
            warning=''     
            flag = False
            par_id = Organization.objects.get(pk=org_id).parent_org_id
            org_name = Organization.objects.get(pk=org_id).name
            while par_id is not None:
                role = Membershiplevel.objects.get(user_id = request.user.id, organization__id = par_id).role
                if role == 1:
                    flag = True
                    break
                par_id = Organization.objects.get(pk=par_id).parent_org
            if flag == True:
                warning = "Sorry, You can't leave the team!!"
            else:
                # retrieving all the channels of team and storing their ids in child[]
                child = []
                retrieve_child_org(org_id,child)
                child.append(org_id)

                for org in child:
                    # checking whether the user is a part of any of the channels
                    if Membershiplevel.objects.filter(organization__id=org,user_id=request.user.id).exists():

                        role = Membershiplevel.objects.get(organization__id = org , user_id = request.user.id).role
                        curr_user = User.objects.get(pk = request.user.id)
                        total_members = Membershiplevel.objects.filter(organization__id = org).count()
                        if total_members>1:
                            # if the person is admin
                            if role == 1:
                                admin_count = Membershiplevel.objects.filter(organization__id = org,role = 1).count()
                                # if count of admin >1 then the person could easily leave the team
                                if admin_count > 1:
                                    Membershiplevel.leave_team(curr_user,org)
                                    warning = "Left the team successfully!!"
                                else:  
                                    # if count of admin equals 1, then before leaving,
                                    # some random person should be made as admin of the team
                                    members = Membershiplevel.objects.filter(organization__id = org)
                                    # accessing the random member of team to be made as admin. 
                                    user = Membershiplevel.access_new_admin(members,org,request.user.id)
                                    new_admin = User.objects.filter(pk=user)
                                    # changing the status of randomly selected person as admin
                                    Membershiplevel.change_role(new_admin,org)
                                    # current user(also the previous admin or owner) leaving the team
                                    Membershiplevel.leave_team(curr_user,org)
                                    warning = "Left the team successfully"
                            else:
                                # if the person is participant
                                Membershiplevel.leave_team(curr_user,org)
                                warning = "Left the team successfully"
                        else: 
                            '''
                            if the only person is left in the team, then on leaving the team,
                            current team will also be deleted
                            '''
                            Membershiplevel.leave_team(curr_user,org)
                            Organization.delete_org(org)
                            warning = "Left the team successfully!!"
            return render(request,'createTeams/leave_team.html',{'warning':warning,'user':request.user,'team':team},)
        else:
            return redirect(reverse("createTeams:view_team",kwargs={'team_id':org_id}))
        return redirect('/createTeams/display_teams/')
    team = Organization.objects.get(pk=org_id)
    return render(request,'createTeams/leave_team.html',{'team':team})


'''
View being called from 'edit_team' 
to remove the person from team by taking all the conditions into account
Here variable 'role' refers to admin or participant status
role == 1 refers to admin status
role == 2 refers to participant status
'''
def remove_team(memberId,org_id):     
    flag = False
    par_id = Organization.objects.get(pk=org_id).parent_org_id
    while par_id is not None:
        role = Membershiplevel.objects.get(user_id = memberId, organization__id = par_id).role
        if role == 1:
            flag = True
            break
        par_id = Organization.objects.get(pk=par_id).parent_org
    if flag == False:
        child = []
        retrieve_child_org(org_id,child)
        child.append(org_id)

        for org in child:
            if Membershiplevel.objects.filter(organization__id=org,user_id=memberId).exists():
                role = Membershiplevel.objects.get(organization__id = org , user_id = memberId).role
                p = User.objects.get(pk = memberId)
                total_members = Membershiplevel.objects.filter(organization__id = org).count()
                if total_members>1:
                    if role == 1:
                        admin_count = Membershiplevel.objects.filter(organization__id = org,role = 1).count()
                        if admin_count > 1:
                            Membershiplevel.leave_team(p,org)
                        else:  
                            # if count of admin is one then before leaving some random person should be made as admin
                            members = Membershiplevel.objects.filter(organization__id = org)
                            # accessing the member of team which was first added to team. 
                            user = Membershiplevel.access_new_admin(members,org,memberId)
                            q = User.objects.filter(pk=user)
                            # making random person admin
                            Membershiplevel.change_role(q,org)
                            # admin leaving the team
                            Membershiplevel.leave_team(p,org)
                    else:
                        # if the person is participant
                        Membershiplevel.leave_team(p,org)
                else: 
                    Membershiplevel.leave_team(p,org)
                    Organization.delete_org(org)


'''
View called for editing the team. 
Team Name and Description can also be changed using this.
All the users selected will be added to the team.
Non selected users which were part of the team before will be removed from the team
'''    
def edit_team(request, org_id) :
    if request.user.is_authenticated:
        warning = ''
       
        if request.method == 'POST':
            team_name = request.POST['team_name']
            description = request.POST['description']
            new_members = request.POST.getlist('checks')

            old_team_name = Organization.objects.get(pk=org_id).name
            par_id = Organization.objects.get(pk = org_id).parent_org_id

            Organization.update_team(old_team_name,team_name,description,par_id)

            ex_members = Membershiplevel.objects.filter(organization__id = org_id)
            ids = []
            for ex_member in ex_members:
                ids.append(ex_member.user_id)
            ex_members = User.objects.filter(pk__in = ids)

            new_members = User.objects.filter(pk__in = new_members)
            for member in ex_members:
                if member not in new_members:
                    remove_team(member.id,org_id) 

            user = request.user
            org  = Organization.objects.get(pk = org_id)           
            Membershiplevel.edit_team(ex_members,new_members,org_id,par_id,request.user.id)
            warning = "Successfully edited!!"
        par_id = Organization.objects.get(pk = org_id).parent_org_id
        if par_id is None:
            memberships = User.objects.all()
        else:
            memberships = Membershiplevel.objects.filter(organization__id=par_id)
        organisation  = Organization.objects.get(pk = org_id)    
        return render(request, 'createTeams/edit_team.html',{'memberships': memberships,'org': organisation, 'warning':warning, 'user': request.user},)
    else:
        return redirect('/')


'''
View used for displaying the details of the team
along with its all sub organizations
'''
def view_team(request, team_id):
    if request.user.is_authenticated:
        user = request.user
        org  = Organization.objects.get(pk = team_id)
        if not org:
            return  redirect('/createTeams/display_teams')
        all_channels = Organization.get_all_children(org)
        user_part_of_channels=[]
        for channel in all_channels:
            if Membershiplevel.objects.filter(organization__id=channel.id,user_id=request.user.id).exists():
                user_part_of_channels.append(channel)
        members = Membershiplevel.objects.filter(organization__id = org.id)
        user_role = Membershiplevel.objects.get(organization__id = org.id,user_id = request.user.id).role
        return render(request, 'createTeams/team_page.html',{"org": org, "channels": user_part_of_channels, "members": members,'user':request.user,'user_role':user_role})
    else:
        return redirect('/')


'''
View for deleting the team or organisation.
If sub-organizations(channels) exist for the team,
then on deletion all the sub-organizations of the team along with the team are deleted.
'''
def delete_team(request,org_id):
    if request.method == 'POST':
        team = Organization.objects.get(pk=org_id)
        if request.POST.get('confirmation')=='clicked_yes':
            team = Organization.objects.get(pk=org_id)
            channels = []
            retrieve_child_org(org_id,channels)
            channels.append(org_id)
            for team in channels:
                Organization.delete_org(team)
        else:
            return redirect(reverse("createTeams:view_team",kwargs={'team_id':org_id}))
        return redirect('/createTeams/display_teams/')
    team = Organization.objects.get(pk=org_id)
    return render(request,'createTeams/delete_team.html',{'team':team})


'''
View for sending invite to team members through email for video call
when any member of the team starts the video call.
'''
def send_invite(request,org_id):
    if request.user.is_authenticated:
        recipient_list = []
        members = Membershiplevel.objects.filter(organization__id = org_id)
        for member in members:
            if member.user_id == request.user.id:
                continue
            else:
                receipient = User.objects.get(pk = member.user_id)
                recipient_list.append(receipient.email)
        room_id = uuid.uuid4()
        base_url =  "{0}://{1}/{2}/{3}/{4}".format(request.scheme, request.get_host(),'video_call', org_id,room_id)
        subject = 'Invite to join video conference'
        message = f'Hi {request.user.username}, invited you to join a video call. Link for the meet is {base_url}'
        email_from = settings.EMAIL_HOST_USER
        send_mail( subject, message, email_from, recipient_list )
        return redirect(reverse("video_call:main_view",kwargs={'team_id':org_id, 'room_id':room_id}))
    else:
        return redirect('/')

'''
View for adding members to the team or channel.
If no parent organization of the team exists, 
then all the users in the database are provided for selection.
else members existing in the "parent organization" of the team(channel) are provided in the checklist
'''
def add_members(request, org_id):
    warning = ''
    if request.method == 'POST':
        new_members = request.POST.getlist('checks')
        par_id = Organization.objects.get(pk = org_id).parent_org_id
        ex_members = Membershiplevel.objects.filter(organization__id = org_id)
        ids = []
        for ex_member in ex_members:
            ids.append(ex_member.user_id)
        ex_members = User.objects.filter(pk__in = ids)
        new_members = User.objects.filter(pk__in = new_members)
        user = request.user
        org  = Organization.objects.get(pk = org_id)
        count = Membershiplevel.edit_team(ex_members,new_members,org_id,par_id,request.user.id)
        warning = "Members added successfully!!"
    org = Organization.objects.filter(pk = org_id)[0]
    if org.parent_org_id is None:
        memberships = User.objects.all()
    else:
        memberships = Membershiplevel.objects.filter(org__id = org.parent_org_id)
    return render(request,'createTeams/add_members.html',{'memberships':memberships,'warning':warning,'user':request.user,'org':org},)


