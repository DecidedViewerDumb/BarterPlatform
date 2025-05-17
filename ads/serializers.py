from rest_framework import serializers
from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_sender_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        source='ad_sender',
        write_only=True
    )

    ad_receiver = AdSerializer(read_only=True)
    ad_receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        source='ad_receiver',
        write_only=True
    )

    class Meta:
        model = ExchangeProposal
        fields = [
            'id', 'ad_sender', 'ad_receiver', 'ad_sender_id', 'ad_receiver_id',
            'comment', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']
