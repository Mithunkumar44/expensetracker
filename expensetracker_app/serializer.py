from rest_framework import serializers
from expensetracker_app.models import Expenses
from django.contrib.auth.models import User



class UserSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()


class ExpensesSerializer(serializers.ModelSerializer):
    # owner=serializers.StringRelatedField(read_only=True)
    #SerializerMethodField
    # greeting=serializers.SerializerMethodField()
    owner=serializers.SerializerMethodField()

    class Meta:
        model=Expenses
        fields="__all__"
        read_only_fields=["id","created_at","owner"]

    def get_greeting(self,obj):
         return "Hi, Welcome to Expense Tracker !!"
        
    def get_owner(self,obj):
        return obj.owner.username