from django_elasticsearch_dsl_drf.serializers import DocumentSerializer


class PublisherDocumentSerializer(DocumentSerializer):

    class Meta(object):
        fields = (
            'id',
            'name',
            'info',
            'address',
            'city',
            'state_province',
            'country',
            'website',
        )