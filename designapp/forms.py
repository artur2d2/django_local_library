from django import forms

class values(forms.Form):
    liquid_flux = forms.DecimalField(label='liquid flux', widget=forms.TextInput(attrs={'placeholder': 'Kg/s'}), max_digits=30, decimal_places=6)
    vapor_flux = forms.DecimalField(label='vapor flux', widget=forms.TextInput(attrs={'placeholder': 'Kg/s'}), max_digits=30, decimal_places=6)
    liquid_density = forms.DecimalField(label='liquid density', widget=forms.TextInput(attrs={'placeholder': 'Kg/m^3'}), max_digits=30, decimal_places=6)
    vapor_density = forms.DecimalField(label='vapor density', widget=forms.TextInput(attrs={'placeholder': 'Kg/m^3'}), max_digits=30, decimal_places=6)
    API = forms.DecimalField(label='API Gravity', widget=forms.TextInput(attrs={'placeholder': 'API'}), max_digits=30, decimal_places=6)

    def clean(self):
        cleaned_data = super().clean()
        liquid_flux = cleaned_data.get("liquid_flux")
        vapor_flux = cleaned_data.get("vapor_flux")
        liquid_density = cleaned_data.get("liquid_density")
        vapor_density = cleaned_data.get("vapor_density")
        API = cleaned_data.get("API")
