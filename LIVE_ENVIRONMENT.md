# Live Environment Specification
# Wasla E-commerce Platform

**Version:** 1.0  
**Date:** February 2026  
**Environment Type:** Production

---

## Table of Contents
1. [Production Environment Overview](#1-production-environment-overview)
2. [Infrastructure Architecture](#2-infrastructure-architecture)
3. [Deployment Strategy](#3-deployment-strategy)
4. [Monitoring & Alerting](#4-monitoring--alerting)
5. [Disaster Recovery](#5-disaster-recovery)
6. [Security & Compliance](#6-security--compliance)
7. [Performance & Scalability](#7-performance--scalability)
8. [Maintenance & Support](#8-maintenance--support)

---

## 1. Production Environment Overview

### 1.1 Service Level Objectives (SLOs)

#### Availability
- **Uptime Target**: 99.9% (8.76 hours downtime per year)
- **Monthly Downtime Budget**: 43.2 minutes
- **Planned Maintenance Window**: Sundays 2-4 AM UTC

#### Performance
- **Page Load Time**: < 2 seconds (p95)
- **API Response Time**: < 500ms (p95)
- **Database Query Time**: < 100ms (p95)
- **Time to First Byte**: < 300ms

#### Capacity
- **Concurrent Users**: 50,000+
- **Requests per Second**: 10,000+
- **Database TPS**: 5,000+
- **Storage**: Unlimited (auto-scaling)

### 1.2 Environment Characteristics

- **Region**: Multi-region deployment (Primary + DR)
- **Auto-scaling**: Enabled based on CPU and request metrics
- **High Availability**: Multi-AZ deployment
- **Disaster Recovery**: Cross-region replication
- **CDN**: Global content delivery
- **SSL/TLS**: Required for all connections

---

## 2. Infrastructure Architecture

### 2.1 Compute Infrastructure

#### Application Servers
```yaml
Production:
  Auto Scaling Group:
    Min: 10 instances
    Max: 100 instances
    Desired: 15 instances
    Instance Type: c5.2xlarge
    CPU: 8 vCPUs
    Memory: 16GB RAM
    Scaling Metrics:
      - CPU > 70%
      - Requests per second > 1000
      - Response time > 500ms
```

#### Container Orchestration
```yaml
Kubernetes Cluster:
  Control Plane: Managed (EKS/GKE)
  Worker Nodes: 20-200 nodes
  Node Type: c5.2xlarge
  Namespaces:
    - production
    - monitoring
    - logging
  
  Deployments:
    web-app:
      replicas: 15-50
      resources:
        requests:
          cpu: 1000m
          memory: 2Gi
        limits:
          cpu: 2000m
          memory: 4Gi
      health_checks:
        liveness: /health/live
        readiness: /health/ready
    
    api-server:
      replicas: 20-60
      resources:
        requests:
          cpu: 1500m
          memory: 3Gi
        limits:
          cpu: 3000m
          memory: 6Gi
    
    worker:
      replicas: 10-30
      resources:
        requests:
          cpu: 1000m
          memory: 2Gi
```

### 2.2 Database Architecture

#### PostgreSQL Primary Cluster
```yaml
Primary Database:
  Instance Type: db.r5.4xlarge
  vCPUs: 16
  Memory: 128GB
  Storage: 2TB SSD (gp3)
  IOPS: 16,000
  Multi-AZ: Yes
  
Read Replicas:
  Count: 3
  Instance Type: db.r5.2xlarge
  vCPUs: 8
  Memory: 64GB
  Storage: 2TB SSD (gp3)
  Lag Threshold: < 5 seconds
  
Backup:
  Automated: Daily at 3 AM UTC
  Retention: 30 days
  Point-in-Time Recovery: 7 days
  Cross-Region Backup: Yes
  
Configuration:
  max_connections: 1000
  shared_buffers: 32GB
  effective_cache_size: 96GB
  maintenance_work_mem: 2GB
  checkpoint_completion_target: 0.9
  wal_buffers: 16MB
  default_statistics_target: 100
  random_page_cost: 1.1
  effective_io_concurrency: 200
```

#### Database Sharding Strategy
```yaml
Sharding:
  Type: Horizontal
  Shard Key: store_id
  Shards: 8 (initial), auto-scale to 64
  Routing: Application-level
  
Shard Distribution:
  - Shard 1-4: Primary region
  - Shard 5-8: DR region
```

### 2.3 Caching Layer

#### Redis Cluster
```yaml
Primary Cache Cluster:
  Nodes: 6 (3 master + 3 replica)
  Instance Type: cache.r5.2xlarge
  Memory per Node: 52GB
  Total Memory: 312GB
  Eviction Policy: allkeys-lru
  Persistence: AOF + RDB
  
Session Store:
  Nodes: 3 (1 master + 2 replica)
  Instance Type: cache.r5.xlarge
  Memory per Node: 26GB
  TTL: 24 hours
  
Configuration:
  maxmemory-policy: allkeys-lru
  timeout: 300
  tcp-keepalive: 60
  maxclients: 50000
```

### 2.4 Search Infrastructure

#### Elasticsearch Cluster
```yaml
Production Cluster:
  Master Nodes: 3
    Instance: r5.xlarge.elasticsearch
    Memory: 16GB per node
  
  Data Nodes: 6
    Instance: r5.2xlarge.elasticsearch
    Memory: 32GB per node
    Storage: 500GB SSD per node
  
  Configuration:
    indices.memory.index_buffer_size: 30%
    indices.queries.cache.size: 10%
    thread_pool.write.queue_size: 1000
  
  Backup:
    Snapshots: Daily
    Retention: 14 days
    Repository: S3
```

### 2.5 Message Queue

#### RabbitMQ Cluster
```yaml
Message Queue:
  Nodes: 3
  Instance Type: t3.large
  Memory: 8GB per node
  Disk: 100GB per node
  
  Queues:
    - email-queue (priority)
    - sms-queue (priority)
    - order-processing (critical)
    - reports-generation (low)
    - webhooks (normal)
  
  Configuration:
    max_connections: 5000
    heartbeat: 60
    vm_memory_high_watermark: 0.7
```

### 2.6 Storage & CDN

#### Object Storage (S3)
```yaml
Buckets:
  media-assets:
    Lifecycle: Never expire
    Encryption: AES-256
    Versioning: Enabled
    Replication: Cross-region
    Size: Unlimited
  
  backups:
    Lifecycle: 90 days
    Encryption: AES-256
    Versioning: Enabled
    Size: Unlimited
  
  logs:
    Lifecycle: 30 days
    Compression: gzip
    Size: Unlimited
```

#### CDN (CloudFlare)
```yaml
CDN Configuration:
  Locations: Global (200+ PoPs)
  SSL: Full (strict)
  HTTP/2: Enabled
  HTTP/3 (QUIC): Enabled
  Compression: Brotli + gzip
  
  Caching Rules:
    Static Assets:
      TTL: 365 days
      Types: .jpg, .png, .css, .js, .woff2
    
    API Responses:
      TTL: 60 seconds
      Cache-Control: respected
    
    HTML Pages:
      TTL: 5 minutes
      Edge-cache: Enabled
  
  Security:
    WAF: Enabled
    DDoS Protection: Enabled
    Rate Limiting: 100 req/sec per IP
    Bot Management: Enabled
```

### 2.7 Load Balancing

#### Application Load Balancer
```yaml
Load Balancer:
  Type: Application Load Balancer
  Scheme: Internet-facing
  Availability Zones: 3
  
  Listeners:
    HTTP (80):
      Action: Redirect to HTTPS
    
    HTTPS (443):
      SSL Policy: ELBSecurityPolicy-TLS-1-2-2017-01
      Certificates: ACM managed
      Target Group: application-servers
  
  Health Checks:
    Protocol: HTTPS
    Path: /health/
    Interval: 30 seconds
    Timeout: 5 seconds
    Healthy Threshold: 2
    Unhealthy Threshold: 3
  
  Connection Settings:
    Idle Timeout: 60 seconds
    Deregistration Delay: 30 seconds
```

---

## 3. Deployment Strategy

### 3.1 Deployment Process

#### Blue-Green Deployment
```yaml
Deployment Strategy: Blue-Green

Process:
  1. Deploy new version to Green environment
  2. Run smoke tests on Green
  3. Gradually shift traffic (10% -> 50% -> 100%)
  4. Monitor metrics and errors
  5. Complete switch or rollback
  6. Keep Blue for 24 hours before decommission

Traffic Shifting:
  - 10% for 30 minutes
  - 50% for 30 minutes
  - 100% if no issues
```

#### Canary Deployment
```yaml
Canary Deployment:
  Initial Canary: 5% traffic
  Duration: 1 hour
  Metrics to Monitor:
    - Error rate < 0.1%
    - Response time < 500ms
    - CPU usage < 80%
  
  Progression:
    - 5% -> 10% -> 25% -> 50% -> 100%
    - Each stage: 30 minutes
  
  Rollback Triggers:
    - Error rate > 1%
    - Response time > 1s
    - Customer complaints
```

### 3.2 CI/CD Pipeline

#### Production Pipeline
```yaml
stages:
  - security_scan
  - build
  - test
  - staging_deploy
  - production_approval
  - production_deploy
  - health_check
  - smoke_test

security_scan:
  - SAST (Bandit, SonarQube)
  - Dependency check (Safety, Snyk)
  - Container scan (Trivy)
  - Secret detection (GitGuardian)

build:
  - Build Docker image
  - Tag with version and SHA
  - Push to container registry
  - Sign images

test:
  - Unit tests
  - Integration tests
  - API tests
  - Performance tests

staging_deploy:
  - Deploy to staging
  - Run full test suite
  - Manual QA verification

production_approval:
  - Require approvals from:
    - Tech Lead
    - Product Manager
    - On-call Engineer

production_deploy:
  - Blue-green deployment
  - Gradual traffic shift
  - Automated rollback on failure

health_check:
  - Verify all services healthy
  - Check database connectivity
  - Verify cache connectivity
  - Check external integrations

smoke_test:
  - Critical user flows
  - API health checks
  - Payment processing test
  - Email sending test
```

### 3.3 Rollback Procedure

#### Automated Rollback
```yaml
Rollback Triggers:
  - Error rate > 1% for 5 minutes
  - Response time > 2s for 5 minutes
  - Health check failures > 20%
  - Critical service down

Rollback Process:
  1. Stop new deployment
  2. Route all traffic to previous version
  3. Alert on-call team
  4. Create incident
  5. Investigate and fix
```

#### Manual Rollback
```bash
# Rollback script
./scripts/rollback.sh <version>

# Example
./scripts/rollback.sh v2.3.1

# Process:
# 1. Confirm rollback version
# 2. Update deployment
# 3. Monitor health
# 4. Notify team
```

---

## 4. Monitoring & Alerting

### 4.1 Monitoring Stack

#### Application Performance Monitoring (APM)
```yaml
APM Tool: New Relic / DataDog

Metrics:
  - Response time (p50, p95, p99)
  - Throughput (requests/sec)
  - Error rate
  - Apdex score
  - Transaction traces
  - Database queries
  - External services

Dashboards:
  - Real-time overview
  - Service health
  - Database performance
  - API analytics
  - Business metrics
```

#### Infrastructure Monitoring
```yaml
Tool: Prometheus + Grafana

Metrics:
  System:
    - CPU usage
    - Memory usage
    - Disk I/O
    - Network traffic
  
  Application:
    - Active connections
    - Request queue depth
    - Cache hit rate
    - Worker queue size
  
  Database:
    - Connections
    - Queries per second
    - Replication lag
    - Table sizes
  
  Cache:
    - Hit/miss ratio
    - Evictions
    - Memory usage
    - Latency
```

#### Log Management
```yaml
ELK Stack:
  Elasticsearch:
    Nodes: 6
    Storage: 2TB per node
    Retention: 30 days
  
  Logstash:
    Workers: 4
    Pipeline: Grok parsing, enrichment
  
  Kibana:
    Dashboards: 15+
    Saved Searches: 50+
  
Log Sources:
  - Application logs (JSON format)
  - Access logs (Nginx)
  - Error logs
  - Audit logs
  - Security logs
```

### 4.2 Alerting

#### Alert Rules
```yaml
Critical Alerts (Immediate Response):
  - Service down
  - Database connection failure
  - Payment processing failure
  - Error rate > 5%
  - Response time > 5s
  - Disk space < 10%

High Priority (Response within 30 min):
  - Error rate > 1%
  - Response time > 2s
  - CPU usage > 90%
  - Memory usage > 90%
  - Database replication lag > 60s
  - Failed deployments

Medium Priority (Response within 4 hours):
  - Error rate > 0.5%
  - Response time > 1s
  - CPU usage > 80%
  - Cache hit rate < 80%
  - Disk space < 20%

Low Priority (Response within 24 hours):
  - Performance degradation
  - Minor errors
  - Capacity warnings
  - Cost anomalies
```

#### Alert Channels
```yaml
Channels:
  PagerDuty:
    - Critical alerts
    - High priority alerts
    - On-call escalation
  
  Slack:
    - All alerts
    - Deployment notifications
    - Performance warnings
  
  Email:
    - Daily summaries
    - Weekly reports
    - Scheduled maintenance
  
  SMS:
    - Critical alerts only
    - For on-call team
```

### 4.3 On-Call Rotation

#### Schedule
```yaml
On-Call Rotation:
  Primary: 1 week rotation
  Secondary: 1 week rotation
  
  Coverage: 24/7
  
  Escalation:
    Level 1: Primary on-call (immediate)
    Level 2: Secondary on-call (15 min)
    Level 3: Engineering Manager (30 min)
    Level 4: CTO (1 hour)

Compensation:
  - On-call allowance
  - Overtime pay for incidents
  - Time-off in lieu
```

---

## 5. Disaster Recovery

### 5.1 Backup Strategy

#### Database Backups
```yaml
Automated Backups:
  Frequency: Every 6 hours
  Retention: 30 days
  Storage: Cross-region S3
  Encryption: AES-256
  
Point-in-Time Recovery:
  Window: 7 days
  Granularity: 1 second
  
Manual Backups:
  Before: Major deployments
  Before: Data migrations
  Retention: 90 days
```

#### Application State Backups
```yaml
Configuration Backups:
  Frequency: On every change
  Storage: Git repository
  Versioned: Yes

Media Backups:
  Frequency: Real-time replication
  Storage: Cross-region S3
  Versioning: Enabled
```

### 5.2 Disaster Recovery Plan

#### Recovery Time Objective (RTO)
- **RTO Target**: 1 hour
- **Recovery Point Objective (RPO)**: 15 minutes

#### DR Regions
```yaml
Primary Region: us-east-1
DR Region: us-west-2

Data Replication:
  Database: Continuous replication
  Object Storage: Cross-region replication
  Elasticsearch: Snapshot + restore
  Redis: AOF + RDB backups

Failover Process:
  1. Detect primary region failure
  2. Confirm data consistency in DR
  3. Update DNS to DR region
  4. Start services in DR region
  5. Verify application health
  6. Notify stakeholders
  
Failover Time: < 1 hour
```

#### DR Testing
```yaml
Testing Schedule:
  Full DR Drill: Quarterly
  Partial Failover Test: Monthly
  Backup Restore Test: Weekly

Scenarios:
  - Complete region failure
  - Database failure
  - Application failure
  - Network partition
  - Data corruption
```

---

## 6. Security & Compliance

### 6.1 Security Measures

#### Network Security
```yaml
VPC Configuration:
  Public Subnets: Load balancers only
  Private Subnets: Application servers
  Data Subnets: Databases, cache (isolated)
  
Security Groups:
  - Allow only necessary ports
  - Restrict by IP/CIDR
  - Deny by default
  
Network ACLs:
  - Stateless firewall
  - Additional layer of security
  
VPN:
  - Required for administrative access
  - Multi-factor authentication
  - IP whitelisting
```

#### Application Security
```yaml
Web Application Firewall (WAF):
  Provider: CloudFlare WAF
  Rules:
    - OWASP Top 10 protection
    - SQL injection prevention
    - XSS prevention
    - Rate limiting (100 req/sec)
    - Bot protection
    - Geo-blocking (if needed)

DDoS Protection:
  Provider: CloudFlare
  Protection Level: Enterprise
  Always On: Yes
  
SSL/TLS:
  Minimum Version: TLS 1.2
  Certificate: Wildcard + SAN
  HSTS: Enabled
  Perfect Forward Secrecy: Yes
```

#### Data Security
```yaml
Encryption:
  At Rest:
    - Database: AES-256
    - Object Storage: AES-256
    - Backups: AES-256
  
  In Transit:
    - External: TLS 1.2+
    - Internal: TLS 1.2+ (optional)
  
Secrets Management:
  Tool: AWS Secrets Manager / HashiCorp Vault
  Rotation: Automatic (90 days)
  Access: IAM roles only
  Audit: All access logged
```

### 6.2 Compliance

#### PCI DSS Compliance
```yaml
Requirements:
  - No storage of CVV/CVC
  - Tokenization of card data
  - Annual security audit
  - Quarterly network scans
  - Penetration testing
  - Access logging
  
Payment Processing:
  - Use PCI-compliant gateway
  - Never log card numbers
  - Encrypted transmission
  - Secure storage (if needed)
```

#### GDPR Compliance
```yaml
Data Protection:
  - Data encryption
  - Access controls
  - Data minimization
  - Purpose limitation
  
User Rights:
  - Right to access
  - Right to be forgotten
  - Right to data portability
  - Right to rectification
  
Processes:
  - Data processing agreement
  - Privacy policy
  - Cookie consent
  - Data breach notification (72h)
```

#### SOC 2 Compliance
```yaml
Type II Audit:
  Frequency: Annual
  Criteria:
    - Security
    - Availability
    - Confidentiality
    - Processing Integrity
  
Controls:
  - Access management
  - Change management
  - System operations
  - Risk mitigation
```

---

## 7. Performance & Scalability

### 7.1 Auto-scaling Rules

#### Application Servers
```yaml
Scale Up Triggers:
  - CPU > 70% for 5 minutes
  - Requests/sec > 1000
  - Response time > 500ms
  
Scale Down Triggers:
  - CPU < 30% for 15 minutes
  - Requests/sec < 300
  
Scaling Policy:
  Type: Target tracking
  Target: 70% CPU
  Cool down: 5 minutes
  
Limits:
  Min: 10 instances
  Max: 100 instances
  Step: 5 instances
```

#### Database Read Replicas
```yaml
Scale Up Triggers:
  - Read connections > 80%
  - CPU > 75%
  - Replication lag > 10s
  
Auto-scaling:
  Min replicas: 3
  Max replicas: 10
  Step: 1 replica
```

### 7.2 Performance Optimization

#### Database Optimization
```yaml
Indexing:
  - Index all foreign keys
  - Index frequently queried fields
  - Composite indexes for complex queries
  - Regular index analysis

Query Optimization:
  - Use EXPLAIN for slow queries
  - Optimize N+1 queries
  - Use connection pooling (pgBouncer)
  - Read replicas for read-heavy operations

Caching Strategy:
  Database: Query result caching
  Application: Page caching, fragment caching
  CDN: Static asset caching
```

#### Application Optimization
```yaml
Code Optimization:
  - Lazy loading
  - Async processing
  - Background jobs
  - Database query optimization
  - N+1 query prevention

Resource Optimization:
  - Image compression
  - CSS/JS minification
  - Gzip compression
  - HTTP/2 multiplexing
  - Resource hints (preconnect, prefetch)
```

---

## 8. Maintenance & Support

### 8.1 Maintenance Windows

#### Scheduled Maintenance
```yaml
Schedule:
  Day: Sunday
  Time: 2:00 AM - 4:00 AM UTC
  Frequency: Monthly
  
Notification:
  Advance Notice: 7 days
  Channels: Email, in-app notification, status page
  
Activities:
  - Security updates
  - Database maintenance
  - Infrastructure upgrades
  - Performance tuning
```

### 8.2 Support Tiers

#### Customer Support
```yaml
Tier 1: Self-service
  - Knowledge base
  - Documentation
  - Video tutorials
  - Community forum

Tier 2: Email Support
  - Response time: 24 hours
  - Business hours: 9 AM - 6 PM
  - Languages: English, Arabic

Tier 3: Priority Support
  - Response time: 4 hours
  - 24/7 availability
  - Dedicated support engineer
  - Phone support

Enterprise: White-glove
  - Response time: 1 hour
  - 24/7/365 availability
  - Dedicated account manager
  - On-site support (if needed)
```

### 8.3 Incident Management

#### Incident Response Process
```yaml
1. Detection:
   - Automated alerting
   - User reports
   - Monitoring systems

2. Triage:
   - Severity assessment
   - Impact analysis
   - Team assignment

3. Response:
   - Immediate mitigation
   - Root cause analysis
   - Communication

4. Resolution:
   - Implement fix
   - Verify solution
   - Deploy to production

5. Post-mortem:
   - Incident report
   - Lessons learned
   - Action items
```

---

## 9. Cost Optimization

### 9.1 Cost Monitoring
```yaml
Tools:
  - AWS Cost Explorer
  - CloudHealth
  - Custom dashboards

Budgets:
  Monthly: $50,000
  Alerts: 80%, 90%, 100%
  
Cost Allocation:
  - By service
  - By environment
  - By team
```

### 9.2 Optimization Strategies
```yaml
Compute:
  - Reserved instances (1-3 years)
  - Spot instances for batch jobs
  - Right-sizing instances

Storage:
  - Lifecycle policies
  - Compression
  - S3 Intelligent-Tiering

Database:
  - Reserved instances
  - Read replica optimization
  - Archive old data
```

---

**Document Version:** 1.0  
**Last Updated:** February 2026  
**Next Review:** March 2026
