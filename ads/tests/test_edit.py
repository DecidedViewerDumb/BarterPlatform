from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad


class AdEditTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Старое название',
            category='ELECTRONICS',
            condition='NEW',
            description='Старое описание',
            image_url=''
        )

    def test_edit_ad(self):
        self.client.login(username='testuser', password='password')

        data = {
            'title': 'Новое название',
            'category': 'CLOTHING',
            'condition': 'USED',
            'description': 'Новое описание',
            'image_url': ''
        }

        response = self.client.post(reverse('edit_ad', kwargs={'ad_id': self.ad.id}), data)

        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Новое название')
        self.assertEqual(self.ad.category, 'CLOTHING')
        self.assertEqual(self.ad.condition, 'USED')
        self.assertEqual(self.ad.description, 'Новое описание')
        self.assertRedirects(response, reverse('my_ads'))
