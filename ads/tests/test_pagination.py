from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad


class PaginationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.viewer = User.objects.create_user(username='viewer', password='password')

        for i in range(15):
            Ad.objects.create(
                user=self.user,
                title=f'Объявление {i}',
                category='BOOKS',
                condition='NEW',
                description='Описание',
                image_url=''
            )

    def test_index_pagination_limit(self):
        self.client.login(username='viewer', password='password')
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context['ads']), 10)

        response2 = self.client.get(reverse('index') + '?page=2')
        self.assertTrue(len(response2.context['ads']) > 0)
