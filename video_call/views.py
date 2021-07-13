from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

'''
View being called to let the user join video conference
here "room_id" refers to "team_id"
'''
def main_view(request,team_id,room_id):
    base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    if request.user.is_authenticated:   
        room_id = room_id
        team_id = team_id
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        context = {'room_id':room_id,'user_id':user_id,'user':user,'base_url':base_url,'team_id':team_id} 
        return render(request,'video_call/final_video.html',context=context)
    else:
        return redirect('/')

'''
View being called to send invitation for video call to input "email id"
'''
@csrf_exempt
def invite_people(request):
    recipient_list = []
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        base_url = request.POST.get('base_url')
        recipient_list.append(email_id)
        subject = 'Invite to join video conference'
        message = f'Hi {request.user.username}, invited you to join a video call. Link for the meet is {base_url}'
        email_from = settings.EMAIL_HOST_USER
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponse("success")
    else:
        return HttpResponse("Invite not sent!!")
    
    return redirect('/',{'users':users})