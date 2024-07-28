from rest_framework import viewsets
from .serializers import (
    PacientSerializer, ProfessionalSerializer, ProcedureSerializer,
    RoomSerializer, AppointmentSerializer
    )
from .models import (
    Pacient, Professional, Procedure, Room, Appointment
    )
from rest_framework.permissions import IsAuthenticated

class PacientsViewSet(viewsets.ModelViewSet):
    serializer_class = PacientSerializer
    queryset = Pacient.objects.all()
    permission_classes = [IsAuthenticated]

class ProfessionalViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessionalSerializer
    queryset = Professional.objects.all()
    permission_classes = [IsAuthenticated]

class ProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = ProcedureSerializer
    queryset = Procedure.objects.all()
    permission_classes = [IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated]

class AppoitmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]