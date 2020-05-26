from django_elasticsearch_dsl import DocType, Index
from ESearch.models import PostSearch

posts = Index("posts")


@posts.doc_type
class PostDocument(DocType):
    class Meta:
        model = PostSearch

        fields = [
            'title',
            'id',
            'slug',
            'description',
            'body'
        ]