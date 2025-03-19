# Chaos Testing Incidents & Architectures

## v1.0 AWS Availability Zone (AZ) Outage

### **🧮 Architecture**
```
- VPC (Single AZ)
  - Subnet
    - EC2 (Frontend)
    - EC2 (Backend)
    - EC2 (DB)
    - EC2 (Load Balancer)
```
### **❌ What will go wrong?**
- If **AZ goes down**, all services **fail**.

### **📌 What happened in the actual incident?**
- **Netflix** was unavailable in some regions as AWS **Availability Zone was down**

### **🔧 How it is simulated in ChaosBank?**
- Deploy everything in **a single AZ**.
- Make an AZ unavailable.
- Observe how all services fail.

---

## v2.0 MySQL Connection Limit Misconfiguration

### **🧮 Architecture**
```
- VPC
  - Subnet
    - EC2 (Frontend)
    - EC2 (Backend)
    - EC2 (DB - MySQL, max_connections=10k)
    - EC2 (Load Balancer)
```
### **❌ What will go wrong?**
- Expected **100k users**, but MySQL **can only handle 10k connections**.
- **New connections are rejected**, causing user-facing errors.

### **📌 What happened in the actual incident?**
- DB **hit the connection limit**, causing **massive failures under heavy traffic**.

### **🔧 How it is simulated in ChaosBank?**
- Set MySQL's **max_connections** to an artificially low number.
- Spike user traffic beyond the limit.
- Observe how requests start failing.

---

## v3.0 HAProxy Limit vs. Auto-Scaling Web Servers (Slack Incident)

### **🧮 Architecture**
```
- VPC
  - Subnet
    - EC2 (Frontend)
    - EC2 (Backend)
    - EC2 (DB)
    - EC2 (Load Balancer - HAProxy)
```
### **❌ What will go wrong?**
- Load-Balancer has a **fixed max connections limit**.
- Auto-scaling adds more backend instances **beyond HAProxy's configured limit**.
- New instances **won't receive traffic**, while old/dead instances still do.

### **📌 What happened in the actual incident?**
- Slack scaled up web servers, but Load Balancer (HAProxy) **could not route traffic to them**.
- Users **experienced outages despite additional web servers being available**.

### **🔧 How it is simulated in ChaosBank?**
- HAProxy is configured with a **hard limit** on backends (e.g., max 5 servers in the config, even if 10 are running).
- Auto Scaling spawns **more backend instances**, but HAProxy **ignores them**.
- Traffic remains **stuck on old instances**, leading to **downtime**.

---

## v4.0 DB unavailable on Primary DB Kill

### **🧮 Architecture**
```
- VPC
  - Subnet
    - EC2 (Frontend)
    - EC2 (Backend)
    - EC2 (DB - Primary)
    - EC2 (DB - Replica)
```
### **❌ What will go wrong?**
- Primary DB goes **down unexpectedly**.
- The replica is **not promoted** properly.
- **Application queries fail**.

### **🔧 How it is simulated in ChaosBank?**
- Kill the **primary DB instance**.
- Ensure the replica **does not automatically take over**.
- Observe how requests start failing.

---


## v5.0 Inconsistent Slave Becomes Primary (GitHub DB Incident)

### **🧮 Architecture**
```
- VPC
  - Subnet
    - EC2 (Frontend)
    - EC2 (Backend)
    - EC2 (DB - Primary)
    - EC2 (DB - Replica, stale data)
```
### **❌ What will go wrong?**
- **Failover promotes an inconsistent replica**.
- **Stale data** becomes the primary DB.

### **📌 What happened in the actual incident?**
- GitHub **promoted a stale replica**, causing **data corruption**.

### **🔧 How it is simulated in ChaosBank?**
- Delay **replication sync**.
- Force failover to an **inconsistent replica**.
- Observe how old/stale data gets used.

---

## v6.0 DB Partitioning (User vs. Transaction DB Split)

### **🧮 Architecture**
```
- VPC
  - Subnet
    - EC2 (Frontend)
    - EC2 (Backend)
    - EC2 (DB - Users)
    - EC2 (DB - Transactions)
```
### **❌ What will go wrong?**
- **User DB fails**, but **Transaction DB still processes transactions**.
- **Balances become inconsistent**.

### **📌 What happened in the actual incident?**
- Transactions **happened without User DB**, causing **balance mismatches**.

### **🔧 How it is simulated in ChaosBank?**
- Kill the **User DB** while allowing transactions.
- Observe how balances **become inconsistent**.

---

