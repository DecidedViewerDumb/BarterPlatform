from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad


class ExchangeProposalTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.receiver = User.objects.create_user(username='testreceiver', password='password')

        self.ad_sender = Ad.objects.create(
            user=self.user,
            title='Объявление 1',
            category='ELECTRONICS',
            condition='NEW',
            description='Описание 1',
            image_url='http://example.com/image1.jpg'
        )

        self.ad_receiver = Ad.objects.create(
            user=self.receiver,
            title='Объявление 2',
            category='CLOTHING',
            condition='USED',
            description='Описание 2',
            image_url='http://example.com/image2.jpg'
        )

    def test_create_exchange_proposal(self):
        self.client.login(username='testuser', password='password')

        data = {
            'ad_sender': self.ad_sender.id,
            'comment': 'Предложение обмена'
        }

        response = self.client.post(reverse('create_proposal', kwargs={'ad_id': self.ad_sender.id}), data)

        self.assertEqual(len(self.ad_sender.sent_proposals.all()), 1)
        self.assertEqual(self.ad_sender.sent_proposals.first().status, 'PENDING')
        self.assertRedirects(response, reverse('index'))
