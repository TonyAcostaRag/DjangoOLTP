from django.http import JsonResponse
from django.http import Http404
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
    data = ['/users',
            'users/:username',
            'users/<str:username>/accounts/',
            'users/<str:username>/accounts/<str:account_name>/cards/']
    return Response(data)


# USER instances


# CREATE READ
class UserList(APIView):

    def get(self, request):
        query = request.GET.get('query')
        if query == None:
            query = ''

        users = User.objects.filter(Q(username__icontains=query) | Q(age__icontains=query))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        user = self.get_object(username=username)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, username, pk=None):
        try:
            user = self.get_object(username=username)
            serializer = UserSerializer(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"Error": "User not found"})

    def patch(self, request, username):

        try:
            user = self.get_object(username=username)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            Response({"Error": "User not found"})

    def delete(self, request, username):
        user = self.get_object(username=username)
        user.delete()
        return Response({'message': 'User was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class AccountList(APIView):
    def get(self, request, username):

        try:
            user = User.objects.get(username=username)
            accounts = Account.objects.filter(user=user)
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error' : 'User not found'})

    def post(self, request, username):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(data={**request.data, 'user': user.id})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.data, status.HTTP_200_OK)


class CardList(APIView):

    def get(self, request, username, account_name):

        try:
            user = User.objects.get(username=username)
            account = Account.objects.get(user=user)
            cards = Card.objects.filter(account=account)

            serializer = CardSerializer(cards, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        except User.DoesNotExist:
            raise JsonResponse({'error': 'User does not exist'})
        except Account.DoesNotExist:
            raise JsonResponse({'error': 'Account does not exist'})
        except Card.DoesNotExist:
            raise JsonResponse({'error': 'Card does not exist'})

    def post(self, request, username, account_name):

        try:
            user = User.objects.get(username=username)
            account = Account.objects.get(user=user)
        except User.DoesNotExist:
            raise JsonResponse({'error': 'User does not exist'}, status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            raise JsonResponse({'error': 'Account does not exist'}, status.HTTP_404_NOT_FOUND)

        serializer = CardSerializer(data={**request.data, 'account': account.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


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
