from django.urls import path
from . import views
from .views import *
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('users/', views.getUsers),
    path('users/create/', RegisterView.as_view()),
    path('users/<str:pk>/', views.getUser),
    path('users/<str:pk>/update/', views.UpdateView.as_view()),
    path('users/<str:pk>/updateActive/', views.UpdateUser.as_view()),
    path('users/<str:pk>/delete/', views.deleteUser),


    path('projet/', views.getProjets),
    path('projet/create/', views.createProjet),
    path('projet/<str:pk>/', views.getProjet),
    path('projet/<int:pk>/update/', views.UpdateProjetView.as_view()),
    path('projet/<int:pk>/updateStatut/', views.projetUpdateStatut.as_view()),
    path('projet/<str:pk>/delete/', views.deleteProjet),



    path('departement/', views.getDepartements),
    path('departement/<int:pk>/update/', views.departementUpdate.as_view()),
    path('document/<int:pk>/', views.getDocuments),
    path('document/<int:pk>/update/', views.documentUpdate.as_view()),

    path('taches/create/', views.createTache),
    path('taches/<str:pk>/', views.getTaches),
    path('tache/<int:pk>/update/', views.TacheUpdate.as_view()),
    path('tache/<str:pk>/delete/', views.deleteTache),






   

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
