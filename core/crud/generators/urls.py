from textwrap import dedent


def generate_urls(facade):
    model = facade.model_class_name
    model_lower = facade.model_name

    return dedent(f"""
    from django.urls import path
    from .views import (
        {model}ListAPI, {model}CreateAPI, {model}RetrieveAPI,
        {model}UpdateAPI, {model}DeleteAPI,
        {model}ListView, {model}CreateView,
        {model}UpdateView, {model}DeleteView
    )

    urlpatterns = [
        # API
        path("api/{model_lower}/", {model}ListAPI.as_view(), name="{model_lower}_api_list"),
        path("api/{model_lower}/create/", {model}CreateAPI.as_view(), name="{model_lower}_api_create"),
        path("api/{model_lower}/<int:pk>/", {model}RetrieveAPI.as_view(), name="{model_lower}_api_detail"),
        path("api/{model_lower}/<int:pk>/update/", {model}UpdateAPI.as_view(), name="{model_lower}_api_update"),
        path("api/{model_lower}/<int:pk>/delete/", {model}DeleteAPI.as_view(), name="{model_lower}_api_delete"),

        # Web
        path("{model_lower}/", {model}ListView.as_view(), name="{model_lower}_list"),
        path("{model_lower}/create/", {model}CreateView.as_view(), name="{model_lower}_create"),
        path("{model_lower}/<int:pk>/update/", {model}UpdateView.as_view(), name="{model_lower}_update"),
        path("{model_lower}/<int:pk>/delete/", {model}DeleteView.as_view(), name="{model_lower}_delete"),
    ]
    """)
