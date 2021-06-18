from django.urls import path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),

    path('', views.index, name='index'),
    path('login/', views.login),
    path('logout/', views.logout),

    path('new_directory/', views.new_directory),
    path('new_file/', views.new_file),
    path('remove_directory/', views.remove_directory),
    path('remove_file/', views.remove_file),

    path('user_directories/', views.get_user_directories),
    path('user_files/', views.get_user_files),
    path('file/', views.get_file),

    path('run_file/', views.run_file),
    path('set_prover/', views.set_prover),
    path('set_vcs/', views.set_vcs),
]
