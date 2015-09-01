try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import SingleChargeFormView, ProductPurchaseListView, ProductPurchaseDetailView, ProductCreateView

urlpatterns = [
    url(r'^$', SingleChargeFormView.as_view(), name='single_charge'),
    url(r'^purchases/$', ProductPurchaseListView.as_view(), name='purchase_list'),
    url(r'^purchases/(?P<slug>[\d\w]+)/$', ProductPurchaseDetailView.as_view(), name='purchase_detail'),
    url(r'^products/create/$', ProductCreateView.as_view(), name='product_create'),
    ]
