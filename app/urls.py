from django.urls import path
from . import views

tea_list = views.TeaViewSet.as_view({'get': 'list', 'post': 'create'})
tea_detail = views.TeaViewSet.as_view({'put': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('auth/register/', views.register),
    path('auth/me/', views.current_user),
    path('teas/', tea_list),
    path('teas/<int:pk>/', tea_detail),
]
