import requests
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .forms import UserForm, PacienteForm, ProfessionalForm, ProcedureForm, RoomForm
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'base.html')

class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        response = requests.post('http://api:8000/api/user/login/', data={'email': email, 'password': password})
        if response.status_code == 200:
            token = response.json().get('token')
            request.session['access_token'] = token['access']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User(username=email, email=email)
                user.save()
            return user
        return None

def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = CustomBackend().authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('paciente_list')
        else:
            messages.error(request, 'Invalid email or password')
    
    if request.user.is_authenticated:
        return redirect('paciente_list')
    
    return render(request, 'pages/login.html')

def custom_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            response = requests.post('http://api:8000/api/user/register/', data={
                'name': name,
                'email': email,
                'password': password,
                'password2': password
            })

            if response.status_code == 201:
                user = User(username=email, email=email)
                user.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, response.json()['errors'])
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = UserForm()

    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'pages/register.html', {'form': form})

def custom_logout(request):
    django_logout(request)

    return redirect('login')

def home(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')
    return render(request, 'pages/paciente.html')

class PacienteListView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        if not access_token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('http://api:8000/api/core/pacients/', headers=headers)

        if response.status_code == 200:
            pacientes = response.json()
        else:
            pacientes = {}

        return render(request, 'pages/paciente.html', {'pacientes': pacientes})


class PacienteCreateView(View):
    def get(self, request):
        form = PacienteForm()
        return render(request, 'pacientes/paciente_form.html', {'form': form})

    def post(self, request):
        form = PacienteForm(request.POST)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post('http://api:8000/api/core/pacients/', data=form.cleaned_data, headers=headers)
            if response.status_code in [200, 201]:
                paciente = response.json()
                return JsonResponse({'success': True, 'paciente': paciente})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao adicionar paciente'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)


class PacienteUpdateView(View):
    def put(self, request, id):
        data = json.loads(request.body)
        form = PacienteForm(data)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            response = requests.put(f'http://api:8000/api/core/pacients/{id}/', data=json.dumps(form.cleaned_data), headers=headers)
            if response.status_code == 200:
                paciente = response.json()
                return JsonResponse({'success': True, 'paciente': paciente})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao atualizar paciente'}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)


class PacienteDeleteView(View):
    def delete(self, request, id):
        access_token = request.session.get('access_token')
        if not access_token:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        headers = {'Authorization': f'Bearer {access_token}'}
        api_url = f'http://api:8000/api/core/pacients/{id}/'

        response = requests.delete(api_url, headers=headers)
        
        if response.status_code == 204:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to delete'}, status=response.status_code)


class ProfessionalListView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        if not access_token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('http://api:8000/api/core/professional/', headers=headers)

        if response.status_code == 200:
            profissionais = response.json()
        else:
            profissionais = {}

        return render(request, 'pages/profissionais.html', {'profissionais': profissionais})


class ProfessionalCreateView(View):
    def get(self, request):
        form = ProfessionalForm()
        return render(request, 'pacientes/professional_form.html', {'form': form})

    def post(self, request):
        form = ProfessionalForm(request.POST)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post('http://api:8000/api/core/professional/', data=form.cleaned_data, headers=headers)
            if response.status_code in [200, 201]:
                profissional = response.json()
                return JsonResponse({'success': True, 'profissional': profissional})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao adicionar profissional'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)

class ProfessionalUpdateView(View):
    def put(self, request, id):
        data = json.loads(request.body)
        form = ProfessionalForm(data)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            response = requests.put(f'http://api:8000/api/core/professional/{id}/', data=json.dumps(form.cleaned_data), headers=headers)
            if response.status_code == 200:
                profissional = response.json()
                return JsonResponse({'success': True, 'profissional': profissional})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao atualizar profissional'}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class ProfessionalDeleteView(View):
    def delete(self, request, id):
        access_token = request.session.get('access_token')
        if not access_token:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        headers = {'Authorization': f'Bearer {access_token}'}
        api_url = f'http://api:8000/api/core/professional/{id}/'

        response = requests.delete(api_url, headers=headers)
        
        if response.status_code == 204:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to delete'}, status=response.status_code)

# procedimentos views

class ProcedureListView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        if not access_token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('http://api:8000/api/core/procedure/', headers=headers)

        if response.status_code == 200:
            procedure = response.json()
        else:
            procedure = {}

        return render(request, 'pages/procedimentos.html', {'procedimentos': procedure})

class ProcedureCreateView(View):
    def get(self, request):
        form = ProcedureForm()
        return render(request, 'pacientes/procedure_form.html', {'form': form})

    def post(self, request):
        form = ProcedureForm(request.POST)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post('http://api:8000/api/core/procedure/', data=form.cleaned_data, headers=headers)
            if response.status_code in [200, 201]:
                procedimento = response.json()
                return JsonResponse({'success': True, 'procedimento': procedimento})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao adicionar procedimento'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)

class ProcedureUpdateView(View):
    def put(self, request, id):
        data = json.loads(request.body)
        form = ProcedureForm(data)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            response = requests.put(f'http://api:8000/api/core/procedure/{id}/', data=json.dumps(form.cleaned_data), headers=headers)
            if response.status_code == 200:
                procedimento = response.json()
                return JsonResponse({'success': True, 'procedimento': procedimento})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao atualizar procedimento'}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class ProcedureDeleteView(View):
    def delete(self, request, id):
        access_token = request.session.get('access_token')
        if not access_token:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        headers = {'Authorization': f'Bearer {access_token}'}
        api_url = f'http://api:8000/api/core/procedure/{id}/'

        response = requests.delete(api_url, headers=headers)
        
        if response.status_code == 204:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to delete'}, status=response.status_code)

# salas views

class RoomListView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        if not access_token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('http://api:8000/api/core/room/', headers=headers)

        if response.status_code == 200:
            salas = response.json()
        else:
            salas = {}

        return render(request, 'pages/salas.html', {'salas': salas})

class RoomCreateView(View):
    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post('http://api:8000/api/core/room/', data=form.cleaned_data, headers=headers)
            if response.status_code in [200, 201]:
                sala = response.json()
                return JsonResponse({'success': True, 'sala': sala})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao adicionar sala'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)

class RoomUpdateView(View):
    def put(self, request, id):
        data = json.loads(request.body)
        form = RoomForm(data)
        if form.is_valid():
            access_token = request.session.get('access_token')
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            response = requests.put(f'http://api:8000/api/core/room/{id}/', data=json.dumps(form.cleaned_data), headers=headers)
            if response.status_code == 200:
                sala = response.json()
                return JsonResponse({'success': True, 'sala': sala})
            else:
                return JsonResponse({'success': False, 'error': 'Erro ao atualizar sala'}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class RoomDeleteView(View):
    def delete(self, request, id):
        access_token = request.session.get('access_token')
        if not access_token:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        headers = {'Authorization': f'Bearer {access_token}'}
        api_url = f'http://api:8000/api/core/room/{id}/'

        response = requests.delete(api_url, headers=headers)
        
        if response.status_code == 204:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to delete'}, status=response.status_code)

# agendamento views

class AppointmentListView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        if not access_token:
            return redirect('login')
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('http://api:8000/api/core/appointment/', headers=headers)

        if response.status_code == 200:
            agendamentos = response.json()
        else:
            agendamentos = {}

        return render(request, 'pages/agendamentos.html', {'agendamentos': agendamentos})

class AppointmentDeleteView(View):
    def delete(self, request, id):
        access_token = request.session.get('access_token')
        if not access_token:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        headers = {'Authorization': f'Bearer {access_token}'}
        api_url = f'http://api:8000/api/core/appointment/{id}/'

        response = requests.delete(api_url, headers=headers)
        
        if response.status_code == 204:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to delete'}, status=response.status_code)

class AppointmentUpdateView(View):
    def patch(self, request, id):
        access_token = request.session.get('access_token')
        if not access_token:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        headers = {'Authorization': f'Bearer {access_token}'}
        api_url = f'http://api:8000/api/core/appointment/{id}/'

        data = json.loads(request.body)

        response = requests.patch(api_url, data=data, headers=headers)
        if response.status_code == 200:
            return JsonResponse({'success': True, 'appointment': response.json()})
        else:
            return JsonResponse({'success': False, 'errors': response.json()}, status=response.status_code)


        
