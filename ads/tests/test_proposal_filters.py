from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal


class ProposalFilterTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')

        self.ad_sender = Ad.objects.create(
            user=self.sender,
            title='Книга',
            category='BOOKS',
            condition='NEW',
            description='Учебник по Python',
            image_url=''
        )

        self.ad_receiver = Ad.objects.create(
            user=self.receiver,
            title='Ноутбук',
            category='ELECTRONICS',
            condition='USED',
            description='Б/у ноутбук',
            image_url=''
        )

        ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            comment='Предложение ожидает подтверждения',
            status='PENDING'
        )

        ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            comment='Предложение принято',
            status='ACCEPTED'
        )

    def test_filter_by_pending_status(self):
        self.client.login(username='receiver', password='password')

        response = self.client.get(reverse('all_proposals'), {'status': 'PENDING'})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Предложение ожидает подтверждения')
        self.assertNotContains(response, 'Предложение принято')

    def test_filter_by_accepted_status(self):
        self.client.login(username='receiver', password='password')

        response = self.client.get(reverse('all_proposals'), {'status': 'ACCEPTED'})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Предложение принято')
        self.assertNotContains(response, 'Предложение ожидает подтверждения')
