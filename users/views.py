from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, RedirectView, TemplateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group

from orders.models import Order
from .tokens import account_activation_token
from .forms import CustomerRegistrationForm, CreateClerkForm
from .models import User, CustomerProfile, ClerkProfile
from .tasks import verification_email_send


class CustomerRegistrationView(FormView):
    success_url = reverse_lazy('users:profile_dashboard')
    form_class = CustomerRegistrationForm
    template_name = 'registration/register.html'
    message_success = ("To use your account on Doc Disco, "
                       "you need to confirm the email address. Please check your mailbox.")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        customer_group = Group.objects.get(name='Customers')
        user.save(group_pk=customer_group.pk)
        profile_data = form.cleaned_data.get('profile')
        CustomerProfile.objects.filter(pk=user.customer_profile.pk).update(**profile_data)
        verification_email_send.delay(user.pk)
        messages.success(self.request, self.message_success)
        return redirect(self.get_success_url())


class CustomerEmailVerificationView(RedirectView):
    def get(self, request, uid, token, *args, **kwargs):
        try:
            uid_pk = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse_lazy('dashboard'))


class UserProfileDashboard(TemplateView):
    template_name = 'user_dashboard.html'


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['table_label'] = 'Orders List'
        if self.request.user.is_customer:
            ctx['url_for_ajax'] = reverse_lazy('orders:list')
            ctx['is_clerk'] = False
        else:
            orders_status = self.request.GET.get('status', Order.TO_FILL)
            try:
                orders_status_str = Order.STATUSES[int(orders_status)][1]
            except (IndexError, ValueError):
                orders_status = 0
                orders_status_str = Order.STATUSES[orders_status][1]
            table_label = 'Orders {}'.format(orders_status_str)
            url = reverse_lazy('orders:list', kwargs={'status': orders_status})
            ctx['url_for_ajax'] = url
            ctx['is_clerk'] = True
            ctx['table_label'] = table_label
        return ctx


class CreateClerkView(UserPassesTestMixin, FormView):
    template_name = 'create_clerk.html'
    form_class = CreateClerkForm
    success_url = reverse_lazy('dashboard')
    message_success = "Clerk account successfully created."
    redirect_field_name = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.is_head_clerk

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        clerks_group = Group.objects.get(name='Clerks')
        user.save(group_pk=clerks_group.pk)
        user.set_password(form.cleaned_data.get('password'))
        profile_data = form.cleaned_data.get('profile')
        ClerkProfile.objects.filter(pk=user.clerk_profile.pk).update(**profile_data)
        messages.success(self.request, self.message_success)
        return redirect(self.get_success_url())


class ClerkListView(UserPassesTestMixin, ListView):
    model = ClerkProfile
    template_name = 'clerks_list.html'
    context_object_name = 'clerks'
    redirect_field_name = reverse_lazy('dashboard')
    paginate_by = 10
    queryset = ClerkProfile.objects.order_by('user__email')

    def test_func(self):
        return self.request.user.is_head_clerk


@user_passes_test(lambda u: u.is_head_clerk)
def ban_clerk_account(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_active = False
    user.remove_sessions()
    messages.success(request, 'Account blocked!')
    user.save()
    return redirect(reverse_lazy('users:clerk_list'))


@user_passes_test(lambda u: u.is_head_clerk)
def restore_clerk_account(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_active = True
    messages.success(request, 'Account restored!')
    user.save()
    return redirect(reverse_lazy('users:clerk_list'))
