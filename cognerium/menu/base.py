from rest_framework import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CustomModelSerializers(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(CustomModelSerializers, self).__init__(*args, **kwargs)
        if kwargs.get('context') and kwargs.get('context').get('data'):
            data = kwargs.get('context').get('data')
            fields = excludes = []
            if 'field' in data:
                fields = data.getlist('field', [])
            if 'fields' in data:
                fields = data.get('fields', [])
            if 'excludes' in data:
                excludes = data.get('excludes', [])
            if fields:
                included = set(fields)
                existing = set(self.fields.keys())

                for other in existing - included:
                    self.fields.pop(other)
            if excludes:
                for exclude in excludes:
                    self.fields.pop(exclude)


def CustomPaginator(queryset, page_size=5, page_number=1):
    paginator = Paginator(queryset, page_size)
    try:
        queryset = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    return queryset