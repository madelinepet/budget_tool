from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Budget, Transaction
from .forms import BudgetForm, TransactionForm


class BudgetListView(LoginRequiredMixin, ListView):
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(
            budget__user__username=self.request.user.username)
        return context

    def get_queryset(self):
        return Budget.objects.filter(
            user__username=self.request.user.username)


class TransactionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'budgets/transaction_detail.html'
    context_object_name = 'transaction'
    login_url = reverse_lazy('login')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Transaction.objects.filter(
            budget__user__username=self.request.user.username)


class BudgetCreateView(LoginRequiredMixin, CreateView):
    template_name = 'budgets/budget_create.html'
    model = Budget
    form_class = BudgetForm
    success_url = reverse_lazy('budget_view')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """ Attatch a user
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'budgets/transaction_create.html'
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('budget_view')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """ Attatch a user
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
