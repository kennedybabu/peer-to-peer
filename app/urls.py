from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('login_user/', views.login_user, name = 'login'),
    path('logout/', views.logoutUser, name='logout' ),
    path('new/project', views.new_project, name='new_project'),
    path('register_user', views.register_user, name='register_user'),
    path('view_profile/<int:id>', views.view_profile, name='view_profile'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)