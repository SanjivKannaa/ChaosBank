# 📦 ChaosBank - Features To Be Implemented

A distributed, scalable, chaos-resilient fintech application built for DevOps and distributed systems showcase.

---

## 🏗️ Infrastructure

- [x] Provision all infrastructure using **Terraform**
- [ ] Use **AWS ALB** for load balancing and routing
- [ ] Setup **multi-AZ deployment** for high availability
- [ ] Use **AWS S3** to serve static frontend

---

## 🧱 Containerization & Orchestration

- [x] Containerize all services using **Docker**
- [ ] Use **Kubernetes on AWS EKS** for orchestration

---

## 🗃️ Storage & Databases

- [ ] Setup **MySQL Master-Slave Replication**
- [ ] Schedule automatic **MySQL backups to S3**
- [ ] Setup **Read Replicas** for scalable reads

---

## 🔄 DevOps / CI-CD

- [ ] Setup **CI/CD** pipeline
- [ ] Enable **zero-downtime deployments**
- [ ] Push Docker images to **Amazon ECR**

---

## 📈 Monitoring & Observability

- [ ] Use **AWS Managed Prometheus** for metrics collection
- [ ] Visualize system metrics using **Grafana Dashboards**
- [ ] Integrate **AWS CloudWatch** for logs and alarms
- [ ] Setup **alerting** (PagerDuty, Slack, or email)
- [ ] Enable **distributed tracing** using OpenTelemetry / Jaeger

---

## 💥 Load & Fault Testing

- [ ] Simulate **10k–50k concurrent users** with **k6**
- [ ] Perform **stress/load testing** on all critical services
- [ ] Compare system behavior **before/after chaos events**
- [ ] Validate **Auto Scaling** triggers under load

---

## 🔐 Security & Resilience

- [ ] Secure services using **IAM roles**, **VPC security groups**
- [ ] Enforce **HTTPS**
- [ ] Add **Rate Limiting** and **Request Throttling**

---
