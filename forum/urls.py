from django.urls import path
from . import views

urlpatterns = [
    # Cesta pre zobrazenie zoznamu fór
    path('', views.forums, name='forum'),  
    # Cesta pre pridanie nového fóra
    path('addInForum/', views.addInForum, name='addInForum'),  
    # Cesta pre pridanie diskusie do konkrétneho fóra
    path('<int:forum_id>/addInDiscussion/', views.addInDiscussion, name='addInDiscussion'),  
]


