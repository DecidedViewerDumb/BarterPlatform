from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal


class ProposalStatusUpdateTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')

        self.ad_sender = Ad.objects.create(
            user=self.sender,
            title='A',
            category='BOOKS',
            condition='NEW',
            description='',
            image_url=''
        )
        self.ad_receiver = Ad.objects.create(
            user=self.receiver,
            title='B',
            category='BOOKS',
            condition='NEW',
            description='',
            image_url=''
        )

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            comment='Хочу обменяться',
            status='PENDING'
        )

    def test_update_status_to_accepted(self):
        self.client.login(username='receiver', password='password')

        response = self.client.post(
            reverse(
                'update_proposal_status',
                kwargs={
                    'proposal_id': self.proposal.id
                }
            ),
            {
                'status': 'ACCEPTED'
            }
        )

        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'ACCEPTED')
        self.assertRedirects(response, reverse('all_proposals'))

    def test_forbidden_user_cannot_update_status(self):
        self.client.login(username='sender', password='password')

        response = self.client.post(
            reverse(
                'update_proposal_status',
                kwargs={
                    'proposal_id': self.proposal.id
                }
            ),
            {
                'status': 'REJECTED'
            }
        )

        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'PENDING')
        self.assertRedirects(response, reverse('all_proposals'))
