# 🚀 DevOps Final Project — Flask Notes App with Docker, AWS RDS, Terraform & Jenkins CI/CD

## 📌 Overview

This project demonstrates a **production-like DevOps workflow** where a Flask application is containerized using Docker, connected to an AWS RDS database, provisioned using Terraform, and deployed automatically via a Jenkins CI/CD pipeline.

It showcases real-world DevOps practices including:

* Infrastructure as Code (Terraform)
* Containerization (Docker)
* Cloud Database (AWS RDS)
* CI/CD Automation (Jenkins)
* Deployment on AWS EC2

---

## 🧱 Architecture

```
GitHub → Jenkins → Docker → EC2 → Flask App → AWS RDS (MySQL)
```

---

## ⚙️ Tech Stack

* **Backend**: Flask (Python)
* **Database**: MySQL (AWS RDS)
* **Containerization**: Docker
* **CI/CD**: Jenkins
* **Infrastructure**: Terraform
* **Cloud Provider**: AWS (EC2, RDS, VPC, Security Groups)

## 🚀 Features

* Add and delete notes via Flask web UI
* Persistent storage using AWS RDS
* Retry logic for database connection handling
* Fully containerized application
* Automated CI/CD pipeline with Jenkins
* Infrastructure provisioning using Terraform

---

## ⚙️ Setup & Deployment

### 🔹 1. Clone Repository

```bash
git clone https://github.com/Soumi-Pandit12/devops-final-project.git
cd DevOps-Final-Project
```

---

### 🔹 2. Provision Infrastructure (Terraform)

```bash
cd terraform
terraform init
terraform apply
```

This creates:

* VPC
* Subnets
* Security Groups
* EC2 Instance
* RDS MySQL Database

---

### 🔹 3. Build Docker Image

```bash
docker build -t flask-app .
```

---

### 🔹 4. Run Application (Local or EC2)

```bash
docker run -d \
  -p 5000:5000 \
  -e MYSQL_HOST=<RDS_ENDPOINT> \
  -e MYSQL_USER=admin \
  -e MYSQL_PASSWORD=<DB_PASSWORD> \
  -e MYSQL_DB=mydb \
  flask-app
```

---

### 🔹 5. Access Application

```
http://localhost:5000
```

OR (on EC2):

```
http://<EC2_PUBLIC_IP>:5000
```

---

## 🔄 Jenkins CI/CD Pipeline

The Jenkins pipeline automates:

1. Clone code from GitHub
2. Build Docker image
3. Stop existing container
4. Deploy updated container


## 🔐 Security Considerations

* Sensitive values (DB password) should be stored in:

  * Jenkins Credentials Manager
  * Environment variables (not hardcoded)
* Avoid exposing ports publicly in production
* Use IAM roles instead of hardcoded credentials

---

## 🧠 Key Learnings

* How Docker containers interact with cloud databases (RDS)
* Managing infrastructure using Terraform
* Debugging real-world networking & security group issues
* Building CI/CD pipelines with Jenkins
* Handling environment variables in containerized apps

---

## 🚀 Future Improvements

* Use Docker Hub for image storage
* Add Nginx reverse proxy
* Implement HTTPS with domain
* Use Kubernetes for orchestration
* Add monitoring (Prometheus + Grafana)

---

## 👨‍💻 Author

**Soumi Pandit**
GitHub: https://github.com/Soumi-Pandit12

---

## ⭐ If you found this useful, give it a star!
