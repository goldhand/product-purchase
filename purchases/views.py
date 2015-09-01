from django.views.generic import FormView
from django.views.generic import ListView, DetailView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from braces.views import FormValidMessageMixin, LoginRequiredMixin

from djstripe.mixins import SubscriptionMixin
from djstripe.models import Customer
from djstripe.settings import subscriber_request_callback
import stripe

from .forms import ChargeForm
from .models import ProductPurchase, Product


class SingleChargeFormView(LoginRequiredMixin, FormValidMessageMixin, SubscriptionMixin, FormView):
    """TODO: Add stripe_token to the form and use form_valid() instead of post()."""

    form_class = ChargeForm
    template_name = "pages/purchase.html"
    success_url = reverse_lazy("charges:purchase_list")
    form_valid_message = "You successfully purchased this!"

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            try:
                customer, created = Customer.get_or_create(
                    subscriber=subscriber_request_callback(self.request))
                customer.update_card(self.request.POST.get("stripe_token"))
                product = Product.objects.get(id=form.cleaned_data['product'])
                charge = customer.charge(product.price, send_receipt=False)  # don't send reciept until product purhcase is created
                # create a product_purchase model that is associated with the charge
                ProductPurchase.objects.create(charge=charge,
                                               product=product,
                                               downloads=product.downloads)
                # send reciept now that product pruchase is created
                charge.send_receipt()

            except stripe.StripeError as exc:
                form.add_error(None, str(exc))
                return self.form_invalid(form)
            # redirect to confirmation page
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(SingleChargeFormView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductPurchaseListView(ListView):
    '''
    List purchases
    '''
    model = ProductPurchase


class ProductPurchaseDetailView(DetailView):
    '''
    Returns an object resource and decrements the downloads counter
    '''
    model = ProductPurchase
    slug_field = 'key'

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        if obj.product.resource and obj.downloads > 0:
            # if the product has a downloadable resource then render it and decrease download counter
            pdf = open(obj.product.resource.path, 'r')
            response = HttpResponse(pdf.read(), content_type='text/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(obj.product.name)
            obj.decrement_downloads()
            return response
        if obj.downloads == 0:
            messages.error(self.request,
                           'You have run out of downloads for {name}. \
                           Purchase {name} again to download more.'
                           .format(name=obj.product.name))
            return HttpResponseRedirect(reverse_lazy('charges:single_charge'))
        return super(ProductPurchaseDetailView,
                     self).render_to_response(context, **response_kwargs)


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'resource', 'downloads']
    success_url = reverse_lazy('charges:single_charge')