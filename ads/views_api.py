from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related('user').all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.select_related('ad_sender__user', 'ad_receiver__user').all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(status='PENDING')

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        proposal = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(ExchangeProposal.STATUES_CHOICES):
            if request.user == proposal.ad_receiver.user:
                proposal.status = new_status
                proposal.save()
                return Response({'status': 'updated'})
        return Response({'error': 'Unauthorized or invalid status'}, status=403)
