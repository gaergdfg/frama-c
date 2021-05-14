from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login),

    path('new_directory/', views.new_directory),
    path('new_file/', views.new_file),
    path('remove_directory/', views.remove_directory),
    path('remove_file/', views.remove_file),
    path('file/', views.get_file),
    path('run_file/', views.run_file),
    path('set_prover/', views.set_prover),
    path('set_vcs/', views.set_vcs),
]
