from django.urls import path
from . import views

urlpatterns = [
    path('details/<id>/', views.productDetailsPage, name='product_details_page'),
    path('myproducts/', views.myProductPage, name='my_product_page'),
    path('myproducts/<id>', views.myProductDetailsPage, name='my_product_details_page'),
    path('add/', views.addProductPage, name='add_product_page'),
    path('update/<id>/', views.updateProductPage, name='update_product_page'),
    path('delete/<id>', views.deleteProductPage, name='delete_product_page'),

    path('like/<id>/', views.likeProduct, name='product_like'),
    path('dislike/<id>/', views.dislikeProduct, name='product_dislike'),
    path('report/<product_id>/', views.reportProduct, name='report_product'),

    path('updatecomment/<comment_id>/', views.updateCommentPage, name='update_comment'),
    path('deletecomment/<comment_id>', views.deleteCommentPage, name='delete_comment')
]
