import base64


from .forms import *
from .models import *
from .serializers import *
from django.conf import settings
from .tasks import create_car_task
from rest_framework import viewsets
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required






def main(request):
    form = CarFilterForm(request.GET or None)

    filters = {}
    
    # Start with all approved cars
    cars = Car.objects.filter(is_approved=True)

    if form.is_valid():  
        cleaned_data = form.cleaned_data

        if cleaned_data.get('brand'):
            filters['brand'] = cleaned_data['brand']
        if cleaned_data.get('model'):
            filters['model'] = cleaned_data['model']  # Düzəliş olunmuş hissə
        if cleaned_data.get('city'):
            filters['city'] = cleaned_data['city']
        if cleaned_data.get('min_price'):
            filters['price__gte'] = cleaned_data['min_price']
        if cleaned_data.get('max_price'):
            filters['price__lte'] = cleaned_data['max_price']
        if cleaned_data.get('currency'):
            filters['currency'] = cleaned_data['currency']
        if cleaned_data.get('min_year'):
            filters['year__gte'] = cleaned_data['max_year']
        if cleaned_data.get('max_year'):
            filters['year__lte'] = cleaned_data['min_year']
        if cleaned_data.get('color'):
            filters['color'] = cleaned_data['color']
        if cleaned_data.get('fueltype'):
            filters['fueltype'] = cleaned_data['fueltype']
        if cleaned_data.get('transmitter'):
            filters['transmitter'] = cleaned_data['transmitter']
        if cleaned_data.get('bantype'):
            filters['bantype'] = cleaned_data['bantype']
        if cleaned_data.get('carmarch'):
            filters['carmarch'] = cleaned_data['carmarch']
        if cleaned_data.get('gearbox'):
            filters['gearbox'] = cleaned_data['gearbox']

    # Apply the filters to the cars queryset
    
        cars = cars.filter(**filters)
    context = {
        'form': form,
        'cars': cars,  # Include the filtered or all cars here
        'brands_car': CarBrand.objects.all(),
        'models_car': CarModel.objects.all(),
        'city': City.objects.all(),
        'currency': Currency.objects.all(),
        'year': Year.objects.all(),
        'color': Color.objects.all(),
        'fueltype': FuelType.objects.all(),
        'transmitter': Transmitter.objects.all(),
        'bantype': BanType.objects.all(),
        'carmarch': CarMarch.objects.all(),
        'gearbox': GearBox.objects.all()      
    }

    return render(request, 'elanlar/main.html', context)
