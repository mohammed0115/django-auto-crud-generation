# Project Structure Guide

## الهيكل الكامل للمشروع

```
auto_crud_app_project/
│
├── 📄 manage.py                          # Django management CLI
├── 📄 requirements.txt                   # Python dependencies
├── 📄 README.md                          # توثيق المشروع الرئيسي
├── 📄 QUICKSTART.md                      # البدء السريع
├── 📄 EXAMPLE.md                         # مثال عملي كامل
├── 📄 API.md                             # توثيق REST API
├── 📄 CONFIGURATION.md                   # إعدادات إضافية
├── 📄 PROJECT_STRUCTURE.md               # هذا الملف
│
├── 📁 auto_crud_app/                     # Django project config
│   ├── 📄 __init__.py
│   ├── 📄 settings.py                    # إعدادات Django الرئيسية
│   ├── 📄 urls.py                        # URL patterns الرئيسية
│   ├── 📄 asgi.py                        # ASGI config (Async)
│   └── 📄 wsgi.py                        # WSGI config (Production)
│
└── 📁 core/                              # Django app رئيسي
    ├── 📄 __init__.py
    ├── 📄 apps.py                        # App configuration
    ├── 📄 admin.py                       # Django admin registration
    ├── 📄 models.py                      # Data models
    ├── 📄 urls.py                        # Web URL patterns
    ├── 📄 api_urls.py                    # API URL patterns
    ├── 📄 views.py                       # Web views (يتم توليده)
    ├── 📄 forms.py                       # Django forms (يتم توليده)
    ├── 📄 serializers.py                 # DRF serializers (يتم توليده)
    ├── 📄 api_views.py                   # API ViewSets (يتم توليده)
    │
    ├── 📁 crud/                          # CRUD generation engine
    │   ├── 📄 __init__.py
    │   ├── 📄 facade.py                  # Facade pattern - واجهة موحدة
    │   ├── 📄 widgets.py                 # Custom form widgets
    │   ├── 📄 pagination.py              # API pagination classes
    │   ├── 📄 filters.py                 # Search & filter classes
    │   ├── 📄 permissions.py             # Custom permissions
    │   │
    │   └── 📁 generators/                # Code generators
    │       ├── 📄 __init__.py
    │       ├── 📄 views.py               # Views code generator
    │       ├── 📄 forms.py               # Forms code generator
    │       ├── 📄 api.py                 # API code generator
    │       ├── 📄 urls.py                # URLs code generator
    │       └── 📄 templates.py           # Templates code generator
    │
    ├── 📁 management/                    # Custom management commands
    │   ├── 📄 __init__.py
    │   └── 📁 commands/
    │       ├── 📄 __init__.py
    │       └── 📄 generate_crud.py       # Main CRUD generator command
    │
    ├── 📁 templates/                     # HTML templates
    │   └── 📁 base/
    │       └── 📄 base.html              # Base template (Bootstrap)
    │
    ├── 📁 static/                        # CSS, JS, images (اختياري)
    │   ├── 📁 css/
    │   ├── 📁 js/
    │   └── 📁 images/
    │
    └── 📁 migrations/                    # Database migrations
        └── 📄 __init__.py

```

## شرح كل جزء 🔍

### 1. Root Directory Files

| الملف | الغرض |
|------|-------|
| `manage.py` | CLI لتشغيل أوامر Django |
| `requirements.txt` | قائمة بجميع المكتبات المطلوبة |
| `README.md` | توثيق شامل للمشروع |
| `QUICKSTART.md` | دليل البدء السريع |
| `EXAMPLE.md` | أمثلة عملية |
| `API.md` | توثيق REST API |

### 2. auto_crud_app/ - Project Configuration

```python
# settings.py
- تكوين قاعدة البيانات
- تثبيت التطبيقات
- إعدادات الأمان
- متغيرات البيئة

# urls.py
- URL patterns الرئيسية
- تضمين URLs من التطبيقات الأخرى

# wsgi.py / asgi.py
- نقطة دخول الخادم للإنتاج
```

### 3. core/ - Main Application

#### models.py
```python
# نماذج قاعدة البيانات
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(...)
```

#### views.py (يتم توليده)
```python
# Web views
- ListView
- CreateView
- UpdateView
- DeleteView
- DetailView
```

#### forms.py (يتم توليده)
```python
# Django forms
- ModelForm للنماذج
```

#### api_views.py (يتم توليده)
```python
# REST API ViewSets
- ModelViewSet
- مع Permissions و Pagination
```

