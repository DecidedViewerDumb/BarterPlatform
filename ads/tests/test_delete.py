from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad


class AdDeleteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Удаляемое объявление',
            category='ELECTRONICS',
            condition='NEW',
            description='Описание для удаления',
            image_url='http://example.com/image.jpg'
        )

    def test_delete_ad(self):
        self.client.login(username='testuser', password='password')

        self.assertEqual(Ad.objects.count(), 1)

        response = self.client.post(reverse('delete_ad', kwargs={'ad_id': self.ad.id}))

        self.assertEqual(Ad.objects.count(), 0)
        self.assertRedirects(response, reverse('index'))
