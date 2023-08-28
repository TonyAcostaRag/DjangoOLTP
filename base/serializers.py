from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User, Account, Card, Transaction


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        validated_data['user'] = user_data
        account = Account.objects.create(**validated_data)
        return account


class CardSerializer(ModelSerializer):

    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        validated_data['account'] = account_data
        card = Card.objects.create(**validated_data)
        return card


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['card_id', 'amount', 'transaction_type']
