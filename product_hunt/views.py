from product_hunt import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from product_hunt.forms import ContactForm
from products.models import Product, ProductComment
from .filters import ProductFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def homePage(request):
    product_list = Product.objects.all().order_by('-pub_date')
    filter = ProductFilter(request.GET, queryset=product_list)
    # postby_filter = PostByFilter(request.GET, queryset=product_list)
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
                'title': 'Home',
               'product_list': response,
               'search_filter': filter,
               'searchbox_needed':'Yes',
               'page_size': 10,
               'first_item_number':first_item_number
               }
    return render(request, 'product_hunt/home.html', context)

def aboutPage(request):
    context = {'title': 'About'}
    return render(request, 'product_hunt/about.html', context)

def contactPage(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            # ------------------------- Mail for Admin -------------------------
            subject_for_admin = form.cleaned_data['subject']
            message_for_admin = 'Received an enquiry from : ' + form.cleaned_data['email'] +'\n' \
                               'Enquiry Message : ' + form.cleaned_data['message']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            # ------------------------- Mail for User -------------------------
            subject_for_user = form.cleaned_data['subject']
            message_for_user = 'Hi '+form.cleaned_data['email']+'. Warm welcome from ProductHunt support team.' \
                                'We have got your query and we will soon reply to you with proper answer.' \
                                'Thanks again for being such a fantastic customer! \n\nCheers!!!\n[from Admin]'
            admin_email = settings.EMAIL_HOST_USER
            user_recipient_list = [form.cleaned_data['email']]
            try:
                send_mail(subject_for_admin, message_for_admin, from_email, recipient_list)
                send_mail(subject_for_user, message_for_user, admin_email, user_recipient_list)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Mail has been sent successfully.')
            return redirect('home_page')
    return render(request, 'product_hunt/contact.html', {'form': form, 'title': 'Contact Us'})
