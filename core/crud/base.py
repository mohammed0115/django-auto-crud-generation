from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class BaseAPIView:
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = "__all__"
    filterset_fields = "__all__"


class BaseListAPIView(BaseAPIView, generics.ListAPIView):
    pass


class BaseCreateAPIView(generics.CreateAPIView):
    pass


class BaseRetrieveAPIView(generics.RetrieveAPIView):
    pass


class BaseUpdateAPIView(generics.UpdateAPIView):
    pass


class BaseDeleteAPIView(generics.DestroyAPIView):
    pass


# -------- Web Views --------

class BaseListView(ListView):
    paginate_by = 10


class BaseCreateView(CreateView):
    pass


class BaseUpdateView(UpdateView):
    pass


class BaseDeleteView(DeleteView):
    pass
