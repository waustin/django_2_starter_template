from haystack import indexes

from .models import Page


class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,)

    # Non-indexed fields to reduce DB hits
    title = indexes.CharField(indexed=False, model_attr='title')
    url = indexes.CharField(indexed=False, model_attr='get_absolute_url')

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        """ Used when the entire index for model is updated """
        return self.get_model().objects.filter(is_hidden=False)
