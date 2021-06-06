from django.urls import path

from vote import views

urlpatterns = [
    path('', views.votation_list_view, name="votation-list"),
    path('vote/<uuid:pk>/', views.votation_detail, name="votation-detail"),
    path('vote/<uuid:pk>/vote/', views.vote_action, name="vote"),
]
