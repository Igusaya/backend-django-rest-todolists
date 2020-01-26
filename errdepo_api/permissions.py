from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission(権限) オブジェクトの所有者のみに編集を許可する
    """

    def has_object_permission(self, request, view, obj):
        # 読取り許可は全てのリクエストに対して許可する
        # そのため、GET、HEAD、OPTIONSリクエストは常に許可する
        if request.method in permissions.SAFE_METHODS:
            return True

        # 書込み許可はオブジェクトの所有者のみに許可する
        return obj.owner == request.user

class IsOwner(permissions.BasePermission):
    """
    オブジェクト所有者のみに閲覧・編集を許可する
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
