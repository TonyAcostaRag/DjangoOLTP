from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User, Account, Card, Transaction


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AccountSerializer(ModelSerializer):
    #user = UserSerializer()

    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        print(f'\n-------> Account Serializer validated_data: {validated_data}')
        user_data = validated_data.pop('user')
        print(f'\n-------> Account Serializer user_data: {user_data}')
        validated_data['user'] = user_data
        print(f'\n-------> Account Serializer validated_data: {validated_data}')
        account = Account.objects.create(**validated_data)
        print("Returning account")
        return account


class CardSerializer(ModelSerializer):
    #account = AccountSerializer()

    class Meta:
        model = Card
        fields = "__all__"

    """
    def create(self, validated_data):
        account_data = validated_data.pop('account')
        #account_serializer = AccountSerializer(data=account_data)  # Create a UserSerializer instance
        #account_serializer.is_valid(raise_exception=True)
        #account = account_serializer.save()  # Save the user instance

        card = Card.objects.create(account=account_data, **validated_data)
        return card
    """


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        field = "__all__"
