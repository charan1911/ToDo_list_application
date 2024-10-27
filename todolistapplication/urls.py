from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login-page"),
    path('logoutpage/', views.logoutpage, name="logout-page"),
    path('registerpage/', views.register, name="register-page"),
    path('todolistpage/', views.todolists, name="todolist-page"),
    path("deletetask/<str:name>/", views.deletetask, name="deletetask"),
    path("taskmark/<str:name>/", views.taskmark, name="taskmark"),
    
]