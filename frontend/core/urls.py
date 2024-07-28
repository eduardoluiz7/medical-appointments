from django.urls import path
from .views import (
    PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView, 
    ProfessionalListView, ProfessionalUpdateView, ProfessionalCreateView, ProfessionalDeleteView,
    ProcedureListView, ProcedureCreateView, ProcedureUpdateView, ProcedureDeleteView,
    RoomCreateView, RoomListView, RoomUpdateView, RoomDeleteView,
    AppointmentListView, AppointmentDeleteView, AppointmentUpdateView
)

urlpatterns = [
    # pacientes
    path('pacientes', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/novo/', PacienteCreateView.as_view(), name='paciente_create'),
    path('paciente/editar/<int:id>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('paciente/<int:id>/excluir/', PacienteDeleteView.as_view(), name='paciente_delete'),
    # profissionais
    path('profissionais', ProfessionalListView.as_view(), name='profissional_list'),
    path('profissionais/novo/', ProfessionalCreateView.as_view(), name='profissional_create'),
    path('profissional/editar/<int:id>/', ProfessionalUpdateView.as_view(), name='profissional_update'),
    path('profissional/<int:id>/excluir/', ProfessionalDeleteView.as_view(), name='profissional_delete'),
    # procedimentos
    path('procedimentos', ProcedureListView.as_view(), name='procedimento_list'),
    path('procedimentos/novo/', ProcedureCreateView.as_view(), name='procedimento_create'),
    path('procedimento/editar/<int:id>/', ProcedureUpdateView.as_view(), name='procedimento_update'),
    path('procedimento/<int:id>/excluir/', ProcedureDeleteView.as_view(), name='procedimento_delete'),
    # salas
    path('salas', RoomListView.as_view(), name='sala_list'),
    path('salas/novo/', RoomCreateView.as_view(), name='sala_create'),
    path('salas/editar/<int:id>/', RoomUpdateView.as_view(), name='sala_update'),
    path('salas/<int:id>/excluir/', RoomDeleteView.as_view(), name='sala_delete'),
    # agendamentos
    path('agendamentos', AppointmentListView.as_view(), name='agendamento_list'),
    path('agendamento/<int:id>/excluir/', AppointmentDeleteView.as_view(), name='agendamento_delete'),
    path('agendamento/editar/<int:id>/', AppointmentUpdateView.as_view(), name='agendamento_update'),
]
