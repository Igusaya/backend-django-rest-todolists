from errdepo_api.models import Card, Profile, Fw, Report
from errdepo_api.serializers import CardSerializer, UserSerializer, ProfileSerializer, FwSerializer, ReportSerializer
from errdepo_api.permissions import IsOwnerOrReadOnly, IsOwner
from errdepo_api.util import toMD

from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Count, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

import base64
import numpy as np
import cv2
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

import markdown
import re

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
        """
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

class FwView(APIView):
    """
    本来getだが、パラメーターに禁則文字(javascript等)があるため、
    postで取得処理を行う
    """
    permission_classes = [permissions.AllowAny]

    def post(self,request, format=None):
        lang = request.data['lang']
        fw = Fw.objects.filter(lang=request.data['lang'])
        serializer = FwSerializer(fw, many=True)
        return Response(serializer.data)


class ConfirmReport(APIView):
    """
    """
    permission_classes = [permissions.AllowAny]

    def post(self,request, format=None):
        # パラメーターの取り出し
        description = request.data['description']
        correspondence = request.data['correspondence']
        lang = request.data['lang']
        
        return Response({'description':toMD(description, lang), 'correspondence':toMD(correspondence, lang)})


#class ReportList(APIView):
class ReportList(generics.ListAPIView):
    """
    全てのReportを取得、もしくは新しいReportを作成する。
    Postは認証済ユーザのみ許可
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def post(self, request, format=None):
        """
        Post {baseURL}/report
        fwTBLにrequest.fwが存在しない場合はinsertした後にreportTBLへinsertする
        """
        fw_count = Fw.objects.filter(lang=request.data['lang'], fw=request.data['fw']).count()
        if fw_count == 0 and request.data['fw'] != '' :
            fw_serializer = FwSerializer(data={'lang':request.data['lang'],'fw':request.data['fw']})
            if fw_serializer.is_valid():
                fw_serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ReportDetail(APIView):
    """
    Reportインスタンスを取得、更新、削除する。
    Get以外はownerのみ許可
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, formata=None):
        report = self.get_object(pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExistsValue(APIView):
    """
    検索の為に登録されている作成者とlangを取得
    getのみ
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        query = Report.objects.values('lang','owner','owner_id')
        #　配列化
        l_lang = [d.get('lang') for d in query]
        l_owner = [d.get('owner') for d in query]
        # 重複削除
        l_lang = list(set(l_lang))
        l_owner = list(set(l_owner))
        # owner名取得
        q_user = User.objects.filter(id__in=l_owner)
        l_creater = [o.username for o in q_user]
        return Response({'langList':l_lang, 'createrList':l_creater})

class SearchReports(APIView):
    """
    reportの検索を行う
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        l_word = request.data['inputWord']
        l_lang = request.data['inputLang']
        l_fw = request.data['inputFw']
        l_creater = request.data['inputCreater']
        if len(l_creater) > 0:
            l_user_id = []
            for creater in l_creater:
                l_user_id.append(User.objects.filter(username=creater)[0].id)

        report = Report.objects
        # Option(creater, fw, lang) search
        if len(l_creater) > 0:
            report = report.filter(owner_id__in=l_user_id)
        if len(l_fw) > 0:
            report = report.filter(fw__in=l_fw)
        if len(l_lang) > 0:
            report = report.filter(lang__in=l_lang)

        # word like search
        for word in l_word:
            report = report.filter(
                Q(errmsg__icontains=word) |
                Q(description__icontains=word) |
                Q(correspondence__icontains=word))

        serializer = ReportSerializer(report, many=True)
        return Response({'count':report.count(), 'next':'2', 'previous':'', 'results':serializer.data})
    