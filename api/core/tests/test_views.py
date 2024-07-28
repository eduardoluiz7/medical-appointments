from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from core.models import Pacient, Professional, Procedure, Room, Appointment

class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class PacientTests(BaseTestCase):
    def test_list_pacients(self):
        url = reverse('pacients-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_pacient(self):
        url = reverse('pacients-list')
        data = {'name': 'John Doe', 'email': 'john@example.com', 'document': '123456789'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_pacient(self):
        pacient = Pacient.objects.create(name='John Doe', email='john@example.com', document='123456789')
        url = reverse('pacients-detail', args=[pacient.id])
        data = {'name': 'John Smith', 'email': 'johnsmith@example.com', 'document': '987654321'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_pacient(self):
        pacient = Pacient.objects.create(name='John Doe', email='john@example.com', document='123456789')
        url = reverse('pacients-detail', args=[pacient.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ProfessionalTests(BaseTestCase):
    def test_list_professionals(self):
        url = reverse('professional-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_professional(self):
        url = reverse('professional-list')
        data = {'name': 'Dr. John', 'email': 'drjohn@example.com', 'document': '123456789', 'specialty': 'Cardiology'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_professional(self):
        professional = Professional.objects.create(name='Dr. John', email='drjohn@example.com', document='123456789', specialty='Cardiology')
        url = reverse('professional-detail', args=[professional.id])
        data = {'name': 'Dr. John Smith', 'email': 'drjohnsmith@example.com', 'document': '987654321', 'specialty': 'Neurology'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_professional(self):
        professional = Professional.objects.create(name='Dr. John', email='drjohn@example.com', document='123456789', specialty='Cardiology')
        url = reverse('professional-detail', args=[professional.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ProcedureTests(BaseTestCase):
    def test_list_procedures(self):
        url = reverse('procedure-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_procedure(self):
        url = reverse('procedure-list')
        data = {'name': 'Blood Test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_procedure(self):
        procedure = Procedure.objects.create(name='Blood Test')
        url = reverse('procedure-detail', args=[procedure.id])
        data = {'name': 'Urine Test'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_procedure(self):
        procedure = Procedure.objects.create(name='Blood Test')
        url = reverse('procedure-detail', args=[procedure.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class RoomTests(BaseTestCase):
    def test_list_rooms(self):
        url = reverse('room-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_room(self):
        url = reverse('room-list')
        data = {'name': 'Room 101'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_room(self):
        room = Room.objects.create(name='Room 101')
        url = reverse('room-detail', args=[room.id])
        data = {'name': 'Room 102'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_room(self):
        room = Room.objects.create(name='Room 101')
        url = reverse('room-detail', args=[room.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class AppointmentTests(BaseTestCase):
    def test_list_appointments(self):
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_appointment(self):
        pacient = Pacient.objects.create(name='John Doe', email='john@example.com', document='123456789')
        professional = Professional.objects.create(name='Dr. John', email='drjohn@example.com', document='123456789', specialty='Cardiology')
        room = Room.objects.create(name='Room 101')
        url = reverse('appointment-list')
        data = {'name': 'Check-up', 'pacient': pacient.id, 'professional': professional.id, 'room': room.id, 'status': 'Scheduled', 'date': '2024-08-01'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_appointment(self):
        pacient = Pacient.objects.create(name='John Doe', email='john@example.com', document='123456789')
        professional = Professional.objects.create(name='Dr. John', email='drjohn@example.com', document='123456789', specialty='Cardiology')
        room = Room.objects.create(name='Room 101')
        appointment = Appointment.objects.create(pacient=pacient, professional=professional, room=room, status='Scheduled', date='2024-08-01')
        url = reverse('appointment-detail', args=[appointment.id])
        data = {'pacient': pacient.id, 'professional': professional.id, 'room': room.id, 'status': 'Completed', 'date': '2024-08-02'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_appointment(self):
        pacient = Pacient.objects.create(name='John Doe', email='john@example.com', document='123456789')
        professional = Professional.objects.create(name='Dr. John', email='drjohn@example.com', document='123456789', specialty='Cardiology')
        room = Room.objects.create(name='Room 101')
        appointment = Appointment.objects.create(pacient=pacient, professional=professional, room=room, status='Scheduled', date='2024-08-01')
        url = reverse('appointment-detail', args=[appointment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)