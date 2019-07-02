from django.urls import path,include
from .views import *

urlpatterns = [
    path('',HomePage.as_view(),name='home'),
    path('login/',LoginView.as_view(),name='login'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('logout/',LogOut,name='logout'),
    path('seasons/',Seasons.as_view(),name='seasons'),
    path('season/points/',Points.as_view(),name='points_page'),
    path('seasons/<str:season>/',Seasons.as_view(),name='seasons'),
    path('seasons/<str:season>/match/<int:match_id>/',Matches_view.as_view(),name='matches'),

    path('season/<str:season>/points/',Points.as_view(),name='points'),
    path('teams/',Teams.as_view(),name='teams_page'),
    path('teams/<str:season>/',Teams.as_view(),name='teams'),
    path('teams/<str:season>/<str:teamName>/',Teams.as_view(),name='team_details_init'),
    path('teams/<str:season>/<str:teamName>/<int:matchYear>/',Teams.as_view(),name='team_details'),
]