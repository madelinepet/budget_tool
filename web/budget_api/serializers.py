from django.contrib.auth.models import User
from rest_framework import serializers
from budgets.models import Budget, Transaction


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = super().create({
            'username': validated_data['username'],
            'email': validated_data['email'],
            'firstname': validated_data['firstname'],
            'lastname': validated_data['lastname'],
        })

        user.set_password(validated_data['password'])
        user.save()
        return user


# Custom
class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )

    class Meta:
        model = Budget
        fields = ('id', 'owner', 'name', 'description', 'user')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    transaction = serializers.HyperlinkedRelatedField(
        view_name='budget_api',
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = (
            'id',
            'assigned_to',
            'budget',
            'title',
            'description',
            'status'
        )
