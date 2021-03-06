from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from errdepo_api import views
from django.conf.urls import include

urlpatterns = [
        path('cards/', views.CardList.as_view()),
        path('cards/<int:pk>/', views.CardDetail.as_view()),
        path('users/', views.UserList.as_view()),
        path('users/<int:pk>/', views.UserDetail.as_view()),
        path('profile/', views.ProfileDetail.as_view()),
        path('lang/', views.Lang.as_view()),
        path('confirmreport/', views.ConfirmReport.as_view()),
        path('report/', views.ReportList.as_view()),
        path('report/<int:pk>/', views.ReportDetail.as_view()),
        path('fw/', views.FwView.as_view()),
        path('exists_values/', views.ExistsValue.as_view()),
        path('search_reports/', views.SearchReports.as_view()),
]

urlpatterns += [
        # ブラウザビューにログインを表示
        path('api-auth/', include('rest_framework.urls')),
        path('api/v1/rest-auth/', include('rest_auth.urls')),
        path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
