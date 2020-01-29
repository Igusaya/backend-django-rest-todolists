from errdepo_api.models import Card, Profile, Fw, Report
from django.contrib.auth.models import User
from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    # 作成したユーザとの関連付け
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Card
        fields = ['id', 'name', 'position', 'color', 'created', 'owner']

class UserSerializer(serializers.ModelSerializer):
    #errdepo_api = serializers.PrimaryKeyRelatedField(many=True, queryset=Card.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'report_owner']

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    last_login= serializers.ReadOnlyField(source='user.last_login')
    #report_owner= serializers.ReadOnlyField(source='user.report_owner')

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'username', 'email', 'last_login', 'image', 'description', 'modify']

class FwSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fw
        fields = ['lang', 'fw']

class ReportSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Report
        fields =['id', 'created', 'modify', 'lang', 'fw', 'env', 'errmsg', 'description', 'correspondence', 'owner_id','owner']