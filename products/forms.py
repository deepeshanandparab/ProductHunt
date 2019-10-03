from django import forms
from .models import Product, ProductComment, ProductReport

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title','body','url','image1','image2','image3','image4','image5','image6','icon','hunter']


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add a public comment', 'rows': 4}), label='')

    class Meta:
        model = ProductComment
        fields = ['text']

class ReportForm(forms.ModelForm):
    report_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Describe your reason for reporting in few words', 'rows': 4}))

    class Meta:
        model = ProductReport
        fields = ['reason','report_description','screenshot_1','screenshot_2']
