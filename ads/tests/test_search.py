from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad


class AdSearchTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.usertmp = User.objects.create_user(username='testuser_creator', password='password')
        self.ad1 = Ad.objects.create(
            user=self.usertmp,
            title='Объявление 1',
            category='ELECTRONICS',
            condition='NEW',
            description='Описание 1',
            image_url='http://example.com/image1.jpg'
        )
        self.ad2 = Ad.objects.create(
            user=self.usertmp,
            title='Объявление 2',
            category='CLOTHING',
            condition='USED',
            description='Описание 2',
            image_url='http://example.com/image2.jpg'
        )

    def test_search_by_title(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('index'), {'q': 'Объявление 1'})

        self.assertContains(response, 'Объявление 1')
        self.assertNotContains(response, 'Объявление 2')

    def test_filter_by_category(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('index'), {'category': 'ELECTRONICS'})

        self.assertContains(response, 'Объявление 1')
        self.assertNotContains(response, 'Объявление 2')
