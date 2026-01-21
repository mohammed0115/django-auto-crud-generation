# 🚀 البدء السريع

دليل سريع جداً لتشغيل المشروع فوراً.

## المتطلبات الأساسية

- Python 3.8+
- pip

## 1️⃣ التثبيت (1 دقيقة)

```bash
# تثبيت المكتبات المطلوبة
pip install -r requirements.txt
```

## 2️⃣ إعداد قاعدة البيانات (2 دقيقة)

```bash
# تطبيق Migrations
python manage.py migrate

# إنشاء مستخدم Admin
python manage.py createsuperuser
```

## 3️⃣ إنشاء نموذج (أقل من دقيقة)

أضف هذا الكود في `core/models.py`:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
```

## 4️⃣ توليد CRUD (ثانية واحدة)

```bash
python manage.py generate_crud core Product
```

## 5️⃣ نسخ الملفات المولدة (دقيقتان)

انسخ الكود المطبوع وضعه في:
- `core/views.py`
- `core/forms.py`
- `core/serializers.py`
- `core/api_views.py`
- قم بتحديث `core/urls.py` و `core/api_urls.py`

## 6️⃣ تطبيق التغييرات (دقيقة)

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7️⃣ التشغيل (ثانية واحدة)

```bash
python manage.py runserver
```

## الوصول

- **Admin:** http://localhost:8000/admin/
- **Web:** http://localhost:8000/product/
- **API:** http://localhost:8000/api/product/

---

## 🎯 النتيجة النهائية

في أقل من **5 دقائق** حصلت على:

✅ واجهة Web كاملة (CRUD)
✅ REST API كامل
✅ نماذج Django
✅ تصفح وبحث وحذف
✅ Pagination
✅ Bootstrap styling

## ملاحظة

هذا مثال مبسط. للمزيد من الميزات، انظر [README.md](README.md) و [EXAMPLE.md](EXAMPLE.md)
