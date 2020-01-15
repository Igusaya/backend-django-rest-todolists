from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from todo_lists_api import views
from django.conf.urls import include

urlpatterns = [
        path('cards/', views.CardList.as_view()),
        path('cards/<int:pk>/', views.CardDetail.as_view()),
        path('users/', views.UserList.as_view()),
        path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns += [
        # ブラウザビューにログインを表示
        path('api-auth/', include('rest_framework.urls')),
        path('api/v1/rest-auth/', include('rest_auth.urls')),
        path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
