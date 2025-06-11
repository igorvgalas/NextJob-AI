from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import JobOffer
from .serializers import JobOfferSerializer


class JobOfferPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class JobOfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobOffer.objects.all().order_by('-created_at')
    serializer_class = JobOfferSerializer
    pagination_class = JobOfferPagination

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        if not isinstance(request.data, list):
            return Response({"detail": "Expected a list of items."}, status=400)

        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": f"{len(serializer.validated_data)} job offers created."}, status=201)
        return Response(serializer.errors, status=400)
