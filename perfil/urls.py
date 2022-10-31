
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls.base import reverse_lazy

from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.BasePerfil.as_view(), name='entrar'),
    path('cadastrar/', views.Criar.as_view(), name='criar'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('perfil:password_reset_done')),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('perfil:login')),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]
