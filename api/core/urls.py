from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PacientsViewSet, ProfessionalViewSet, ProcedureViewSet, RoomViewSet, AppoitmentViewSet
)

router = DefaultRouter()
router.register(r'pacients', PacientsViewSet, basename='pacients')
router.register(r'professional', ProfessionalViewSet, basename='professional')
router.register(r'procedure', ProcedureViewSet, basename='procedure')
router.register(r'room', RoomViewSet, basename='room')
router.register(r'appointment', AppoitmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
]
