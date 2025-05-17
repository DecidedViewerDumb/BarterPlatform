from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('BOOKS', 'Книги'),
        ('ELECTRONICS', 'Электроника'),
        ('CLOTHING', 'Одежда')
    ]

    CONDITION_CHOICES = [
        ('NEW', 'Новый'),
        ('USED', 'Б/у')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUES_CHOICES = [
        ('PENDING', 'Ожидает'),
        ('ACCEPTED', 'Принято'),
        ('REJECTED', 'Отклонено')
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField()
    status = models.CharField(max_length=50, choices=STATUES_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Предложение #{self.id}"

    def clean(self):
        errors = {}
        if self.ad_sender.user == self.ad_receiver.user:
            errors['ad_sender'] = "Нельзя предложить обмен самому себе."

        if self.ad_sender == self.ad_receiver:
            errors['ad_receiver'] = "Выберите другое объявление для обмена."

        if errors:
            raise ValidationError(errors)
