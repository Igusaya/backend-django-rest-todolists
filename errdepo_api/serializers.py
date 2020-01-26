from errdepo_api.models import Card, Profile
from django.contrib.auth.models import User
from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    # 作成したユーザとの関連付け
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Card
        fields = ['id', 'name', 'position', 'color', 'created', 'owner']

class UserSerializer(serializers.ModelSerializer):
    errdepo_api = serializers.PrimaryKeyRelatedField(many=True, queryset=Card.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'errdepo_api']

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    last_login= serializers.ReadOnlyField(source='user.last_login')

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'username', 'email', 'last_login', 'image', 'description', 'modify']
