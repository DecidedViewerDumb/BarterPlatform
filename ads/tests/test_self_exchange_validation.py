from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal


class SelfExchangeValidationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='selfuser', password='password')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Объявление',
            category='BOOKS',
            condition='NEW',
            description='Описание',
            image_url=''
        )

    def test_self_exchange_clean_validation(self):
        proposal = ExchangeProposal(
            ad_sender=self.ad,
            ad_receiver=self.ad,
            comment='Хочу поменять сам с собой'
        )

        with self.assertRaises(ValidationError) as context:
            proposal.full_clean()

        self.assertIn('ad_sender', context.exception.message_dict)
