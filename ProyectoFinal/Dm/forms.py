from django import forms
from django.contrib.auth.models import User
class FormMensajes(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea(attrs={
        "class": "formulario_ms",
        "placeholder": "Escribe tu mensaje"
    }))
    
class SeleccionarDestinatarioForm(forms.Form):
    destinatario = forms.ModelChoiceField(queryset=User.objects.all())