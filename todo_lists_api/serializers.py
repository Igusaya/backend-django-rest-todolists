from todo_lists_api.models import Card
from django.contrib.auth.models import User
from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    # 作成したユーザとの関連付け
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Card
        fields = ['id', 'name', 'position', 'color', 'created', 'owner']

class UserSerializer(serializers.ModelSerializer):
    PourmeeAPI = serializers.PrimaryKeyRelatedField(many=True, queryset=Card.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'PourmeeAPI']
