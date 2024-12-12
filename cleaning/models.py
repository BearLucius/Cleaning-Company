from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    SERVICE_CHOICES = [
        ('general_cleaning', 'Общий клининг'),
        ('deep_cleaning', 'Генеральная уборка'),
        ('post_construction_cleaning', 'Послестроительная уборка'),
        ('dry_cleaning', 'Химчистка'),
    ]

    name = models.CharField(max_length=50, choices=SERVICE_CHOICES, unique=True, verbose_name='Название услуги')

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
        ('canceled', 'Отменено'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    contact_info = models.CharField(max_length=255, verbose_name='Контактная информация')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    preferred_date_time = models.DateTimeField(verbose_name='Дата и время')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, verbose_name='Тип оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name='Причина отмены')

    def __str__(self):
        return f"{self.user.username} - {self.service.get_name_display()}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

