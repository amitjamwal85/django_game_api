from django.shortcuts import render
from ESearch.documents import PostDocument
from ESearch.publisher import PublisherDocument
from ESearch.serializers import PublisherDocumentSerializer
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet



def search(request):
    q = request.GET.get('q')
    if q:
        posts = PostDocument.search().query("match", title=q)
    else:
        posts = ''

    return render(request, 'search.html', {'posts': posts})




class PublisherViewSet(DocumentViewSet):
    document = PublisherDocument
    serializer_class = PublisherDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # Define search fields
    search_fields = (
        'name',
        'address',
    )

    # Filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'name': 'name.raw',
        'city': 'city.raw',
    }

    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'name': 'name.raw',
        'address': 'address',
        'city': 'city',
        'state_province': 'state_province',
        'country': 'country',
    }

    # Specify default ordering
    ordering = ('id',)
