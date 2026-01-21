# 🚀 Django Auto CRUD Generator

> **نظام توليد CRUD تلقائي متكامل لـ Django**

اكتب الأمر واحصل على Web Interface + REST API + Forms + Templates في دقائق! ⚡

---

## ⚡ البدء الفوري (4 دقائق)

```bash
# 1. التثبيت
pip install -r requirements.txt

# 2. الإعداد
python manage.py migrate

# 3. أضف نموذج في core/models.py، ثم:
python manage.py generate_crud core YourModel

# 4. التشغيل
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

**النتيجة**: http://localhost:8000/yourmodel/ ✨

---

## 📖 أين تبدأ؟

### 👶 للمبتدئين
1. اقرأ [START.md](START.md) (2 دقيقة)
2. اقرأ [QUICKSTART.md](QUICKSTART.md) (10 دقائق)
3. جرب المثال في [EXAMPLE.md](EXAMPLE.md)

### 💪 للمطورين
1. اقرأ [README.md](README.md) (شامل)
2. اقرأ [API.md](API.md) (REST API)
3. اقرأ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

### 🆘 عند حدوث مشكلة
اقرأ [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### 🗂️ فهرس سريع
اقرأ [INDEX.md](INDEX.md)

---

## ✨ ما تحصل عليه

### Web Interface 🌐
```
✅ قائمة (مع Pagination)
✅ إضافة جديد
✅ تعديل
✅ حذف
✅ تفاصيل
✅ بحث
```

### REST API 📡
```
✅ GET    /api/model/
✅ POST   /api/model/
✅ GET    /api/model/{id}/
✅ PUT    /api/model/{id}/
✅ DELETE /api/model/{id}/
```

### المميزات 🎯
```
✅ Bootstrap 5 Design
✅ Pagination
✅ Search & Filter
✅ Permissions
✅ Form Widgets
```

---

## 📁 الملفات المهمة

| الملف | الوصف |
|------|--------|
| [START.md](START.md) | ⭐ ابدأ هنا! |
| [QUICKSTART.md](QUICKSTART.md) | 7 خطوات سريعة |
| [EXAMPLE.md](EXAMPLE.md) | مثال عملي كامل |
| [README.md](README.md) | توثيق شاملة |
| [API.md](API.md) | توثيق REST API |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | حل المشاكل |
| [INDEX.md](INDEX.md) | فهرس سريع |

---

## 🎯 الخطوات الأساسية

```python
# 1. أنشئ نموذج في core/models.py
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

```bash
# 2. وليّد CRUD
python manage.py generate_crud core Product
```

```bash
# 3. طبق التغييرات
python manage.py makemigrations
python manage.py migrate
```

```bash
# 4. شغل الخادم
python manage.py runserver
```

**النتيجة**:
- Web: http://localhost:8000/product/
- API: http://localhost:8000/api/product/
- Admin: http://localhost:8000/admin/

---

## 📊 الإحصائيات

| الميزة | القيمة |
|--------|--------|
| الملفات | 42+ |
| أسطر الكود | 3350+ |
| توثيق | 13 ملف |
| Generators | 6 |
| Bootstrap | 5 |
| API Endpoints | 5 CRUD |

---

## 🔧 المتطلبات

- Python 3.8+
- pip
- Django 4.2+

---

## 🆘 الدعم

### مشاكل شائعة؟
→ اقرأ [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### أسئلة عن الاستخدام؟
→ اقرأ [EXAMPLE.md](EXAMPLE.md)

### معلومات API؟
→ اقرأ [API.md](API.md)

### شيء آخر؟
→ اقرأ [INDEX.md](INDEX.md)

---

## 📚 الملفات الكاملة

### للبدء السريع
- [START.md](START.md) - ابدأ هنا
- [QUICKSTART.md](QUICKSTART.md) - خطوات سريعة
- [EXAMPLE.md](EXAMPLE.md) - مثال كامل

### التوثيق الشاملة
- [README.md](README.md) - الدليل الكامل
- [API.md](API.md) - REST API
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - الهيكل
- [CONFIGURATION.md](CONFIGURATION.md) - الإعدادات

### المراجع
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - حل المشاكل
- [INDEX.md](INDEX.md) - الفهرس
- [CONTENTS.md](CONTENTS.md) - جدول المحتويات
- [FILES.md](FILES.md) - قائمة الملفات
- [WELCOME.md](WELCOME.md) - رسالة الترحيب
- [SUMMARY.md](SUMMARY.md) - ملخص الإنجاز

---

## 🎓 مستويات مختلفة

### مستوى 1: للمبتدئين
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### مستوى 2: للمتوسطين
```bash
# أضف نموذج
python manage.py generate_crud core Product
# انسخ الملفات المولدة
python manage.py makemigrations && migrate
```

### مستوى 3: للمتقدمين
```bash
# ادرس الـ generators
# خصّص الـ widgets و templates
# أضف features مخصصة
```

---

## 🚀 ابدأ الآن!

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

ثم افتح: http://localhost:8000/admin/

---

## 📞 معلومات سريعة

- **الإصدار**: 1.0.0
- **الحالة**: جاهز للإنتاج ✅
- **الترخيص**: MIT
- **التاريخ**: يناير 2026

---

**🎉 هيا بنا نبدأ!**

اقرأ [START.md](START.md) الآن! 👈
