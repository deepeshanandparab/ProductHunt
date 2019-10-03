from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('reported', 'Report')
    )

    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    image1 = models.ImageField(upload_to='images/product/screenshots/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/product/screenshots/', null=True, blank=True)
    image3 = models.ImageField(upload_to='images/product/screenshots/', null=True, blank=True)
    image4 = models.ImageField(upload_to='images/product/screenshots/', null=True, blank=True)
    image5 = models.ImageField(upload_to='images/product/screenshots/', null=True, blank=True)
    image6 = models.ImageField(upload_to='images/product/screenshots/', null=True, blank=True)
    icon = models.ImageField(upload_to='images/product/icons/', null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='active')
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Product with ID: ({self.id}) posted by {self.hunter}'


class ProductLikes(models.Model):
    post_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user_id} liked post number : {self.post_id.id}'


class ProductDislikes(models.Model):
    post_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user_id} disliked post number : {self.post_id.id}'


class ProductComment(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} commented on post : "{self.post.title}"'


class ProductReport(models.Model):
    REPORT_REASONS = (
        ('fake', 'Products listed in the post are fake'),
        ('hate', 'Post contains hateful content'),
        ('copy', 'Copyright issues regarding content'),
        ('expl', 'Post contains explicit/adult content'),
        ('other', 'Other reasons')
    )

    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reason = models.CharField(max_length=6, choices=REPORT_REASONS, default='', null=True, blank=True)
    report_description = models.TextField(null=True, blank=True)
    screenshot_1 = models.ImageField(upload_to='images/product/report/', null=True, blank=True)
    screenshot_2 = models.ImageField(upload_to='images/product/report/', null=True, blank=True)

    def __str__(self):
        return f'"{self.post}" reported by "{self.user}"'