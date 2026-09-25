from django.shortcuts import render
from expensetracker_app.serializer import UserSerializer,ExpensesSerializer
from expensetracker_app.models import Expenses
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone


# Create your views here.


class SignUpViewset(ViewSet):
    def create(self,request):
        dser=UserSerializer(data=request.data)
        if dser.is_valid():
            User.objects.create_user(**dser.validated_data)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)



class ExpenseView(ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        dser=ExpensesSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        exp=Expenses.objects.filter(owner=request.user)
        ser=ExpensesSerializer(exp,many=True)
        return Response(data=ser.data,status=status.HTTP_200_OK)

    def destroy(self,request,pk=0):
        Expenses.objects.get(id=pk).delete()
        return Response(data={"msg":"deleted!!"})


    def update(self,request,pk=0):
        exp=Expenses.objects.get(id=pk)
        dser=ExpensesSerializer(data=request.data,instance=exp,)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self,request,pk=0):
        exp=Expenses.objects.get(id=pk)
        dser=ExpensesSerializer(data=request.data,instance=exp,partial=True)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

# class ExpenseSummaryView(APIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
#         cur_date=timezone.now()
#         # print(cur_date)
#         cur_month=cur_date.month
#         cur_year=cur_date.year
#         print(cur_month,cur_year)
#         data=Expenses.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
#         # qs=data.values('category').annotate(Sum('amount'))
#         category_summary=data.values('category').annotate(Sum('amount'))
#         cat_summary=[summary for summary in category_summary]
#         for i in category_summary:
#             print(i)
#         # for i in qs:
#         #     print(i)
#         # # ser=ExpensesSerializer(qs,many=True)
#         return Response(data={"msg":"Summary"})



class ExpenseSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur_date=timezone.now()
        print(cur_date)
        cur_month=cur_date.month
        print(cur_month)
        cur_year=cur_date.year
        print(cur_month,cur_year)
        expense=Expenses.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        summery=expense.values('amount').aggregate(Sum('amount'))
        summery_data=expense.values('category').annotate(Sum('amount'))
    

        return Response(data={"category":summery_data,"total":summery})



    
    
        
