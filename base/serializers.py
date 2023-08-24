from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User, Account, Card


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'age']


class AccountSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ['id', 'user', 'account_name', 'balance', 'open_date']

    def create(self, validated_data):
        print(f'\n-------> Account Serializer validated_data: {validated_data}')
        user_data = validated_data.pop('user')
        print(f'\n-------> Account Serializer user_data: {user_data}')
        #user_serializer = UserSerializer(data=user_data)  # Create a UserSerializer instance
        #print(f'\n-------> Account Serializer user_serializer: {user_serializer}')
        #user_serializer.is_valid(raise_exception=True)
        user = user_data.save()  # Save the user instance



        account = Account.objects.create(user=user)
        return account


class CardSerializer(ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Card
        fields = ['id', 'account', 'name', 'cvv']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        #account_serializer = AccountSerializer(data=account_data)  # Create a UserSerializer instance
        #account_serializer.is_valid(raise_exception=True)
        #account = account_serializer.save()  # Save the user instance

        card = Card.objects.create(account=account_data, **validated_data)
        return card
