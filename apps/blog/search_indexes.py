from haystack import indexes

from .models import Post


class PostSearchIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    title = indexes.CharField(indexed=False, model_attr='title')
    url = indexes.CharField(indexed=False, model_attr='get_absolute_url')
    publish_date = indexes.DateTimeField(model_attr='publish_date')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.latest_public()