### 4. crud/ - Code Generation Engine

**facade.py** - الواجهة الموحدة
```python
CRUDFacade(model, app_name, template_engine)
├── generate_web_views()
├── generate_forms()
├── generate_api()
├── generate_templates()
└── generate_all()  # كل شيء
```

**generators/** - منولدات الكود
```
views.py     → توليد Web Views
forms.py     → توليد Django Forms
api.py       → توليد REST API
urls.py      → توليد URL patterns
templates.py → توليد HTML templates
```

### 5. management/commands/generate_crud.py

أمر Django:
```bash
python manage.py generate_crud <app_name> <model_name> --template=bootstrap
```

## سير العمل 🔄

```
1. تحديد النموذج (Model)
        ↓
2. تشغيل generate_crud command
        ↓
3. توليد الكود التلقائي
   ├── Views
   ├── Forms
   ├── Templates
   ├── Serializers
   ├── ViewSets
   └── URL patterns
        ↓
4. نسخ الكود المولد
        ↓
5. تطبيق Migrations
        ↓
6. تشغيل الخادم
        ↓
7. استخدام الـ CRUD كاملاً
```

## الملفات التي يتم توليدها تلقائياً ✅

### 1. views.py
```python
# يحتوي على:
- ProductListView
- ProductCreateView
- ProductUpdateView
- ProductDeleteView
- ProductDetailView
```

### 2. forms.py
```python
# يحتوي على:
- ProductForm (ModelForm)
```

### 3. serializers.py
```python
# يحتوي على:
- ProductSerializer
```

### 4. api_views.py
```python
# يحتوي على:
- ProductViewSet
```

### 5. urls.py
```python
# يحتوي على Web routes:
- /product/ (list)
- /product/create/ (create form)
- /product/<id>/ (detail)
- /product/<id>/update/ (update form)
- /product/<id>/delete/ (delete form)
```

### 6. api_urls.py
```python
# يحتوي على API routes:
- /api/product/ (list/create)
- /api/product/<id>/ (detail/update/delete)
```

### 7. templates/product/
```
list.html          # قائمة المنتجات
form.html          # نموذج الإضافة والتعديل
detail.html        # تفاصيل المنتج
confirm_delete.html # تأكيد الحذف
```

## الملفات الثابتة (غير متغيرة) 📦

### core/crud/ - المحرك

#### widgets.py
```python
WidgetFactory.get_widget()
# أنواع Widgets:
- EmailInput
- DateInput
- DateTimeInput
- CheckboxInput
- TextInput
```

#### pagination.py
```python
StandardPagination
# 10 نتائج لكل صفحة
```

#### filters.py
```python
BaseFilterSet
# البحث والفلترة
```

#### permissions.py
```python
DefaultPermission
# التحقق من Authentication
```

## المتغيرات البيئية (Environment Variables)

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Requirements

```
Django>=4.2
djangorestframework>=3.14
django-filter>=23.1
openpyxl>=3.1.2
```

## التوسعات المستقبلية

### يمكن إضافة:

1. **JWT Authentication**
   ```bash
   pip install djangorestframework-simplejwt
   ```

2. **Celery for async tasks**
   ```bash
   pip install celery redis
   ```

3. **Django Signals**
   - Auto notifications
   - Audit logs

4. **Advanced Filtering**
   - Date range filters
   - Multi-field filters

5. **Caching**
   - Redis cache
   - Query optimization

6. **API Documentation**
   - Swagger/OpenAPI
   - Auto-generated docs

## الملفات المهمة للحفظ

```
✅ models.py      - احفظ نماذجك هنا
✅ admin.py       - سجل النماذج
✅ urls.py        - أضف الـ routes
✅ api_urls.py    - أضف API routes
✅ settings.py    - الإعدادات
```

## ملاحظات مهمة

1. ✅ احفظ `models.py` قبل توليد الـ CRUD
2. ✅ نسخ الملفات المولدة بحذر
3. ✅ طبق Migrations بعد كل تغيير
4. ✅ اختبر الـ CRUD في المتصفح
5. ✅ اختبر API باستخدام Postman أو curl

## Quick Reference

```bash
# البدء
python manage.py migrate

# توليد CRUD
python manage.py generate_crud core Product

# تشغيل
python manage.py runserver

# إنشاء admin
python manage.py createsuperuser

# الوصول
Web:  http://localhost:8000/product/
API:  http://localhost:8000/api/product/
Admin: http://localhost:8000/admin/
```
