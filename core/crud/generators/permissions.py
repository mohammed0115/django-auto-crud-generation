from textwrap import dedent


def generate_permissions(facade):
    model = facade.model_class_name

    return dedent(f"""
    from rest_framework.permissions import BasePermission


    class CanView{model}(BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm("{facade.app_name}.view_{facade.model_name}")


    class CanAdd{model}(BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm("{facade.app_name}.add_{facade.model_name}")


    class CanChange{model}(BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm("{facade.app_name}.change_{facade.model_name}")


    class CanDelete{model}(BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm("{facade.app_name}.delete_{facade.model_name}")
    """)
