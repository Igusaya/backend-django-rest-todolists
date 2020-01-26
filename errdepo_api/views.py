from errdepo_api.models import Card, Profile
from errdepo_api.serializers import CardSerializer, UserSerializer, ProfileSerializer 
from errdepo_api.permissions import IsOwnerOrReadOnly, IsOwner

from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics

import base64
import numpy as np
import cv2
from pygments.lexers import get_all_lexers

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[0]) for item in LEXERS])


class CardList(APIView):
    """
    List all Card, or create a new card.
    """
    # IsAuthenticatedOrReadOnly: 認証済：読み取り/書き込みOK　未認証：読み取りOnly
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        card = Card.objects.filter(owner=self.request.user)
        serializer = CardSerializer(card, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """
        作成したユーザをカードインスタンスに関連付けする
        """
        serializer.save(owner=self.request.user)


class CardDetail(APIView):
    """
    Retrieve, update or delete a card instance.
    """
    # IsAuthenticatedOrReadOnly: 認証済：読み取り/書き込みOK　未認証：読み取りOnly
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_object(self, pk):
        try:
            return Card.objects.filter(owner=self.request.user).get(pk=pk)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        card = self.get_object(pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        card = self.get_object(pk)
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        card = self.get_object(pk)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileDetail(APIView):
    """
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        profile = Profile.objects.filter(user=self.request.user)
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)


    def put(self, request, format=None):
        """
        データURIスキーマを画像に変換し、保存を行う。
        対象の画像のパスはDB登録する
        """
        #data:image/png;base64,iVBOR
        data_uri_scheme = request.data['image']
        # 拡張子を取得
        extension = data_uri_scheme[data_uri_scheme.find('/')+1:data_uri_scheme.find(';')]
        # base64エンコーディングされた文字列を取得
        img_base64 = data_uri_scheme[data_uri_scheme.find(',')+1:]
        # 保存先を作成
        reg_pass = 'image/profIcon/'+ str(request.data['id']) + '.' + extension

        # base64でエンコードされたデータをバイナリデータに,バイナリデータを画像に変換
        img_binary = base64.urlsafe_b64decode(img_base64 + '=' * (-len(img_base64) % 4))
        img=np.frombuffer(img_binary,dtype=np.uint8)

        # 画像を圧縮し、保存
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        cv2.imwrite(reg_pass, img)

        # リクエストデータの書き換え
        request.data['image'] = '/image/profIcon/' + str(request.data['id']) + '.' + extension

        profile = Profile.objects.filter(user=self.request.user).first()
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Lang(APIView):
    """
    言語の配列を返す
    """
    permission_classes = [permissions.AllowAny]

    def get(self,request, format=None):
        return Response({'langArray':LANGUAGE_CHOICES})