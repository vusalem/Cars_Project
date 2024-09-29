
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CarBrand(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.name}' 
    

class CarModel(models.Model):
    name = models.CharField(max_length=100) 
    brand = models.ForeignKey(CarBrand, related_name='models', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} ({self.brand.name})'


    

class City(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'



class Currency(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Year(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FuelType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
      
class Transmitter(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class BanType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class CarMarch(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class GearBox(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Car(models.Model):
    is_approved = models.BooleanField(default=False, verbose_name='Təsdiq')
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Qiymət')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    fueltype = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    transmitter = models.ForeignKey(Transmitter, on_delete=models.CASCADE)
    bantype = models.ForeignKey(BanType, on_delete=models.CASCADE)
    carmarch = models.ForeignKey(CarMarch, on_delete=models.CASCADE)
    gearbox = models.ForeignKey(GearBox, on_delete=models.CASCADE)
    front_view_image = models.ImageField(upload_to='elanlar/movie/img_cars', verbose_name='Ön görünüşü', blank=True, null=True)
    rear_view_image = models.ImageField(upload_to='elanlar/movie/img_cars', verbose_name='Arxa görünüşü', blank=True, null=True)
    interior_view_image = models.ImageField(upload_to='elanlar/movie/img_cars', verbose_name='Ön paneli', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)


    def increment_view_count(self):
        self.view_count += 1
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Kişi'), ('female', 'Qadın'), ('other', 'Digər')], null=True, blank=True)

    def __str__(self):
        return self.user.username


class ImageCar(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Avtomobil')
    image = models.ImageField(upload_to='elanlar/movie/img_cars', verbose_name='Şəkil')  # Eksik alan eklendi

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'Avtomobil Şəkili'
        verbose_name_plural = 'Avtomobil Şəkilləri'


class Salon(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    ads_count = models.PositiveIntegerField()
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.name

