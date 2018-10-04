from django.urls import path
from .views import (
    BudgetListView,
    TransactionDetailView,
    BudgetCreateView,
    TransactionCreateView,
)

urlpatterns = [
    path('budget', BudgetListView.as_view(), name='budget_view'),
    path('budget/new', BudgetCreateView.as_view(), name='budget_create'),
    path(
        'transaction/<int:id>',
        TransactionDetailView.as_view(),
        name='transaction_detail'
    ),
    path(
        'transaction/new',
        TransactionCreateView.as_view(),
        name="transaction_create"
    )
]
