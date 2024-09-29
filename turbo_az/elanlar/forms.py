from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import *



class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
    
class CarFilterForm(forms.Form): 

    brand = forms.ChoiceField(choices=[('', '-------')], required=False)
    model = forms.ChoiceField(choices=[('', '-------')], required=False)
    city = forms.ChoiceField(choices=[('', '-------')], required=False)
    currency = forms.ChoiceField(choices=[('', '-------')], required=False)
    min_year = forms.ModelChoiceField(queryset=Year.objects.all(), required=False)
    max_year = forms.ModelChoiceField(queryset=Year.objects.all(), required=False)
    color = forms.ChoiceField(choices=[('', '-------')], required=False)
    fueltype = forms.ChoiceField(choices=[('', '-------')], required=False)
    transmitter = forms.ChoiceField(choices=[('', '-------')], required=False)
    bantype = forms.ChoiceField(choices=[('', '-------')], required=False)
    carmarch = forms.ChoiceField(choices=[('', '-------')], required=False)
    gearbox = forms.ChoiceField(choices=[('', '-------')], required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)



    # customer = forms.ChoiceField(choices=[('', '-------')], required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].choices += [(brand.id, brand.name) for brand in CarBrand.objects.all()]
        self.fields['model'].choices += [(model.id, model.name) for model in CarModel.objects.all()]
        self.fields['city'].choices += [(city.id, city.name) for city in City.objects.all()]
        self.fields['currency'].choices += [(currency.id, currency.name) for currency in Currency.objects.all()]
        self.fields['color'].choices += [(color.id, color.name) for color in Color.objects.all()]
        self.fields['fueltype'].choices += [(fueltype.id, fueltype.name) for fueltype in FuelType.objects.all()]
        self.fields['transmitter'].choices += [(transmitter.id, transmitter.name) for transmitter in Transmitter.objects.all()]
        self.fields['bantype'].choices += [(bantype.id, bantype.name) for bantype in BanType.objects.all()]
        self.fields['carmarch'].choices += [(carmarch.id, carmarch.name) for carmarch in CarMarch.objects.all()]
        self.fields['gearbox'].choices += [(gearbox.id, gearbox.name) for gearbox in GearBox.objects.all()]

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    phone = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=[('male', 'Kişi'), ('female', 'Qadın'), ('other', 'Digər')])
    birth_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')

        return cleaned_data
    
class ProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    birth_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                profile = Profile.objects.get(user=user)
                self.fields['phone'].initial = profile.phone
                self.fields['gender'].initial = profile.gender
                self.fields['birth_date'].initial = profile.birth_date
            except Profile.DoesNotExist:
                pass