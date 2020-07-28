from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from ESearch.publisher import PublisherDocument


class PublisherDocumentSerializer(DocumentSerializer):
    class Meta:
        document = PublisherDocument
        fields = (
            'id',
            'name',
            'address',
            'city',
            'state_province',
            'country'
        )