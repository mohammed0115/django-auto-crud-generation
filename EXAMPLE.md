# مثال عملي كامل: إنشاء CRUD لـ Product

هذا الملف يوضح خطوات إنشاء CRUD كامل لنموذج Product.

## الخطوة الأولى: إنشاء النموذج

**core/models.py:**

```python
from django.db import models
from core.models import BaseModel

class Product(BaseModel):
    """نموذج المنتج"""
    name = models.CharField(max_length=100, verbose_name="اسم المنتج")
    description = models.TextField(verbose_name="الوصف")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    stock = models.IntegerField(default=0, verbose_name="المخزون")
    category = models.CharField(max_length=50, default="عام", verbose_name="الفئة")
    
    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "منتجات"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.name} - {self.price} ر.س"
```

## الخطوة الثانية: تشغيل أمر التوليد

```bash
python manage.py generate_crud core Product --template=bootstrap
```

سيطبع الأمر الكود التالي:

## الملفات المولدة

### 1. core/views.py

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """قائمة المنتجات"""
    model = Product
    paginate_by = 10
    template_name = "product/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs.order_by("-id")


class ProductCreateView(CreateView):
    """إضافة منتج جديد"""
    model = Product
    form_class = ProductForm
    template_name = "product/form.html"
    success_url = reverse_lazy("product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة منتج جديد'
        context['button_text'] = 'إضافة'
        return context


class ProductUpdateView(UpdateView):
    """تعديل منتج"""
    model = Product
    form_class = ProductForm
    template_name = "product/form.html"
    success_url = reverse_lazy("product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'تعديل {self.object}'
        context['button_text'] = 'حفظ التغييرات'
        return context


class ProductDeleteView(DeleteView):
    """حذف منتج"""
    model = Product
    template_name = "product/confirm_delete.html"
    success_url = reverse_lazy("product_list")


class ProductDetailView(DetailView):
    """تفاصيل المنتج"""
    model = Product
    template_name = "product/detail.html"
    context_object_name = "object"
```

### 2. core/forms.py

```python
from django import forms
from .models import Product
from core.crud.widgets import WidgetFactory


class ProductForm(forms.ModelForm):
    """نموذج المنتج"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = WidgetFactory.get_widget(field, "bootstrap")
            field.widget = widget
```

### 3. core/urls.py

```python
from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView,
)

app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="delete"),
]
```

### 4. core/serializers.py

```python
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer للمنتج"""
    
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
```

### 5. core/api_views.py

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from core.crud.pagination import StandardPagination
from core.crud.permissions import DefaultPermission


class ProductViewSet(ModelViewSet):
    """
    ViewSet للمنتج
    
    توفر عمليات CRUD كاملة عبر REST API
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination
    permission_classes = [DefaultPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["id", "-created_at", "-updated_at"]
    ordering = ["-created_at"]
```

### 6. core/api_urls.py

```python
from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")

urlpatterns = router.urls
```

### 7. core/templates/product/list.html

```html
{% extends "base/base.html" %}

{% block title %}المنتجات - قائمة{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row mb-4">
        <div class="col-md-6">
            <h1>المنتجات</h1>
        </div>
        <div class="col-md-6 text-end">
            <a href="{% url 'product:create' %}" class="btn btn-primary">
                + إضافة منتج
            </a>
        </div>
    </div>

    <!-- نموذج البحث -->
    <div class="row mb-4">
        <div class="col-md-12">
            <form method="get" class="form-inline">
                <input type="text" name="q" class="form-control" placeholder="ابحث..." value="{{ request.GET.q }}">
                <button type="submit" class="btn btn-secondary ms-2">بحث</button>
            </form>
        </div>
    </div>

    <!-- جدول المنتجات -->
    <div class="table-responsive">
        <table class="table table-striped table-hover">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>الاسم</th>
                    <th>السعر</th>
                    <th>المخزون</th>
                    <th>الفئة</th>
                    <th>الإجراءات</th>
                </tr>
            </thead>
            <tbody>
                {% for item in objects %}
                <tr>
                    <td>{{ item.id }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.price }} ر.س</td>
                    <td>{{ item.stock }}</td>
                    <td>{{ item.category }}</td>
                    <td>
                        <a href="{% url 'product:detail' item.id %}" class="btn btn-sm btn-info">عرض</a>
                        <a href="{% url 'product:update' item.id %}" class="btn btn-sm btn-warning">تعديل</a>
                        <a href="{% url 'product:delete' item.id %}" class="btn btn-sm btn-danger">حذف</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- التصفح -->
    {% if is_paginated %}
    <nav aria-label="Page navigation">
        <ul class="pagination">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1">الأولى</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}">السابقة</a>
            </li>
            {% endif %}

            <li class="page-item active">
                <span class="page-link">الصفحة {{ page_obj.number }} من {{ page_obj.paginator.num_pages }}</span>
            </li>

            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}">التالية</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">الأخيرة</a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}
```

## خطوات التطبيق

```bash
# 1. تطبيق Migrations
python manage.py makemigrations
python manage.py migrate

# 2. تشغيل الخادم
python manage.py runserver

# 3. الوصول إلى التطبيق
# Web: http://localhost:8000/product/
# API: http://localhost:8000/api/product/
```

## الخطوات الخمسة الكاملة

1. ✅ إنشاء النموذج في `core/models.py`
2. ✅ تشغيل أمر التوليد
3. ✅ نسخ الملفات المولدة
4. ✅ تطبيق Migrations
5. ✅ تشغيل الخادم

تم! 🎉
