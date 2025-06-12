from django_filters.rest_framework import FilterSet
from .models import JobOffer


class JobOfferFilter(FilterSet):
    """ Filter class for the JobOffer model """

    class Meta:
        """ Fields to filter on """
        model = JobOffer
        fields = {
            'user': ['exact'],
            'email': ['exact'],
            'title': ['exact', 'icontains'],
            'company': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
            'created_at': ['exact', 'date__range'],
        }
