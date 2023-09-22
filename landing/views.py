# Create your views here.
import json

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, FormView

from landing.forms import ContactUsForm
from landing.models import Location
from product.models import Product, Category


class IndexView(generic.ListView):
    """
    A view to show the index page
    """
    model = Category
    queryset = Category.objects.filter()
    template_name = 'landing/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Overriding this method to send products
        :param object_list:
        :param kwargs:
        :return:
        """
        kwargs['product_list'] = Product.objects.order_by('-create_datetime')[:4]
        return super().get_context_data(object_list=object_list, **kwargs)


class Custom404(TemplateView):
    """
    Handling 404 error
    """
    template_name = 'landing/404.html'


class ContactView(FormView):
    """
    A view for ContactUs page.
    """
    form_class = ContactUsForm
    success_url = reverse_lazy('landing:contact')
    template_name = 'contact.html'

    def form_valid(self, form):
        """
        If the form data is valid it will send an email.
        :param form:
        :return:
        """
        sender = form.cleaned_data['form_email']
        subject = form.cleaned_data['subject']
        content = form.cleaned_data['content']
        send_mail(subject, content, sender, ['django.m64@gmail.com', sender])
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        location_list = list(Location.objects.order_by('name').values())
        location_json = json.dumps(location_list)
        # print('sad',location_json)
        kwargs['locations'] = location_json
        return super().get_context_data(**kwargs)
