from django.forms import TextInput
from products.models import Product
import django_filters

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains',
                                      widget=TextInput
                                        (
                                          attrs={
                                              'placeholder': 'Enter Title',
                                              'class': 'form form-control mb-2'
                                                 }),label='Post Title')
    hunter__username = django_filters.CharFilter(widget=TextInput
                                       (
                                           attrs=
                                            {'placeholder': 'Enter Username',
                                             'class': 'form form-control mb-2'
                                             }),label='Posts By')
    class Meta:
        model = Product
        fields = ['title', 'hunter__username']