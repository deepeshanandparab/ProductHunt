from django.contrib import admin
from .models import Product, ProductComment, ProductLikes, ProductDislikes, ProductReport

admin.site.register(Product)
admin.site.register(ProductComment)
admin.site.register(ProductLikes)
admin.site.register(ProductDislikes)
admin.site.register(ProductReport)
