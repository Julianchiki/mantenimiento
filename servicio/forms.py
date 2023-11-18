from django import forms
from .models import Cars

class AddQuote(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(AddQuote, self).__init__(*args, **kwargs)
        
        # Filtrar el queryset de car_id para mostrar solo los autos asociados al usuario
        self.fields['car_id'].queryset = Cars.objects.filter(user_id=user.id)

    car_id = forms.ModelChoiceField(queryset=Cars.objects.none(), empty_label="Selecciona un auto", widget=forms.Select(attrs={'class': 'form-control', 'name': 'car_id'}))