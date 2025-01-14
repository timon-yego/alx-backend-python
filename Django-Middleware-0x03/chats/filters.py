from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    user = filters.CharFilter(field_name="sender__username", lookup_expr="icontains")
    start_date = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']
