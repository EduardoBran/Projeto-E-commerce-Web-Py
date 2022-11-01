"""loja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from perfil.views import BasePerfil

urlpatterns = [
    path('', include('produto.urls')),

    # necessário para recuperar a senha
    path('', include('django.contrib.auth.urls')),
    path('accounts/login/', BasePerfil.as_view(), name='entrar'),

    path('perfil/', include('perfil.urls')),
    path('pedido/', include('pedido.urls')),
    path('suporte/', include('suporte.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "loja.views.page_error_404"
handler500 = "loja.views.page_error_500"
handler503 = "loja.views.page_error_503"

admin.site.site_header = 'Unique Store'
admin.site.site_title = 'Unique Store'
admin.site.index_title = 'Sistema de Cadastro Unique'
