import base64
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Car, User




def save_base64_image(file_data, filename):
    """
    Base64 formatında şəkili fayl sisteminə yazır.
    
    file_data: str
    filename: str
    """
    # Fayl sisteminə yazma prosesi burada olmalıdır
    # Məsələn:
    with open(f'media/car_images/{filename}.png', 'wb') as f:
        f.write(base64.b64decode(file_data.split(',')[1]))

@shared_task
def create_car_task(user_id, serialized_data, file_data_list):
    """
    Yeni avtomobil yaratmaq üçün asinxron iş.
    
    user_id: int
    serialized_data: dict
    file_data_list: list
    """
    user = User.objects.get(id=user_id)

    # Avtomobil məlumatlarını yaradır
    car = Car.objects.create(
        user=user,
        brand=serialized_data.get('brand'),  # Mümkün olan məlumatları alır
        car_models=serialized_data.get('car_models'),
        price=serialized_data.get('price'),
        color=serialized_data.get('color'),
        year_id=serialized_data.get('year'),
        additional_info=serialized_data.get('additional_info'),
        is_approved=False  # Təsdiq edilmədən öncə
    )

    # Şəkilləri fayl sisteminə yazır
    for idx, file_data in enumerate(file_data_list):
        filename = f"{user.username}_{car.id}_{idx}"
        save_base64_image(file_data, filename)

    # Email göndərmə
    subject = 'Yeni Avtomobil Elanı Yaradıldı'
    html_message = render_to_string('user/user_notify_email.html', {'car': car})
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email, settings.ADMIN_EMAIL]

    email = EmailMessage(subject, html_message, from_email, recipient_list)
    email.send()






