from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from product_hunt import settings
from product_hunt.filters import ProductFilter
from .models import Product, ProductComment, ProductLikes, ProductDislikes
from .forms import ProductForm, CommentForm, ReportForm


def productDetailsPage(request, id):
    product = Product.objects.get(pk=id)
    comment_form = CommentForm(request.POST or None)
    comments_list = ProductComment.objects.filter(post_id=product.id).order_by('-created_at')

    if product.likes.filter(id=request.user.id).exists():
        is_liked = True
        is_disliked = False
    elif product.dislikes.filter(id=request.user.id).exists():
        is_disliked = True
        is_liked = False
    else:
        is_liked = False
        is_disliked = False



    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = product
                comment.save()
                messages.success(request, 'Comment posted successfully.')
                return redirect('product_details_page', id=product.id)
            else:
                messages.error(request, 'Error occurred while posting comment.')
                return redirect('product_details_page', id=product.id)
        else:
            return redirect('log_in_page')
    else:
        form = CommentForm()
    context = {'title': 'Product Details',
               'product': product,
               'form': form,
               'comments_list': comments_list,
               'comment_form': comment_form,
               'is_liked':is_liked,
               'is_disliked':is_disliked}
    return render(request, 'products/product_details.html', context)

@login_required
def myProductPage(request):
    product_list = Product.objects.filter(hunter=request.user).order_by('-pub_date')
    filter = ProductFilter(request.GET, queryset=product_list)
    product_filter = ProductFilter(request.GET, queryset=product_list).qs
    paginator = Paginator(product_filter, 10)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    first_item_number = 10 * (response.number - 1) + 1

    context = {
                'title': 'My Products',
                'search_filter': filter,
               'product_list': response,
               'searchbox_needed':'Yes',
                'page_size': 10,
                'first_item_number': first_item_number
                }
    return render(request, 'products/my_product.html', context)


@login_required
def myProductDetailsPage(request, id):
    product = Product.objects.get(pk=id)

    comments_list = ProductComment.objects.filter(post_id=product.id).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = product
            comment.save()
            messages.success(request, 'Comment posted successfully.')
            return redirect('my_product_details_page', id=product.id)
        else:
            messages.error(request, 'Error occurred while posting comment.')
            return redirect('my_product_details_page', id=product.id)
    else:
        form = CommentForm()
        context = {'title': 'Product Details', 'product': product, 'form': form, 'comments_list':comments_list}
    return render(request, 'products/my_product_details.html', context)




'''------------------------------------------- Add Update and Delete Products -------------------------------------------'''

@login_required
def addProductPage(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, 'New product added successfully.')
            return redirect('my_product_page')
        else:
            return HttpResponse('Error Saving Details.')
    else:
        form = ProductForm()
        context = {'title': 'Add New Product', 'form': form}
    return render(request, 'products/add_product.html', context)


@login_required
def updateProductPage(request, id):
    product = Product.objects.get(pk=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product details updated successfully.')
        return redirect('my_product_page')
    return render(request, 'products/update_product.html', {'form':form, 'title':'Update Product'})


@login_required
def deleteProductPage(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    messages.success(request, 'Product has been deleted successfully.')
    return redirect('my_product_page')







'''-------------------------------------- Update and Delete Comments for Product ---------------------------------------'''

@login_required
def updateCommentPage(request, comment_id):
    comment = ProductComment.objects.get(pk=comment_id)
    comment_form = CommentForm(request.POST or None, instance=comment)

    if comment_form.is_valid():
        comment_form.save()
        messages.success(request, 'Comment updated successfully')
        return redirect('product_details_page', id=comment.post.id)
    else:
        messages.error(request, 'Error occurred while updating comment')
        return redirect('product_details_page', id=comment.post.id)
    return render(request, 'products/product_details.html', {'comment_form': comment_form, 'title': 'Product Details'})


@login_required
def deleteCommentPage(request, comment_id):
    comment = ProductComment.objects.get(pk=comment_id)
    comment.delete()
    messages.success(request, 'Comment has been deleted successfully.')
    return redirect('product_details_page', id=comment.post.id)






'''--------------------------------------- Likes and dislikes for the product post -----------------------------------------'''

@login_required
def likeProduct(request, id):
    product = Product.objects.get(id=id)
    is_liked = False
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        ProductLikes.objects.filter(post_id=product, user_id=request.user).delete()
        is_liked = False
    elif product.dislikes.filter(id=request.user.id).exists():
        product.dislikes.remove(request.user)
        ProductDislikes.objects.filter(post_id=product, user_id=request.user).delete()
        product.likes.add(request.user)
        ProductLikes.objects.create(post_id=product, user_id=request.user)
        is_disliked = False
        is_liked = True
    else:
        product.likes.add(request.user)
        ProductLikes.objects.create(post_id = product, user_id = request.user)
        product.dislikes.remove(request.user)
        ProductDislikes.objects.filter(post_id=product, user_id=request.user).delete()
        is_liked = True
        is_disliked = False
    return redirect('product_details_page', id= product.id)

@login_required
def dislikeProduct(request, id):
    product = Product.objects.get(id=id)
    is_disliked = False
    if product.dislikes.filter(id=request.user.id).exists():
        product.dislikes.remove(request.user)
        ProductDislikes.objects.filter(post_id=product, user_id=request.user).delete()
        is_disliked = False
    elif product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        ProductLikes.objects.filter(post_id=product, user_id=request.user).delete()
        product.dislikes.add(request.user)
        ProductDislikes.objects.create(post_id=product, user_id=request.user)
        is_liked = False
        is_disliked = True
    else:
        product.dislikes.add(request.user)
        ProductDislikes.objects.create(post_id = product, user_id = request.user)
        product.likes.remove(request.user)
        ProductLikes.objects.filter(post_id=product, user_id=request.user).delete()
        is_disliked = True
        is_liked = False
    return redirect('product_details_page', id= product.id)

def reportProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        report_form = ReportForm(request.POST, request.FILES)
        if report_form.is_valid():
            report_form.instance.post = product
            report_form.instance.user = request.user
            report_form.save()
            messages.success(request, 'Report accepted. Your report is under the verification process')


            # ------------------------- Mail for Admin -------------------------
            subject_for_admin = f'New issue reported'
            message_for_admin = f'Post "{product.title}" reported by {request.user}. ' \
                                f'Product is posted by {product.hunter}. Contact the post owner on the email listed below.' \
                                f'Contact with user who report the issue and post owner. Resolve the issue as soon as posible.'\
                                f'\n\n Post Owner Email: {product.hunter.email}'\
                                f'\n\n Issuer Email: {request.user.email}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            # ------------------------- Mail for Reported By -------------------------
            subject_for_user = f'Vertification email for reported issue'
            message_for_user = f'Hi {request.user}. Thank you for your concerns. ' \
                               f'We are looking into the issue that you have posted regarding the post' \
                               f'We will try to verify the issue with post owner and resolve it as soon as possible.'\
                               f'Thanks again for being such a fantastic member! \n\nCheers!!!\n[from Admin]'
            admin_email = settings.EMAIL_HOST_USER
            user_recipient_list = [request.user.email]
            try:
                send_mail(subject_for_admin, message_for_admin, from_email, recipient_list)
                send_mail(subject_for_user, message_for_user, admin_email, user_recipient_list)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('product_details_page', id= product.id)


        else:
            messages.error(request, 'Error occured while sending report')
            return redirect('product_details_page', id=product.id)
    else:
        report_form = ReportForm()
        return render(request, 'products/report_product.html', {'report_form':report_form, 'title':'Report'})
