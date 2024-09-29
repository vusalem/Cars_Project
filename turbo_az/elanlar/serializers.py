from rest_framework import serializers
from .models import *


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ['id', 'name']



class CarModelSerializer(serializers.ModelSerializer):
    car_brand_name = serializers.SerializerMethodField()
    brand = serializers.PrimaryKeyRelatedField(queryset=CarBrand.objects.all())  # `car_brand`i ID olarak alır

    class Meta:
        model = CarModel
        fields = ['id', 'brand', 'car_brand_name', 'name']

    def get_car_brand_name(self, obj):
        return obj.brand.name

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class CurrencySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Currency
        fields = '__all__'

class YearSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Year
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Color
        fields = '__all__'

class FuelTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FuelType
        fields = '__all__'

class TransmitterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transmitter
        fields = '__all__'


class BanTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BanType
        fields = '__all__'


class CarMarchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CarMarch
        fields = '__all__'


class GearBoxSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GearBox
        fields = '__all__'



class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'
