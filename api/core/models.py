from django.db import models

class Pacient(models.Model):
    name = models.TextField(max_length=100, verbose_name="Nome")
    document = models.TextField(max_length=11, verbose_name="CPF")
    email = models.TextField(max_length=30, verbose_name="E-mail")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paciente"


class Professional(models.Model):
    name = models.TextField(max_length=100, verbose_name="Nome")
    document = models.TextField(max_length=11, verbose_name="CPF")
    email = models.TextField(max_length=30, verbose_name="E-mail")
    specialty = models.TextField(max_length=30, verbose_name="Especialidade")

    def __str__(self):
        return self.name + f" {self.specialty}"
    
    class Meta:
        verbose_name = "Profissional"


class Procedure(models.Model):
    name = models.TextField(max_length=100, verbose_name="Nome")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Procedimento"


class Room(models.Model):
    name = models.TextField(max_length=100, verbose_name="Nome da Sala")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Sala"


class Appointment(models.Model):
    
    STATUS_CHOICES = [
        ('CANCELED', 'Canceled'),
        ('DONE', 'Done'),
        ('CONFIRMED', 'Confirmed'),
    ]

    paciente = models.ForeignKey(Pacient, on_delete=models.CASCADE, null=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, null=True)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(verbose_name="Data")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='CONFIRMED',
    )

    def __str__(self):
        return str(self.date) + f" {self.status}"
    
    class Meta:
        verbose_name = "Agendamento"