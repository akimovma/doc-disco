from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView

from users.helpers import is_author_or_clerk
from .models import Order
from .forms import CreateOrderForm
from .utils import prepare_orders_for_json


class CreateOrderView(UserPassesTestMixin, CreateView):
    template_name = 'create_order.html'
    form_class = CreateOrderForm
    model = Order
    redirect_field_name = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.is_customer

    def form_valid(self, form):
        order = form.save(commit=False)
        order.owner = self.request.user.customer_profile
        order.save()
        messages.success(self.request, 'Order {} was successfully added'.format(order.name))
        return redirect(reverse_lazy('dashboard'))


class OrderList(View):
    model = Order

    def get(self, request, status=None, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            orders = prepare_orders_for_json(user, status)
            return JsonResponse({'data': orders})
        return redirect(reverse_lazy('dashboard'))


class DetailOrderView(UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'detail_order.html'
    redirect_field_name = reverse_lazy('dashboard')

    def test_func(self):
        order = self.get_object()
        return is_author_or_clerk(self.request.user, order)
