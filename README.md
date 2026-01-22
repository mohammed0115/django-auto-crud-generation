<<<<<<< HEAD
# Django Auto CRUD Generator

نظام توليد CRUD تلقائي لـ Django مع دعم Web و REST API.

## المميزات 🚀

- ✅ توليد Web Views تلقائي (List, Create, Update, Delete, Detail)
- ✅ توليد Forms مع Bootstrap/Tailwind
- ✅ توليد REST API (Serializers, ViewSets, Routers)
- ✅ توليد Templates HTML
- ✅ توليد URL patterns
- ✅ دعم Pagination و Filtering
- ✅ Permissions و Authentication

## متطلبات التثبيت

```bash
pip install -r requirements.txt
```

## هيكل المشروع

```
auto_crud_app/
├── manage.py
├── requirements.txt
├── auto_crud_app/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/
    ├── models.py
    ├── admin.py
    ├── urls.py
    ├── api_urls.py
    ├── management/
    │   └── commands/
    │       └── generate_crud.py
    ├── crud/
    │   ├── facade.py
    │   ├── widgets.py
    │   ├── pagination.py
    │   ├── filters.py
    │   ├── permissions.py
    │   └── generators/
    │       ├── views.py
    │       ├── forms.py
    │       ├── api.py
    │       ├── urls.py
    │       └── templates.py
    └── templates/
        └── base/
            └── base.html
```

## طريقة الاستخدام

### 1️⃣ إنشاء نموذج (Model)

أولاً، قم بإنشاء نموذج في `core/models.py`:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
```

### 2️⃣ تشغيل أمر التوليد

```bash
# لتوليد CRUD مع Bootstrap
python manage.py generate_crud products Product --template=bootstrap

# أو مع Tailwind
python manage.py generate_crud products Product --template=tailwind
```

### 3️⃣ نسخ الملفات المولدة

الأمر سيطبع الكود المولد. انسخ:
- **views.py** → ألصقه في `core/views.py`
- **forms.py** → ألصقه في `core/forms.py`
- **Web URLs** → ألصقه في `core/urls.py`
- **API Serializer & ViewSet** → أنشئ `core/serializers.py` و `core/api_views.py`
- **API URLs** → ألصقه في `core/api_urls.py`
- **Templates** → أنشئ `core/templates/product/` وضع الـ 4 templates فيها

### 4️⃣ تطبيق Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ تشغيل الخادم

```bash
python manage.py runserver
```

الآن يمكنك الوصول إلى:
- **Web Interface:** http://localhost:8000/product/
- **API:** http://localhost:8000/api/product/

## API Endpoints

لنموذج `Product`، ستحصل على الـ endpoints التالية:

```
GET    /api/product/              # قائمة المنتجات
POST   /api/product/              # إنشاء منتج جديد
GET    /api/product/{id}/         # تفاصيل منتج
PUT    /api/product/{id}/         # تحديث منتج
DELETE /api/product/{id}/         # حذف منتج
```

## Web Routes

```
GET  /product/                    # قائمة المنتجات
GET  /product/create/             # نموذج إضافة منتج
GET  /product/{id}/               # تفاصيل المنتج
GET  /product/{id}/update/        # نموذج تعديل المنتج
GET  /product/{id}/delete/        # تأكيد حذف المنتج
```

## مثال العملي الكامل

### الخطوة 1: إنشاء نموذج Customer

**core/models.py:**
```python
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
```

### الخطوة 2: تشغيل الأمر

```bash
python manage.py generate_crud core Customer --template=bootstrap
```

### الخطوة 3: نسخ الملفات المولدة

انسخ الكود المطبوع وضعه في الملفات المناسبة

### الخطوة 4: تطبيق التغييرات

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### الخطوة 5: الاستخدام

الآن يمكنك:
- الوصول إلى http://localhost:8000/customer/ لعرض قائمة العملاء
- الوصول إلى http://localhost:8000/api/customer/ للـ API

## ملاحظات مهمة

⚠️ **لا تنسى:**
1. تحديث `core/urls.py` لشمل URL patterns الخاصة بك
2. تحديث `core/api_urls.py` لشمل API URLs
3. تحديث `core/admin.py` لتسجيل النماذج في الـ Admin
4. إنشاء مجلد `templates` مع اسم النموذج بالحروف الصغيرة

## التخصيص

### تغيير CSS Framework

```bash
# لـ Tailwind
python manage.py generate_crud core Product --template=tailwind
```

### إضافة Fields مخصصة

عدّل الـ `widgets.py` لإضافة widgets مخصصة:

```python
@staticmethod
def get_widget(field, framework="bootstrap"):
    # أضف حالات مخصصة هنا
