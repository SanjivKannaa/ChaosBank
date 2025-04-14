# Chaos Testing Incidents & Architectures

## v1.0 Single AZ deployment.

### **🧮 Architecture**

```
- VPC (Single AZ)
  - Subnet (ap-south-1)
    - Load Balancer (EC2)
    - Frontend1 (EC2)
    - Frontend2 (EC2)
    - Backend1 (EC2)
    - Backend2 (EC2)
    - DB (EC2)
```

### **❌ What will go wrong?**

- If one both instances of **frontend/backend** fail, **entire application goes down**.
- If **database/load balancer** goes down, **entire application goes down**.

---

## v2.0 Multi AZ deployment with DB replication.

### **🧮 Architecture**

```
- VPC (multiple AZ)
  - Subnet 1 (ap-south-1)
    - Load Balancer (EC2)
    - Frontend (Auto Scale Group (1, 2, 4))
        - Frontend1 (EC2)
        - Frontend2 (EC2)
        - ...
    - Backend (Auto Scale Group (1, 2, 4))
        - Backend1 (EC2)
        - Backend2 (EC2)
        - ...
    - DB (EC2)
```

---
