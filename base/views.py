from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import User, Account, Card
from .serializers import UserSerializer, AccountSerializer, CardSerializer

from django.db.models import Q


# Create your views here.
@api_view(['GET'])
def endpoints(request):
    data = ['/users', 'users/:username', 'users/<str:username>/accounts/<str:account_name>/cards/']
    return Response(data)


# READ
@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query == None:
            query = ''

        print(f'\nprinting request parameter: {request}')

        print(f'\nQuery: -->{query}<--')
        users = User.objects.filter(Q(username__icontains=query) | Q(age__icontains=query))
        print(f'\nList of the users: {list(users)}')
        serializer = UserSerializer(users, many=True)
        print(f'\nUserSerializer: {serializer}')
        print(f'\nResponse: {Response(serializer.data)}')
        return Response(serializer.data)

    if request.method == 'POST':
        print(f'\nprinting request parameter: {request}')
        serializer = UserSerializer(data=request.data)
        print(f'\nUserSerializer: {serializer}')

        if serializer.is_valid():
            serializer.save()
            print(f'\nResponse: {Response(serializer.data, status=status.HTTP_201_CREATED)}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""

This is a intended comment to be between the user list and user detail. 

"""

class UserDetail(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise JsonResponse('User does not exist')

    def get(self, request, username):
        user = self.get_object(username=username)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def delete(self, request, username):
        user = self.get_object(username=username)
        user.delete()
        return JsonResponse({'message': 'User was successfully deleted'})


@api_view(['GET', 'POST'])
def account_list(request, username):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query == None:
            query = ''

        print(f'Query: {query}')

        try:
            user = User.objects.get(username=username)

            accounts = Account.objects.filter(user=user)
            accounts_data = [
                {'id': account.id,
                 'user': account.user,
                 'account_name': account.account_name,
                 'balance': account.balance,
                 'open_date': account.open_date.strftime('%Y-%m-%d')} for account in accounts]
            serializer = AccountSerializer(accounts_data, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

    if request.method == 'POST':

        print(f'\n-------> Account Serializer serializer input: {AccountSerializer(data=request.data)}')
        serializer = AccountSerializer(data=request.data)
        print(f'\n-------> Account Serializer serializer output: {serializer}')


        if serializer.is_valid():
            serializer.save()
            print(f'\n{Response(serializer.data, status=status.HTTP_201_CREATED)}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    def get_object(self, username, account_name):
        try:
            user = User.objects.get(username=username)
            return Account.objects.get(user=user, account_name=account_name)
        except Account.DoesNotExist:
            raise JsonResponse({'error': 'Account does not exist'})

    def get(self, request, username, account_name):
        account = self.get_object(username=username, account_name=account_name)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def card_list(request, username, account_name):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query is None:
            query = ''

        try:
            account = Account.objects.get(user__username=username, account_name=account_name)
            cards = Card.objects.filter(account=account)
            serializer = CardSerializer(cards, many=True)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found.'}, status=404)

    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetail(APIView):
    def get_object(self, user_account, card_name):
        try:
            account = Account.objects.get(user__username=user_account)
            return Card.objects.get(account=account, name=card_name)
        except Card.DoesNotExist:
            raise JsonResponse({'error': 'Card does not exist'})

    def get(self, request, user_account, card_name):
        card = self.get_object(user_account=user_account, card_name=card_name)
        serializer = CardSerializer(card)
        return Response(serializer.data)
