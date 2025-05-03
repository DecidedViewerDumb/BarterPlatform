from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad


class AdCreationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_ad(self):
        self.client.login(username='testuser', password='password')

        data = {
            'title': 'Тестовое объявление',
            'category': 'ELECTRONICS',
            'condition': 'NEW',
            'description': 'Описание объявления',
            'image_url': ''
        }

        response = self.client.post(reverse('create_ad'), data)

        print(response.status_code)

        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(Ad.objects.first().title, 'Тестовое объявление')
        self.assertRedirects(response, reverse('index'))