```

## الترخيص

MIT License

## المؤلف

https://github.com/mohammed0115
## الدعم

للمساعدة والأسئلة، يرجى فتح issue على GitHub.

=======
# Django Auto CRUD Generator

نظام توليد CRUD تلقائي لـ Django مع دعم Web و REST API.

## المميزات 🚀

- ✅ توليد Web Views تلقائي (List, Create, Update, Delete, Detail)
- ✅ توليد Forms مع Bootstrap/Tailwind
- ✅ توليد REST API (Serializers, ViewSets, Routers)
- ✅ توليد Templates HTML
- ✅ توليد URL patterns
- ✅ دعم Pagination و Filtering
- ✅ Permissions و Authentication

## متطلبات التثبيت

```bash
pip install -r requirements.txt
```

## هيكل المشروع

```
auto_crud_app/
├── manage.py
├── requirements.txt
├── auto_crud_app/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/
    ├── models.py
    ├── admin.py
    ├── urls.py
    ├── api_urls.py
    ├── management/
    │   └── commands/
    │       └── generate_crud.py
    ├── crud/
    │   ├── facade.py
    │   ├── widgets.py
    │   ├── pagination.py
    │   ├── filters.py
    │   ├── permissions.py
    │   └── generators/
    │       ├── views.py
    │       ├── forms.py
    │       ├── api.py
    │       ├── urls.py
    │       └── templates.py
    └── templates/
        └── base/
            └── base.html
```

## طريقة الاستخدام

### 1️⃣ إنشاء نموذج (Model)

أولاً، قم بإنشاء نموذج في `core/models.py`:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
```

### 2️⃣ تشغيل أمر التوليد

```bash
# لتوليد CRUD مع Bootstrap
python manage.py generate_crud core Product --template=bootstrap

# أو مع Tailwind
python manage.py generate_crud core Product --template=tailwind
```

### 3️⃣ نسخ الملفات المولدة

الأمر سيطبع الكود المولد. انسخ:
- **views.py** → ألصقه في `core/views.py`
- **forms.py** → ألصقه في `core/forms.py`
- **Web URLs** → ألصقه في `core/urls.py`
- **API Serializer & ViewSet** → أنشئ `core/serializers.py` و `core/api_views.py`
- **API URLs** → ألصقه في `core/api_urls.py`
- **Templates** → أنشئ `core/templates/product/` وضع الـ 4 templates فيها

### 4️⃣ تطبيق Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ تشغيل الخادم

```bash
python manage.py runserver
```

الآن يمكنك الوصول إلى:
- **Web Interface:** http://localhost:8000/product/
- **API:** http://localhost:8000/api/product/

## API Endpoints

لنموذج `Product`، ستحصل على الـ endpoints التالية:

```
GET    /api/product/              # قائمة المنتجات
POST   /api/product/              # إنشاء منتج جديد
GET    /api/product/{id}/         # تفاصيل منتج
PUT    /api/product/{id}/         # تحديث منتج
DELETE /api/product/{id}/         # حذف منتج
```

## Web Routes

```
GET  /product/                    # قائمة المنتجات
GET  /product/create/             # نموذج إضافة منتج
GET  /product/{id}/               # تفاصيل المنتج
GET  /product/{id}/update/        # نموذج تعديل المنتج
GET  /product/{id}/delete/        # تأكيد حذف المنتج
```

## مثال العملي الكامل

### الخطوة 1: إنشاء نموذج Customer

**core/models.py:**
```python
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
```

### الخطوة 2: تشغيل الأمر

```bash
python manage.py generate_crud core Customer --template=bootstrap
```

### الخطوة 3: نسخ الملفات المولدة

انسخ الكود المطبوع وضعه في الملفات المناسبة

### الخطوة 4: تطبيق التغييرات

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### الخطوة 5: الاستخدام

الآن يمكنك:
- الوصول إلى http://localhost:8000/customer/ لعرض قائمة العملاء
- الوصول إلى http://localhost:8000/api/customer/ للـ API

## ملاحظات مهمة

⚠️ **لا تنسى:**
1. تحديث `core/urls.py` لشمل URL patterns الخاصة بك
2. تحديث `core/api_urls.py` لشمل API URLs
3. تحديث `core/admin.py` لتسجيل النماذج في الـ Admin
4. إنشاء مجلد `templates` مع اسم النموذج بالحروف الصغيرة

## التخصيص

### تغيير CSS Framework

```bash
# لـ Tailwind
python manage.py generate_crud core Product --template=tailwind
```

### إضافة Fields مخصصة

عدّل الـ `widgets.py` لإضافة widgets مخصصة:

```python
@staticmethod
def get_widget(field, framework="bootstrap"):
    # أضف حالات مخصصة هنا
```

## الترخيص

MIT License

## المؤلف

Django CRUD Generator Team

## الدعم

للمساعدة والأسئلة، يرجى فتح issue على GitHub.
>>>>>>> 5235ea4 (django uto-generate crud for APIs and web)
