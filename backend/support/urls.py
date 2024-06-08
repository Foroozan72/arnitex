from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter()
router.register(r'ticket-unit', views.TicketUnitViewSet, basename='ticket-unit')
router.register(r'create-ticket', views.CreateTicketViewSet, basename='create-ticket')
router.register(r'ticket', views.TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls))
]