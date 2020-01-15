from todo_lists_api.models import Card
from todo_lists_api.serializers import CardSerializer, UserSerializer
from todo_lists_api.permissions import IsOwnerOrReadOnly, IsOwner

from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics


class CardList(APIView):
    """
    List all Card, or create a new card.
    """
    # IsAuthenticatedOrReadOnly: 認証済：読み取り/書き込みOK　未認証：読み取りOnly
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        print('###########' + request.method)
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
