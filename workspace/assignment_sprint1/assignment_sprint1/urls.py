"""assignment_sprint1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from sprint1 import views
from django.conf import settings
from django.conf.urls.static import static


navBar = '<h5><a href="/login/">Log in</a><br /><a href="/signup/">Register</a><a href="/modify/">Modify Account</a></h5>'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/',}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^location/$', views.locationfeed, name='locationfeed'),
    url(r'^location/individual/(?P<location_id>[0-9]+)/$', views.locations, name='locations'),
    url(r'^modify/$', views.modify, name='modify'),
    url(r'^modify/edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^modify/password/$', views.password, name='password'),
    url(r'^email/$', views.email, name='email'),
<<<<<<< HEAD
    url(r'^modify/del_user/$', views.del_user, name='del_user'),
    url(r'^imageform/$', views.imageform, name='imageform'),
=======
    url(r'^bugs/$', views.bugs, name='bugs'),
    url(r'^modify/del_user/$', views.del_user, name='del_user')
>>>>>>> master
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    