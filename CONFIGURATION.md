# Project Configuration Guide

## الملفات الإضافية المطلوبة (يمكنك إنشاؤها حسب الحاجة)

### 1. .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
/media
/staticfiles

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.coverage
.pytest_cache/
htmlcov/
```

### 2. .env (ملف المتغيرات)

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 3. pytest.ini

```ini
[pytest]
DJANGO_SETTINGS_MODULE = auto_crud_app.settings
python_files = tests.py test_*.py *_tests.py
addopts = --strict-markers
testpaths = .
```

### 4. gunicorn_config.py (للإنتاج)

```python
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

## الأوامر المهمة

### إنشاء مستخدم Admin
```bash
python manage.py createsuperuser
```

### إعادة تعيين قاعدة البيانات (تطوير فقط)
```bash
python manage.py flush
```

### جمع الملفات الثابتة (في الإنتاج)
```bash
python manage.py collectstatic
```

### إنشاء backup من البيانات
```bash
python manage.py dumpdata > backup.json
```

### استعادة البيانات
```bash
python manage.py loaddata backup.json
```

## Deployment إلى Heroku

### 1. التثبيت الأولي
```bash
heroku login
heroku create your-app-name
```

### 2. ملفات مطلوبة

**Procfile:**
```
web: gunicorn auto_crud_app.wsgi
```

**runtime.txt:**
```
python-3.11.6
```

### 3. النشر
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## تشغيل Tests

```bash
# تشغيل جميع الـ tests
python manage.py test

# تشغيل tests لتطبيق معين
python manage.py test core

# مع تقرير Coverage
coverage run --source='.' manage.py test
coverage report
```

## Celery (مهام غير متزامنة)

### التثبيت
```bash
pip install celery redis
```

### إنشاء celery.py في auto_crud_app/

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_crud_app.settings')

app = Celery('auto_crud_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### تشغيل Celery Worker
```bash
celery -A auto_crud_app worker -l info
```

## مراقبة الأداء

### تثبيت Django Debug Toolbar
```bash
pip install django-debug-toolbar
```

أضف إلى `settings.py`:
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

## أفضل الممارسات

1. ✅ استخدم Virtual Environment دائماً
2. ✅ احفظ جميع Dependencies في requirements.txt
3. ✅ استخدم Environment Variables للـ Secrets
4. ✅ اكتب Tests لكل Functionality
5. ✅ استخدم Git لإدارة الإصدارات
6. ✅ اتبع PEP 8 لتنسيق الكود
7. ✅ استخدم Logging للـ Debugging

## المراجع المفيدة

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/topics/db/models/best-practices/)
