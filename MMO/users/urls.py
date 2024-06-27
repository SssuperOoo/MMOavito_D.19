from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from users import views
from users.forms import RegisterUserForm


app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),  # http://127.0.0.1:8000
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUserCreateView.as_view(), name='register'),
    path('profile/', views.ProfileUserUpdateView.as_view(), name='profile'),
    path('password-reset/',
         PasswordResetView.as_view(template_name = "users/password_reset_form.html",
                                   email_template_name="users/password_reset_email.html",
                                   success_url=reverse_lazy("users:password_reset_done")),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                          success_url=reverse_lazy("users:password_reset_complete")),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),
    path('activate/<str:code>/', views.activate_account, name='activate_account'),

]