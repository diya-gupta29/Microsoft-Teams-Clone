from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, ChangePasswordForm, PwdResetForm, PwdResetConfirmForm
app_name = 'auth'

urlpatterns = [
    path('registration/',views.registration_view.as_view(),name='reg'),
    path('',auth_views.LoginView.as_view(template_name='authentication/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='auth:login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='authentication/change_pwd.html',form_class = ChangePasswordForm, success_url = '/pwdchdone/'),name='pwdchange'),
    path('pwdchdone/',auth_views.PasswordChangeView.as_view(template_name='authentication/pwdchdone.html'),name='pwdchdone'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='authentication/pwd_reset.html',email_template_name = 'authentication/password_reset_email.html', success_url = reverse_lazy('auth:password_reset_done'), form_class = PwdResetForm), name = 'password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='authentication/pwd_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='authentication/pwd_reset_confirm.html',success_url = reverse_lazy('auth:password_reset_complete'), form_class=PwdResetConfirmForm), name = 'password_reset_confirm'),
    path('reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='authentication/pwd_reset_complete.html'), name = 'password_reset_complete'),
    
]
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)