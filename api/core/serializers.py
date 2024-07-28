from rest_framework import serializers
from .models import (
    Pacient, Professional, Procedure, Room, Appointment
    )

class PacientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacient
        fields = [
            "id", 
            "name", 
            "email", 
            "document"
            ]

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = [
            "id",
            "name",
            "email",
            "document",
            "specialty",
            ]

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "name",
        ]
        model = Procedure

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "name",
        ]
        model = Room

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "paciente",
            "procedure",
            "professional",
            "room",
            "status",
            "date"
        ]
        model = Appointment