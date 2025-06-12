from django.urls import path
from . import views

urlpatterns = [
    path('', views.forums, name='forum'),  
    path('addInForum/', views.addInForum, name='addInForum'),  
    path('<int:forum_id>/addInDiscussion/', views.addInDiscussion, name='addInDiscussion'),  
]


