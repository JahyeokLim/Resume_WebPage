from django.urls import path

from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('inbox/<int:pk>/', views.inbox_detail_view, name='inbox_detail'),
]
