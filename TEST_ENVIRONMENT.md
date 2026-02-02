# Test Environment Specification
# Wasla E-commerce Platform

**Version:** 1.0  
**Date:** February 2026  
**Environment Type:** Testing & Staging

---

## Table of Contents
1. [Environment Overview](#1-environment-overview)
2. [Infrastructure Requirements](#2-infrastructure-requirements)
3. [Test Environment Setup](#3-test-environment-setup)
4. [Testing Strategy](#4-testing-strategy)
5. [Test Data Management](#5-test-data-management)
6. [Quality Assurance Process](#6-quality-assurance-process)
7. [Performance Testing](#7-performance-testing)
8. [Security Testing](#8-security-testing)

---

## 1. Environment Overview

### 1.1 Purpose
The test environment provides a safe, isolated space for:
- Quality assurance testing
- Integration testing
- User acceptance testing (UAT)
- Performance testing
- Security testing
- Pre-production validation

### 1.2 Environment Types

#### Development Environment
- **Purpose**: Active development and unit testing
- **Access**: Developers only
- **Data**: Mock and synthetic data
- **Uptime**: Not critical

#### Testing Environment
- **Purpose**: QA and integration testing
- **Access**: Developers, QA team
- **Data**: Synthetic test data
- **Uptime**: Business hours (99%)

#### Staging Environment
- **Purpose**: Pre-production validation and UAT
- **Access**: All team members, selected beta users
- **Data**: Anonymized production-like data
- **Uptime**: 99.5%

---

## 2. Infrastructure Requirements

### 2.1 Cloud Infrastructure

#### Compute Resources
- **Development**:
  - 2x Application servers (t3.medium)
  - 1x Database server (t3.medium)
  - 1x Redis cache (t3.small)
  
- **Testing**:
  - 3x Application servers (t3.large)
  - 1x Database server (t3.large)
  - 1x Redis cache (t3.medium)
  - 1x Elasticsearch (t3.medium)
  
- **Staging**:
  - 5x Application servers (t3.xlarge)
  - 2x Database servers (Primary + Replica, t3.xlarge)
  - 2x Redis cache (Master + Replica, t3.large)
  - 2x Elasticsearch (t3.large)
  - 1x Load balancer

#### Storage
- **Development**: 50GB SSD
- **Testing**: 200GB SSD
- **Staging**: 500GB SSD

#### Network
- Virtual Private Cloud (VPC)
- Private subnets for databases
- Public subnets for application servers
- Security groups for access control
- NAT gateway for outbound traffic

### 2.2 Database Setup

#### PostgreSQL Configuration
```yaml
Development:
  Instance: db.t3.medium
  Storage: 50GB
  Backup: Daily, 7 days retention
  Multi-AZ: No
  
Testing:
  Instance: db.t3.large
  Storage: 200GB
  Backup: Daily, 14 days retention
  Multi-AZ: No
  
Staging:
  Instance: db.t3.xlarge
  Storage: 500GB
  Backup: Daily, 30 days retention
  Multi-AZ: Yes
  Read Replicas: 1
```

#### Database Isolation
- Separate database instances for each environment
- No shared databases between environments
- Encrypted connections required
- Access controlled via security groups

### 2.3 Cache Layer

#### Redis Configuration
```yaml
Development:
  Instance: cache.t3.small
  Memory: 1.5GB
  Eviction: allkeys-lru
  
Testing:
  Instance: cache.t3.medium
  Memory: 3GB
  Eviction: allkeys-lru
  
Staging:
  Instance: cache.t3.large
  Memory: 6GB
  Replication: Yes (1 replica)
  Eviction: allkeys-lru
  Persistence: RDB + AOF
```

### 2.4 Search Engine

#### Elasticsearch Configuration
```yaml
Testing:
  Nodes: 1
  Instance: t3.medium
  Storage: 100GB
  
Staging:
  Nodes: 2
  Instance: t3.large
  Storage: 250GB
  Snapshots: Daily
```

---

## 3. Test Environment Setup

### 3.1 Configuration Management

#### Environment Variables
```bash
# Development
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=postgresql://dev:pass@dev-db:5432/wasla_dev
REDIS_URL=redis://dev-redis:6379/0
ALLOWED_HOSTS=*.dev.wasla.local
SECRET_KEY=dev-secret-key-change-in-prod

# Testing
ENVIRONMENT=testing
DEBUG=False
DATABASE_URL=postgresql://test:pass@test-db:5432/wasla_test
REDIS_URL=redis://test-redis:6379/0
ELASTICSEARCH_URL=http://test-es:9200
ALLOWED_HOSTS=*.test.wasla.com

# Staging
ENVIRONMENT=staging
DEBUG=False
DATABASE_URL=postgresql://stage:pass@stage-db:5432/wasla_stage
REDIS_URL=redis://stage-redis:6379/0
ELASTICSEARCH_URL=http://stage-es:9200
ALLOWED_HOSTS=*.staging.wasla.com
```

### 3.2 Deployment Process

#### Automated Deployment
```yaml
# .gitlab-ci.yml or .github/workflows/deploy.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - python manage.py test
    - coverage report

build:
  stage: build
  script:
    - docker build -t wasla:${CI_COMMIT_SHA} .
    - docker push wasla:${CI_COMMIT_SHA}

deploy_testing:
  stage: deploy
  environment: testing
  script:
    - kubectl set image deployment/wasla wasla=wasla:${CI_COMMIT_SHA}
    - kubectl rollout status deployment/wasla

deploy_staging:
  stage: deploy
  environment: staging
  when: manual
  script:
    - kubectl set image deployment/wasla wasla=wasla:${CI_COMMIT_SHA}
    - kubectl rollout status deployment/wasla
```

### 3.3 Access Control

#### User Access Matrix
| Role | Development | Testing | Staging | Production |
|------|-------------|---------|---------|------------|
| Developers | Full | Full | Read | No Direct |
| QA Team | Read | Full | Full | Read |
| Product Manager | Read | Read | Full | Read |
| DevOps | Full | Full | Full | Full |
| External Users | No | No | Limited | Full |

#### Authentication
- VPN required for all environments
- SSH key-based authentication
- Multi-factor authentication for staging
- Audit logging enabled

---

## 4. Testing Strategy

### 4.1 Unit Testing

#### Framework
- **Python**: pytest, unittest
- **Coverage Target**: > 80%
- **Execution**: Automated on each commit

#### Example
```python
# tests/test_products.py
import pytest
from core.models import Product

@pytest.mark.django_db
def test_product_creation():
    product = Product.objects.create(
        name="Test Product",
        price=99.99,
        stock=10
    )
    assert product.name == "Test Product"
    assert product.price == 99.99
    assert product.in_stock() == True

@pytest.mark.django_db
def test_product_out_of_stock():
    product = Product.objects.create(
        name="Test Product",
        price=99.99,
        stock=0
    )
    assert product.in_stock() == False
```

### 4.2 Integration Testing

#### API Testing
- **Tool**: pytest-django, requests
- **Coverage**: All API endpoints
- **Validation**: Request/response format, status codes, data integrity

#### Example
```python
# tests/test_api.py
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_product_list_api():
    client = APIClient()
    response = client.get('/api/products/')
    assert response.status_code == 200
    assert 'results' in response.json()

@pytest.mark.django_db
def test_product_create_api():
    client = APIClient()
    data = {
        'name': 'New Product',
        'price': '149.99',
        'stock': 5
    }
    response = client.post('/api/products/', data)
    assert response.status_code == 201
    assert response.json()['name'] == 'New Product'
```

### 4.3 End-to-End Testing

#### Framework
- **Tool**: Selenium, Playwright
- **Scope**: Critical user flows
- **Execution**: Nightly automated runs

#### Test Scenarios
1. User registration and login
2. Product browsing and search
3. Add to cart and checkout
4. Order placement and confirmation
5. Merchant store creation
6. Product management
7. Order fulfillment

### 4.4 User Acceptance Testing (UAT)

#### Process
1. Define acceptance criteria
2. Create test cases
3. Set up staging environment
4. Execute test cases with stakeholders
5. Document results and feedback
6. Address issues
7. Sign-off

#### Test Cases Template
```markdown
**Test Case ID**: UAT-001
**Feature**: Product Creation
**User Story**: As a merchant, I want to create a product

**Pre-conditions**:
- Merchant account created
- Logged in to dashboard

**Test Steps**:
1. Navigate to Products page
2. Click "Add New Product"
3. Enter product details
4. Upload product images
5. Set price and stock
6. Click "Save"

**Expected Result**:
- Product created successfully
- Success message displayed
- Product appears in product list

**Actual Result**: [To be filled during testing]
**Status**: [Pass/Fail]
**Comments**: [Any observations]
```

---

## 5. Test Data Management

### 5.1 Test Data Generation

#### Synthetic Data
- **Tool**: Factory Boy, Faker
- **Purpose**: Generate realistic test data
- **Refresh**: Weekly in test environment

#### Example
```python
# factories.py
import factory
from faker import Faker
from core.models import Product, Store, Customer

fake = Faker()

class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store
    
    name = factory.Faker('company')
    subdomain = factory.Faker('slug')
    email = factory.Faker('email')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = factory.Faker('catch_phrase')
    description = factory.Faker('text')
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=0, max=100)
    store = factory.SubFactory(StoreFactory)

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer
    
    name = factory.Faker('name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
```

### 5.2 Data Anonymization

#### Staging Data
- Clone from production (if needed)
- Anonymize personal information
- Mask sensitive data
- Reduce data volume if needed

#### Anonymization Script
```python
# scripts/anonymize_data.py
from core.models import Customer, Order
from faker import Faker

fake = Faker()

def anonymize_customers():
    customers = Customer.objects.all()
    for customer in customers:
        customer.name = fake.name()
        customer.email = fake.email()
        customer.phone = fake.phone_number()
        customer.address = fake.address()
        customer.save()

def anonymize_orders():
    orders = Order.objects.all()
    for order in orders:
        order.shipping_name = fake.name()
        order.shipping_phone = fake.phone_number()
        order.shipping_address = fake.address()
        order.save()

if __name__ == '__main__':
    anonymize_customers()
    anonymize_orders()
    print("Data anonymization completed")
```

### 5.3 Database Reset

#### Reset Script
```bash
#!/bin/bash
# scripts/reset_test_db.sh

echo "Resetting test database..."

# Backup existing data (optional)
pg_dump -h test-db -U testuser wasla_test > backup_$(date +%Y%m%d_%H%M%S).sql

# Drop and recreate database
psql -h test-db -U postgres -c "DROP DATABASE IF EXISTS wasla_test;"
psql -h test-db -U postgres -c "CREATE DATABASE wasla_test OWNER testuser;"

# Run migrations
python manage.py migrate --settings=config.settings.testing

# Load fixtures
python manage.py loaddata test_fixtures.json

# Generate test data
python scripts/generate_test_data.py

echo "Test database reset completed"
```

---

## 6. Quality Assurance Process

### 6.1 QA Workflow

#### Bug Reporting Process
1. **Discovery**: Tester finds issue
2. **Documentation**: Create detailed bug report
3. **Triage**: Prioritize and assign
4. **Fix**: Developer resolves issue
5. **Verification**: Tester verifies fix
6. **Closure**: Issue closed

#### Bug Report Template
```markdown
**Bug ID**: BUG-001
**Title**: Product price displays incorrectly
**Severity**: High
**Priority**: P1
**Environment**: Testing
**Reported By**: QA Team
**Date**: 2026-02-02

**Description**:
Product prices are showing with incorrect decimal places

**Steps to Reproduce**:
1. Navigate to Products page
2. Create product with price 99.99
3. View product in store

**Expected Result**:
Price displays as $99.99

**Actual Result**:
Price displays as $99.9

**Screenshots**: [Attach screenshots]
**Browser**: Chrome 120
**Device**: Desktop
```

### 6.2 Test Case Management

#### Test Case Repository
- Store in version control
- Organize by feature
- Link to user stories
- Track execution results

#### Test Execution Tracking
```markdown
| Test ID | Feature | Status | Last Run | Result |
|---------|---------|--------|----------|--------|
| TC-001 | Login | Active | 2026-02-01 | Pass |
| TC-002 | Product Create | Active | 2026-02-01 | Pass |
| TC-003 | Checkout | Active | 2026-02-02 | Fail |
| TC-004 | Payment | Active | 2026-02-02 | Pass |
```

### 6.3 Regression Testing

#### Automated Regression Suite
- Run nightly on testing environment
- Cover critical user journeys
- Alert on failures
- Track test results over time

#### Regression Test Plan
```yaml
schedule: "0 2 * * *"  # Daily at 2 AM
tests:
  - authentication_suite
  - product_management_suite
  - order_processing_suite
  - payment_suite
  - api_suite

notifications:
  - slack: "#qa-alerts"
  - email: "qa-team@wasla.com"
```

---

## 7. Performance Testing

### 7.1 Load Testing

#### Tools
- **Apache JMeter**
- **Locust**
- **k6**

#### Test Scenarios
1. **Normal Load**: 1,000 concurrent users
2. **Peak Load**: 5,000 concurrent users
3. **Stress Test**: 10,000+ concurrent users
4. **Endurance Test**: 1,000 users for 24 hours

#### Load Test Script (Locust)
```python
# locustfile.py
from locust import HttpUser, task, between

class WaslaUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def browse_products(self):
        self.client.get("/api/products/")
    
    @task(2)
    def view_product(self):
        self.client.get("/api/products/1/")
    
    @task(1)
    def create_order(self):
        self.client.post("/api/orders/", json={
            "products": [{"id": 1, "quantity": 1}],
            "customer": {"name": "Test", "email": "test@test.com"}
        })
```

### 7.2 Performance Metrics

#### Key Performance Indicators
- **Response Time**: p50, p95, p99
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Resource Utilization**: CPU, Memory, Disk I/O

#### Acceptance Criteria
| Metric | Target | Maximum |
|--------|--------|---------|
| Page Load Time | < 2s | < 3s |
| API Response | < 500ms | < 1s |
| Database Query | < 100ms | < 200ms |
| Error Rate | < 0.1% | < 1% |
| CPU Usage | < 70% | < 85% |
| Memory Usage | < 80% | < 90% |

---

## 8. Security Testing

### 8.1 Security Scan Tools

#### Automated Scanning
- **SAST**: Bandit, SonarQube
- **DAST**: OWASP ZAP, Burp Suite
- **Dependency Check**: Safety, Snyk
- **Container Scan**: Trivy, Clair

#### Scan Schedule
```yaml
daily:
  - dependency_check
  - sast_scan

weekly:
  - dast_scan
  - container_scan

monthly:
  - penetration_testing
  - security_audit
```

### 8.2 Security Test Cases

#### Authentication & Authorization
- [ ] Test password strength requirements
- [ ] Test session timeout
- [ ] Test failed login attempts lockout
- [ ] Test privilege escalation
- [ ] Test horizontal privilege access

#### Input Validation
- [ ] SQL injection testing
- [ ] XSS vulnerability testing
- [ ] CSRF token validation
- [ ] File upload security
- [ ] API input validation

#### Data Protection
- [ ] Encryption in transit (SSL/TLS)
- [ ] Encryption at rest
- [ ] Sensitive data masking
- [ ] PCI DSS compliance
- [ ] GDPR compliance

### 8.3 Penetration Testing

#### Scope
- External penetration testing (quarterly)
- Internal penetration testing (annually)
- Third-party security audit (annually)

#### Deliverables
- Detailed findings report
- Risk assessment
- Remediation recommendations
- Re-test after fixes

---

## 9. Monitoring & Logging

### 9.1 Application Monitoring

#### Tools
- **APM**: New Relic, DataDog
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Metrics**: Prometheus + Grafana

#### Metrics to Track
- Application performance
- Error rates
- API latency
- Database performance
- Cache hit rates
- Queue depths

### 9.2 Test Results Dashboard

#### Dashboard Components
- Test execution results
- Code coverage trends
- Performance metrics
- Security scan results
- Bug metrics

---

## 10. Environment Maintenance

### 10.1 Regular Tasks

#### Daily
- Monitor system health
- Check test execution results
- Review error logs

#### Weekly
- Refresh test data
- Update dependencies
- Review test coverage
- Clean up old data

#### Monthly
- Security updates
- Performance review
- Capacity planning
- Cost optimization

### 10.2 Troubleshooting

#### Common Issues
1. **Slow Performance**: Check database queries, cache hit rates
2. **Test Failures**: Check test data, environment configuration
3. **Deployment Issues**: Check CI/CD logs, rollback if needed
4. **Data Issues**: Refresh test data, check data integrity

---

**Document Version:** 1.0  
**Last Updated:** February 2026  
**Next Review:** March 2026
