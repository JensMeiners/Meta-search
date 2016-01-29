import datetime
from django.utils import six
from haystack import indexes
from haystack.fields import LocationField
from mainApp.models import Project


class GeoField(LocationField):
    field_type = 'location'

    def prepare(self, obj):
        return obj

    def convert(self, value):
        return value

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    area_city = indexes.CharField()
    categoryName = indexes.CharField()

    content_auto = indexes.EdgeNgramField(model_attr='title')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')
    location = GeoField()
    geo_location_address = indexes.CharField(model_attr='get_location_address')

    def prepare_categoryName(self, object):
        return [category.name for category in object.categories.all()]

    def prepare_location(self, obj):
        # If you're just storing the floats...
        return obj.get_location()

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
