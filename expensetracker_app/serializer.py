from rest_framework import serializers
from expensetracker_app.models import Expenses
from django.contrib.auth.models import User



class UserSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields="__all__"
        read_only_fields=["owner","id","created_at"]