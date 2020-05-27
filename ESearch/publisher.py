from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import DocType, Index, fields
from ESearch.models import Publisher


article_index = Index('articles')
article_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# html_strip = analyzer(
#     'html_strip',
#     tokenizer="standard",
#     filter=["standard", "lowercase", "stop", "snowball"],
#     char_filter=["html_strip"]
# )


@article_index.doc_type
class PublisherDocument(DocType):
    id = fields.IntegerField(attr='id')
    name = fields.StringField(
        # analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )
    address = fields.StringField(
        # analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )
    city = fields.StringField(
        # analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )
    state_province = fields.StringField(
        # analyzer=html_strip,
        fields={
            'raw': fields.StringField( analyzer='keyword' ),
        }
    )
    country = fields.StringField(
        # analyzer=html_strip,
        fields={
            'raw': fields.StringField( analyzer='keyword' ),
        }
    )

    class Meta:
        model = Publisher