from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('voting/', views.voting, name='voting'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cast_vote/', views.cast_vote_view, name='cast_vote'),
    path('results/', views.get_results_view, name='results'),
    path('help/', views.help_view, name='help'),
]