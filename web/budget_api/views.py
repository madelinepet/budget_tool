from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import (
    UserSerializer,
    User,
    Budget,
    Transaction,
    BudgetSerializer,
    TransactionSerializer,
)


class RegisterApiView(generics.CreateAPIView):
    """ View from django REST API that allows us to have a registration view
    """
    permission_classes = ''
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer


class UserApiView(generics.RetrieveAPIView):
    """ A class from Django REST API that gives us a user view
    """
    permission_classes = ''
    serializer_class = UserSerializer

    def get_queryset(self):
        """ returns the filtered queryset for the UserApiView
        """
        return User.objects.filter(id=self.kwargs['pk'])


class BudgetListApiView(generics.ListCreateAPIView):
    """ Custom class for listing all budgets
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = BudgetSerializer

    def get_queryset(self):
        """ Filter categories by user
        """
        return Budget.objects.filter(
            user__username=self.request.user.username
        )

    def perform_create(self, serializer):
        """ Saves the serializer with the user on it
        """
        serializer.save(user_id=self.request.user.id)


class BudgetDetailApiView(generics.RetrieveAPIView):
    """ init time occurances for listing budget detail view on a particular budget
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = BudgetSerializer

    def get_queryset(self):
        """ Happens at runtime, filteres the Budget to only those from that user
        """
        return Budget.objects.filter(
            budget__user__username=self.request.user.username)


class TransactionListApiView(generics.ListCreateAPIView):
    """ Gives a list of all transactions
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """ Returns transactions filtered to that specific user and their category the transaction belongs to
        """
        return Transaction.objects.filter(
            budget__user__username=self.request.user.username
        )


class TransactionDetailApiView(generics.RetrieveAPIView):
    """ Detail view for transactions belonging to budgets for a particular user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """ Filters transactions based on user and budget
        """
        return Transaction.objects.filter(
            budget__user__username=self.request.user.username
        )