class CarBrandViewSet(viewsets.ModelViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer

    @action(detail=True, methods=['get'])
    def models(self, request, pk=None):
        brand = self.get_object()
        car_models = CarModel.objects.filter(brand=brand)
        serializer = CarModelSerializer(car_models, many=True)
        return Response(serializer.data)


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer



class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer



class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class YearViewSet(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class FuelTypeViewSet(viewsets.ModelViewSet):
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer


class TransmitterViewSet(viewsets.ModelViewSet):
    queryset = Transmitter.objects.all()
    serializer_class = TransmitterSerializer

class BanTypeViewSet(viewsets.ModelViewSet):
    queryset = BanType.objects.all()
    serializer_class = BanTypeSerializer


class CarMarchViewSet(viewsets.ModelViewSet):
    queryset = CarMarch.objects.all()
    serializer_class = CarMarchSerializer


class GearBoxViewSet(viewsets.ModelViewSet):
    queryset = GearBox.objects.all()
    serializer_class = GearBoxSerializer


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # İstifadəçi adı yoxlanışı
        if not username:
            messages.error(request, 'İstifadəçi adı daxil edilməlidir.')
            return render(request, 'elanlar/register_user.html')

        # E-mail yoxlanışı
        if not email:
            messages.error(request, 'E-mail daxil edilməlidir.')
            return render(request, 'elanlar/register_user.html')

        # Şifrələrin uyğunluğu yoxlanışı
        if password != confirm_password:
            messages.error(request, 'Şifrələr uyğun deyil.')
            return render(request, 'elanlar/register_user.html')

        # İstifadəçi adı mövcuddurmu?
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu istifadəçi adı artıq mövcuddur.')
            return render(request, 'elanlar/register_user.html')

        # İstifadəçi yaratma
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        # Profil yaratma və ya yeniləmə
        try:
            profile = Profile.objects.get(user=user)
            profile.phone = phone
            profile.gender = gender
            profile.birth_date = birth_date
            profile.save()
        except ObjectDoesNotExist:
            profile = Profile.objects.create(user=user, phone=phone, gender=gender, birth_date=birth_date)

        # İstifadəçini uğurla qeydiyyatdan keçirdikdən sonra yönləndir
        messages.success(request, 'Qeydiyyat uğurla tamamlandı. Zəhmət olmasa, daxil olun.')
        return redirect('login')  # Burada 'login' sizin login səhifənizin URL adıdır.

    # Əgər sorğu 'GET' üsulu ilə olarsa, qeydiyyat səhifəsini göstər
    return render(request, 'elanlar/register_user.html')



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş uğurlu oldu.')  # Uğurlu giriş mesajı
            return redirect('main')  # İstifadəçini əsas səhifəyə yönləndir

        else:
            messages.error(request, 'Yanlış istifadəçi adı və ya şifrə.')
    
    return render(request, 'elanlar/login_user.html')


def login_register(request):
    return render(request, 'elanlar/login_register.html')


def help_view(request):
    return render(request, 'elanlar/help.html')  # This will render the help.html template


# def new_adv_view(request):
#     return render(request, 'elanlar/new_adv.html')

@login_required
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            # Form məlumatlarını model instansiyasına çevir
            car_instance = form.save(commit=False)
            car_instance.user = request.user
            car_instance.save()

            # Model instansiyasını serializer ilə JSON formatına çevir
            serializer = CarSerializer(car_instance)
            serialized_data = serializer.data

            # Faylları base64 formatına çevir
            file_data_list = []
            for file in request.FILES.values():
                file_data = base64.b64encode(file.read()).decode('utf-8')
                file_data_list.append(f"data:{file.content_type};base64,{file_data}")

            # Asinxron iş yarat
            create_car_task.delay(request.user.id, serialized_data, file_data_list)

            # Email göndərmə
            subject = 'Yeni Elanınız Yaradıldı'
            html_message = render_to_string('elanlar/user_notify_email.html', {'car': serialized_data})
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email, settings.ADMIN_EMAIL]

            email = EmailMessage(subject, html_message, from_email, recipient_list)
            email.send()
            messages.success(request, 'İlanınız göndərildi və admin tərəfindən təsdiqlənməsini gözləyir.')
            return redirect('main')
    else:
        form = CarForm()

    context = {
        'form': form,
        'brands_car': CarBrand.objects.all(),
        'models_car': CarModel.objects.all(),
        'city': City.objects.all(),
        'currency': Currency.objects.all(),
        'year': Year.objects.all(),
        'color': Color.objects.all(),
        'fueltype': FuelType.objects.all(),
        'transmitter': Transmitter.objects.all(),
        'bantype': BanType.objects.all(),
        'carmarch': CarMarch.objects.all(),
        'gearbox': GearBox.objects.all()   
    }
    return render(request, 'elanlar/create_car.html', context)


@login_required
def delete_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        messages.error(request, 'Bu avtomobil tapılmadı.')
        return redirect('main')
    
    if car.user != request.user:
        messages.error(request, 'Siz bu elanı silməyə icazəniz yoxdur.')
        return redirect('main')
    
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Avtomobil uğurla silindi.')
        return redirect('main')
    
    return render(request, 'elanlar/delete_car.html', {'car': car})
@login_required
def user_cars(request):
    user = request.user
    cars = Car.objects.filter(user=user)
    return render(request, 'elanlar/user_cars.html', {'cars': cars})


@login_required
def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Profil yaradın
        profile = Profile.objects.create(user=request.user)
    
    approved_cars = Car.objects.filter(user=request.user, is_approved=True)
    pending_cars = Car.objects.filter(user=request.user, is_approved=False)
    context = {
        'profile': profile,
        'approved_cars': approved_cars,
        'pending_cars': pending_cars
    }
    return render(request, 'elanlar/user_profile.html', context)



@login_required
def delete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        user = profile.user
        profile.delete()
        user.delete()  # İstifadəçini də silmək üçün
        messages.success(request, 'Profil və istifadəçi uğurla silindi.')
        return redirect('main')  # Silindikdən sonra ana səhifəyə yönləndiririk
    return render(request, 'elanlar/delete_profile.html', {'profile': profile})


def car_page(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.increment_view_count()
    return render(request, 'elanlar/car_page.html', {'car': car})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = form.cleaned_data['phone']
            profile.gender = form.cleaned_data['gender']
            profile.birth_date = form.cleaned_data['birth_date']
            profile.save()
            messages.success(request, 'Profiliniz uğurla yeniləndi.')
            return redirect('main')  # Əsas səhifəyə yönləndirir
    else:
        form = ProfileForm(instance=request.user, user=request.user)
    
    return render(request, 'elanlar/edit_profile.html', {'form': form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if car.user != request.user:
        messages.error(request, 'Siz bu elanı redaktə etməyə icazəniz yoxdur.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = CarForm(instance=car)
    
    return render(request, 'elanlar/edit_car.html', {'form': form, 'car': car})


@login_required
def approve_car(request, car_id):
    if request.user.is_superuser:
        try:
            car = Car.objects.get(id=car_id)
            car.is_approved = True
            car.save()
            messages.success(request, 'Elan təsdiqləndi.')
        except Car.DoesNotExist:
            messages.error(request, 'Elan tapılmadı.')
    else:
        messages.error(request, 'İcazəniz yoxdur.')
    
    return redirect('admin_car_list')


def salons(request):
    salons = Salon.objects.all()
    return render(request, 'elanlar/salons.html', {'salons': salons})


def like_page(request):
    return render(request, 'elanlar/like.html')


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Bu, qorunan bir görünüşdür.'}
        return Response(content)
    




