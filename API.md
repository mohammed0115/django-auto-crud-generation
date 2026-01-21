# API Documentation

## مقدمة عن REST API

جميع API endpoints توفر CRUD كامل (Create, Read, Update, Delete) مع دعم:
- Pagination
- Filtering
- Search
- Ordering
- Authentication

## Base URL

```
http://localhost:8000/api/
```

## Authentication

جميع الـ API endpoints تتطلب مستخدم مصرح (authenticated user).

### الحصول على Token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### استخدام Token

```bash
curl -X GET http://localhost:8000/api/product/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## API Endpoints (مثال Product)

### 1. قائمة المنتجات (GET)

**URL:** `GET /api/product/`

**Parameters:**
```
page=1                    # رقم الصفحة (default: 1)
page_size=10              # عدد النتائج (default: 10)
search=name              # البحث في الحقول المحددة
ordering=-created_at     # الترتيب (- للتنازلي)
```

**مثال:**

```bash
curl -X GET "http://localhost:8000/api/product/?page=1&search=apple&ordering=-price" \
  -H "Authorization: Bearer TOKEN"
```

**Response:**

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/product/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Apple",
      "price": "10.00",
      "stock": 50,
      "category": "Fruits",
      "created_at": "2026-01-21T10:00:00Z",
      "updated_at": "2026-01-21T10:00:00Z"
    }
  ]
}
```

### 2. إنشاء منتج جديد (POST)

**URL:** `POST /api/product/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer TOKEN
```

**Request Body:**

```json
{
  "name": "Banana",
  "price": "5.00",
  "stock": 100,
  "category": "Fruits"
}
```

**مثال:**

```bash
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "name": "Banana",
    "price": "5.00",
    "stock": 100,
    "category": "Fruits"
  }'
```

**Response (201 Created):**

```json
{
  "id": 2,
  "name": "Banana",
  "price": "5.00",
  "stock": 100,
  "category": "Fruits",
  "created_at": "2026-01-21T10:30:00Z",
  "updated_at": "2026-01-21T10:30:00Z"
}
```

### 3. الحصول على منتج واحد (GET)

**URL:** `GET /api/product/{id}/`

**مثال:**

```bash
curl -X GET http://localhost:8000/api/product/1/ \
  -H "Authorization: Bearer TOKEN"
```

**Response:**

```json
{
  "id": 1,
  "name": "Apple",
  "price": "10.00",
  "stock": 50,
  "category": "Fruits",
  "created_at": "2026-01-21T10:00:00Z",
  "updated_at": "2026-01-21T10:00:00Z"
}
```

### 4. تحديث منتج (PUT)

**URL:** `PUT /api/product/{id}/`

**Request Body:**

```json
{
  "name": "Apple (Updated)",
  "price": "12.00",
  "stock": 40,
  "category": "Fruits"
}
```

**مثال:**

```bash
curl -X PUT http://localhost:8000/api/product/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "name": "Apple (Updated)",
    "price": "12.00",
    "stock": 40,
    "category": "Fruits"
  }'
```

**Response:**

```json
{
  "id": 1,
  "name": "Apple (Updated)",
  "price": "12.00",
  "stock": 40,
  "category": "Fruits",
  "created_at": "2026-01-21T10:00:00Z",
  "updated_at": "2026-01-21T10:30:00Z"
}
```

### 5. حذف منتج (DELETE)

**URL:** `DELETE /api/product/{id}/`

**مثال:**

```bash
curl -X DELETE http://localhost:8000/api/product/1/ \
  -H "Authorization: Bearer TOKEN"
```

**Response:** 204 No Content

## Error Handling

### الأخطاء المحتملة

**400 Bad Request:**
```json
{
  "field_name": ["This field is required."]
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error."
}
```

## Filtering Examples

### البحث

```bash
# البحث عن منتجات تحتوي على "apple"
curl "http://localhost:8000/api/product/?search=apple"
```

### الترتيب

```bash
# ترتيب تصاعدي حسب السعر
curl "http://localhost:8000/api/product/?ordering=price"

# ترتيب تنازلي حسب التاريخ
curl "http://localhost:8000/api/product/?ordering=-created_at"
```

### Pagination

```bash
# الصفحة الثانية بـ 20 نتيجة
curl "http://localhost:8000/api/product/?page=2&page_size=20"
```

## Status Codes

| Code | المعنى |
|------|--------|
| 200 | OK - الطلب نجح |
| 201 | Created - تم الإنشاء بنجاح |
| 204 | No Content - تم الحذف بنجاح |
| 400 | Bad Request - بيانات غير صحيحة |
| 401 | Unauthorized - غير مصرح |
| 403 | Forbidden - ممنوع الوصول |
| 404 | Not Found - غير موجود |
| 500 | Server Error - خطأ في الخادم |

## أمثلة باستخدام Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_token_here"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 1. الحصول على قائمة المنتجات
response = requests.get(f"{BASE_URL}/product/", headers=headers)
products = response.json()

# 2. إنشاء منتج
data = {
    "name": "New Product",
    "price": "20.00",
    "stock": 100,
    "category": "Electronics"
}
response = requests.post(f"{BASE_URL}/product/", json=data, headers=headers)
new_product = response.json()

# 3. تحديث منتج
product_id = 1
data = {"name": "Updated Name", "price": "25.00"}
response = requests.put(f"{BASE_URL}/product/{product_id}/", json=data, headers=headers)

# 4. حذف منتج
response = requests.delete(f"{BASE_URL}/product/{product_id}/", headers=headers)
```

## أمثلة باستخدام JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000/api";
const TOKEN = "your_token_here";

const headers = {
    "Authorization": `Bearer ${TOKEN}`,
    "Content-Type": "application/json"
};

// 1. الحصول على قائمة المنتجات
fetch(`${BASE_URL}/product/`, { headers })
    .then(res => res.json())
    .then(data => console.log(data));

// 2. إنشاء منتج
fetch(`${BASE_URL}/product/`, {
    method: "POST",
    headers,
    body: JSON.stringify({
        name: "New Product",
        price: "20.00",
        stock: 100,
        category: "Electronics"
    })
})
.then(res => res.json())
.then(data => console.log(data));

// 3. تحديث منتج
fetch(`${BASE_URL}/product/1/`, {
    method: "PUT",
    headers,
    body: JSON.stringify({
        name: "Updated",
        price: "25.00"
    })
})
.then(res => res.json())
.then(data => console.log(data));

// 4. حذف منتج
fetch(`${BASE_URL}/product/1/`, {
    method: "DELETE",
    headers
})
.then(res => console.log("Deleted"));
```

## Rate Limiting

الـ API حالياً بدون Rate Limiting. يمكنك إضافته باستخدام:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## Testing API

### استخدام Postman

1. استورد جميع الـ endpoints
2. أضف Authorization header مع Token
3. اختبر جميع العمليات

### استخدام Thunder Client (VSCode)

نفس خطوات Postman لكن داخل VSCode.
