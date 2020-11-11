from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from myshop.forms import RegisterForm, OrderForm, ItemCreateForm, RefundForm
from myshop.models import UserProfile, Item, Order, Refund


class Register(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': RegisterForm()}
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            userprofile = form.save(commit=False)
            userprofile.funds = 1000.00
            userprofile.save()
            credentials = form.cleaned_data
            userprofile = authenticate(username=credentials['username'],
                                       password=credentials['password1'])
            login(self.request, userprofile)
            return HttpResponseRedirect(reverse_lazy('profile'))
        return render(request, 'register.html', {'form': form})


class Login(LoginView):
    template_name = 'login.html'
    model = UserProfile
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        credentials = form.cleaned_data
        userprofile = authenticate(username=credentials['username'],
                                   password=credentials['password'])
        if userprofile is not None:
            login(self.request, userprofile)
            return HttpResponseRedirect(self.success_url)

        else:
            return HttpResponseRedirect(reverse_lazy('login'))


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'
    next_page = '/'
    redirect_field_name = 'next'


class Main(ListView):
    template_name = 'main.html'
    model = Item
    context_object_name = 'items'
    queryset = Item.objects.all()[:3]


class Success(TemplateView):
    template_name = 'success.html'


class ItemListView(ListView):
    template_name = 'productlistview.html'
    model = Item
    context_object_name = 'items'
    paginate_by = 10


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm()
        return context


class CreateOrder(CreateView, SingleObjectMixin):
    template_name = 'product_detail.html'
    model = Order
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            data = form.cleaned_data
            order.user_id = self.request.user.id
            order.item_id = kwargs['pk']
            order.amount = int(data['amount'])
            user_obj = UserProfile.objects.get(id=self.request.user.id)
            item_obj = Item.objects.get(id=kwargs['pk'])

            if item_obj.quantity >= order.amount:
                if user_obj.funds >= user_obj.funds - order.get_total_item_price():
                    user_obj.funds = round(user_obj.funds - order.get_total_item_price(), 2)
                    item_obj.quantity = item_obj.quantity - data['amount']
                    order.save()
                    user_obj.save()
                    item_obj.save()
                    return HttpResponseRedirect(reverse_lazy('profile'))
                else:
                    messages.error(self.request, 'Not enough funds.')
                    return HttpResponseRedirect(reverse_lazy('profile'))
            else:
                messages.error(self.request, 'Out of stock :(')
                return HttpResponseRedirect(reverse_lazy('profile'))
        return render(request, 'product_detail.html', {'form': form})

    def get_success_url(self):
        return reverse('item_detail', kwargs={'pk': self.object.pk})


class CombinedView(View):

    def get(self, request, *args, **kwargs):
        view = ItemDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CreateOrder.as_view()
        return view(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'profile.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'refund_form': RefundForm})
        return context


class SuperUserView(PermissionRequiredMixin, ListView):
    permission_required = 'user.delete_user'
    model = Item
    paginate_by = 10
    template_name = 'superedit.html'
    queryset = Item.objects.all()
    context_object_name = 'items'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'create_form': ItemCreateForm})
        return context


class ItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'user.delete_user'
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('super')
    http_method_names = ['post', ]

    def form_valid(self, form):
        obj = form.save(commit=False)
        self.object = obj.save()
        return super().form_valid(form)


class ItemUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'user.delete_user'
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('super')
    http_method_names = ['post', 'get']
    template_name = 'product_update.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        self.object = obj.save()
        return super().form_valid(form)


class CreateRefund(LoginRequiredMixin, CreateView):
    form_class = RefundForm
    model = Refund
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        refund = form.save(commit=False)
        order_id = self.request.POST.get('order.id')
        order = Order.objects.get(id=order_id)
        refund.purchase = order
        order_time = refund.purchase.created_at
        now = timezone.now()
        if now < order_time + timedelta(minutes=3):
            refund.refund_requested = True
            refund.save()
            messages.success(self.request, 'Successful')
            return super().form_valid(form=form)
        else:
            messages.error(self.request, 'No longer in grace period')
            return HttpResponseRedirect(self.success_url)


class RefundView(PermissionRequiredMixin, ListView):
    permission_required = 'user.delete_user'
    model = Refund
    paginate_by = 10
    template_name = 'refund_list.html'
    queryset = Refund.objects.all()
    context_object_name = 'refunds'


class RefundManage(PermissionRequiredMixin, DeleteView):
    permission_required = 'user.delete_user'
    model = Refund
    success_url = reverse_lazy('manage_refunds')

    def delete(self, request, *args, **kwargs):
        refund = self.get_object()
        print(self.request.POST)
        if self.request.POST['action'] == 'approve':
            order = refund.purchase
            user = order.user
            user.funds += order.get_total_item_price()
            item = order.item
            item.quantity += order.amount
            user.save()
            item.save()
            order.delete()

        refund.delete()
        return HttpResponseRedirect(self.success_url)
