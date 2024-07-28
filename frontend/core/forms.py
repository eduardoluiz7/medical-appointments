from django import forms

class UserForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput
    )

class PacienteForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    document = forms.CharField(max_length=11, required=True)

class ProfessionalForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    document = forms.CharField(max_length=11, required=True)
    specialty = forms.CharField(max_length=80, required=True)

class ProcedureForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)

class RoomForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)