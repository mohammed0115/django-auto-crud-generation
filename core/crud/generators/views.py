from textwrap import dedent


def generate_views(facade):
    model = facade.model_class_name
    model_lower = facade.model_name

    return dedent(f"""
    from rest_framework.permissions import IsAuthenticated
    from core.crud.base import (
        BaseListAPIView, BaseCreateAPIView, BaseRetrieveAPIView,
        BaseUpdateAPIView, BaseDeleteAPIView,
        BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
    )
    from {facade.app_name}.models import {model}
    from .serializers import {model}Serializer
    from .forms import {model}Form
    from django.urls import reverse_lazy


    # ---------------- API Views ----------------

    class {model}ListAPI(BaseListAPIView):
        queryset = {model}.objects.all()
        serializer_class = {model}Serializer
        permission_classes = [IsAuthenticated]
        search_fields = "__all__"
        filterset_fields = "__all__"


    class {model}CreateAPI(BaseCreateAPIView):
        queryset = {model}.objects.all()
        serializer_class = {model}Serializer
        permission_classes = [IsAuthenticated]


    class {model}RetrieveAPI(BaseRetrieveAPIView):
        queryset = {model}.objects.all()
        serializer_class = {model}Serializer
        permission_classes = [IsAuthenticated]


    class {model}UpdateAPI(BaseUpdateAPIView):
        queryset = {model}.objects.all()
        serializer_class = {model}Serializer
        permission_classes = [IsAuthenticated]


    class {model}DeleteAPI(BaseDeleteAPIView):
        queryset = {model}.objects.all()
        serializer_class = {model}Serializer
        permission_classes = [IsAuthenticated]


    # ---------------- Web Views ----------------

    class {model}ListView(BaseListView):
        model = {model}
        template_name = "{facade.app_name}/{model_lower}/list.html"
        context_object_name = "objects"
        paginate_by = 10


    class {model}CreateView(BaseCreateView):
        model = {model}
        form_class = {model}Form
        template_name = "{facade.app_name}/{model_lower}/form.html"
        success_url = reverse_lazy("{model_lower}_list")


    class {model}UpdateView(BaseUpdateView):
        model = {model}
        form_class = {model}Form
        template_name = "{facade.app_name}/{model_lower}/form.html"
        success_url = reverse_lazy("{model_lower}_list")


    class {model}DeleteView(BaseDeleteView):
        model = {model}
        template_name = "{facade.app_name}/{model_lower}/confirm_delete.html"
        success_url = reverse_lazy("{model_lower}_list")
    """)
