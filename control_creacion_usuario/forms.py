# forms.py
from django import forms
from .models import Imagen_sig,PDF_sig

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen_sig
        fields = ['archivo_adjunto']

class PDFForm(forms.ModelForm):    
    class Meta:
        model = PDF_sig

        fields = ['archivo_adjunto','nombre']

