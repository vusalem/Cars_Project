from django.urls import path, include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static



router = DefaultRouter()
router.register(r'brands', CarBrandViewSet)
router.register(r'carmodles', CarModelViewSet)
router.register(r'city', CityViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'year', YearViewSet)
router.register(r'color', ColorViewSet)
router.register(r'fueltype', FuelTypeViewSet)
router.register(r'transmitter', TransmitterViewSet)
router.register(r'bantype', BanTypeViewSet)
router.register(r'carmarch', CarMarchViewSet)
router.register(r'gearbox', GearBoxViewSet)



urlpatterns = [
    path('', views.main, name='main'),
    path('api', include(router.urls)),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('login-register/', views.login_register, name='login_register'), 
    path('help/', help_view, name='help'),
    path('create_car', views.create_car, name='create_car' ),
    path('user_cars', views.user_cars, name='user_cars'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('user_profile', user_profile, name='user_profile'),
    path('car_page/<int:car_id>/', views.car_page, name='car_page'),
    path('delete_profile', views.delete_profile, name='delete_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('salon/', views.salons, name='salons'),
    path('approve_car/<int:car_id>/', views.approve_car, name='approve_car'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('like', views.like_page, name='like_page'),
    path('favicon.ico/', RedirectView.as_view(url='/static/favicon.ico')),
    path('protected/', ProtectedView.as_view(), name='protected_view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# from .views import new_adv_view

