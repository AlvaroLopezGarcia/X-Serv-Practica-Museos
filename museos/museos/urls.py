"""museos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout, login
from django.views.static import serve

urlpatterns = [
    url(r'^$','myproject.views.barra'),
    url(r'^museos/$','myproject.views.museos'),
    url(r'^museos/(\d+)$','myproject.views.museo'),
    url(r'^usuario/(\d+)/xml$','myproject.views.usuario_xml'),
    url(r'^usuario/(\d+)$','myproject.views.usuario'),
    url(r'^css$','myproject.views.css'),
    url(r'^static(.+)$',serve,{'document_root':'templates/basic'}),
    url(r'^update/$','myproject.views.update'),
    url(r'^logout', logout, {'next_page': '/'}),
    url(r'^login', 'myproject.views.Login'),
    url(r'^about/$','myproject.views.about'),
    url(r'^admin/', include(admin.site.urls)),
]
