# Troubleshooting & FAQ

## ❓ الأسئلة الشائعة

### س: كيف أبدأ المشروع من الصفر؟

ج: اتبع هذه الخطوات:
```bash
# 1. تثبيت المكتبات
pip install -r requirements.txt

# 2. Migrations
python manage.py migrate

# 3. إنشاء نموذج في models.py

# 4. توليد CRUD
python manage.py generate_crud core YourModel

# 5. نسخ الملفات المولدة

# 6. تطبيق الـ migrations
python manage.py makemigrations
python manage.py migrate

# 7. تشغيل
python manage.py runserver
```

### س: أين أضع الملفات المولدة؟

ج: الملفات المولدة تذهب إلى:
```
views.py      → core/views.py (استبدل المحتوى أو أضفه)
forms.py      → core/forms.py
serializers.py → core/serializers.py
api_views.py  → core/api_views.py
```

### س: كيف أتحديث URL patterns؟

ج: أضف هذا في `core/urls.py`:
```python
from django.urls import path, include
from . import views

urlpatterns = [
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    # ... باقي الـ URLs
]
```

### س: ماذا تفعل Migrations؟

ج: تنشئ جداول قاعدة البيانات:
```bash
python manage.py makemigrations  # إنشاء ملف migration
python manage.py migrate         # تطبيق التغييرات على DB
```

### س: كيف أحذف كل شيء وأبدأ من جديد؟

⚠️ **تحذير**: هذا يحذف جميع البيانات!
```bash
python manage.py flush  # يحذف جميع البيانات
# أو احذف db.sqlite3 يدويًا
```

---

## 🐛 حل المشاكل الشائعة

### مشكلة 1: "ModuleNotFoundError: No module named 'django'"

**السبب:** لم تثبت المكتبات

**الحل:**
```bash
pip install -r requirements.txt
```

### مشكلة 2: "Model not found in app"

**السبب:** اسم النموذج أو التطبيق غير صحيح

**الحل:**
```bash
# تأكد من اسم النموذج والتطبيق
python manage.py generate_crud core Product  # صحيح
python manage.py generate_crud core product  # خطأ (يجب capitalize)
```

### مشكلة 3: "relation does not exist"

**السبب:** لم تطبق Migrations

**الحل:**
```bash
python manage.py migrate
# أو إذا كنت تعدل النموذج
python manage.py makemigrations
python manage.py migrate
```

### مشكلة 4: "No such table"

**السبب:** لم تنشئ جداول قاعدة البيانات

**الحل:**
```bash
python manage.py migrate
```

### مشكلة 5: "TemplateDoesNotExist"

**السبب:** ملفات HTML غير موجودة

**الحل:**
أنشئ مجلد `templates` وضع الـ HTML files:
```
core/templates/
└── product/
    ├── list.html
    ├── form.html
    ├── detail.html
    └── confirm_delete.html
```

### مشكلة 6: "CSRF token missing"

**السبب:** نسيت `{% csrf_token %}` في الـ Form

**الحل:**
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
    <button type="submit">إرسال</button>
</form>
```

### مشكلة 7: "Port 8000 already in use"

**السبب:** الخادم يعمل على نفس الـ Port

**الحل:**
```bash
# استخدم port مختلف
python manage.py runserver 8001

# أو أغلق الـ process القديم
# Windows:
taskkill /PID <process_id> /F

# Linux/Mac:
kill -9 <process_id>
```

### مشكلة 8: "Static files not loading"

**السبب:** Static files لم تجمع

**الحل:**
```bash
# في development (عادي):
# يعمل تلقائياً

# في production:
python manage.py collectstatic
```

### مشكلة 9: "Authentication error in API"

**السبب:** لم تضيف Authorization header

**الحل:**
```bash
# استخدم curl مع header
curl -X GET http://localhost:8000/api/product/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### مشكلة 10: "Form validation error"

**السبب:** بيانات غير صحيحة

**الحل:**
تأكد من:
```python
# تحقق من validators في الـ Model
# تأكد من أنواع البيانات
# اختبر البيانات قبل الإرسال
```

---

## 🔧 نصائح للـ Debugging

### 1. استخدم Django Shell

```bash
python manage.py shell

# في ال shell:
from core.models import Product
Product.objects.all()
Product.objects.create(name="Test", price=10)
```

### 2. استخدم Print Statements

```python
# في views.py
def get_queryset(self):
    qs = super().get_queryset()
    print(f"DEBUG: Queryset = {qs}")
    return qs
```

### 3. استخدم Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

### 4. تحقق من السجلات

```bash
# في settings.py أضف logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
```

---

## ⚙️ تخصيص الـ Generator

### تغيير Bootstrap إلى Tailwind

```bash
python manage.py generate_crud core Product --template=tailwind
```

### إضافة حقول مخصصة

في `core/crud/widgets.py`:
```python
@staticmethod
def get_widget(field, framework="bootstrap"):
    # أضف حالات جديدة
    if isinstance(field, YourCustomField):
        return YourCustomWidget()
    return forms.TextInput()
```

### تعديل Templates

عدّل الـ `core/crud/generators/templates.py`:
```python
def generate_list_template(self):
    # أضف أعمدة أو أزرار مخصصة
    template = f"""
    <!-- أضف HTML مخصص هنا -->
    """
    return template
```

---

## 🚀 تحسينات الأداء

### 1. استخدم Select Related

```python
# في views.py
def get_queryset(self):
    return Product.objects.select_related('category')
```

### 2. استخدم Prefetch Related

```python
def get_queryset(self):
    return Product.objects.prefetch_related('tags')
```

### 3. استخدم Caching

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
def product_list(request):
    # ...
```

### 4. استخدم Database Indexing

```python
class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
```

---

## 📋 Checklist قبل الـ Deployment

- [ ] غيّر `SECRET_KEY` في settings.py
- [ ] ضع `DEBUG = False`
- [ ] أضف Allowed Hosts
- [ ] استخدم Environment Variables
- [ ] طبق Security Headers
- [ ] أضف HTTPS
- [ ] اختبر جميع الـ CRUD operations
- [ ] اختبر API endpoints
- [ ] تحقق من Error Handling
- [ ] أضف Logging
- [ ] استخدم Database Backups
- [ ] اختبر Performance

---

## 📞 الحصول على المساعدة

### إذا واجهت مشكلة:

1. ✅ تحقق من رسالة الخطأ
2. ✅ ابحث عن الحل في هذا الملف
3. ✅ جرب Django Shell
4. ✅ اقرأ توثيق Django الرسمية
5. ✅ ابحث على Stack Overflow

### الموارد المفيدة:

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Stack Overflow Django Tag](https://stackoverflow.com/questions/tagged/django)

---

## 🎓 موارد تعليمية

### مقاطع فيديو:
- Django Basics
- Django REST Framework
- Advanced Django

### كتب:
- "Two Scoops of Django"
- "Django for Beginners"
- "Django for API Development"

---

## آخر تحديث

تاريخ التحديث: 21 يناير 2026
الإصدار: 1.0
