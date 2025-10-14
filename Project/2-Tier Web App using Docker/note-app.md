# **Notes App Project — SOP (Updated with Resources)**

* * *

## **Project Overview**

**Project Name:** Notes App – Two-Tier Web Application (AWS)

**Objective:**  
Develop a **secure, two-tier notes saving web application** using **Docker, Flask, Nginx, and MySQL**, hosted on **AWS EC2**, accessible via an **Application Load Balancer (ALB)**, and storing persistent data.

**Architecture:**

-   **Tier 1:** Flask + Nginx (Application Layer)
    
-   **Tier 2:** MySQL (Database Layer)
    
-   **ALB:** Public entry point → Private EC2 → Docker containers
    
-   **Private EC2:** No public IP, access via **AWS Systems Manager (SSM)**
    

**Technologies Used:**

-   AWS EC2, VPC, Security Groups, ALB
    
-   Docker & Docker Compose
    
-   Flask (Python)
    
-   MySQL 5.7 (Dockerized)
    
-   Nginx (Dockerized)
    
-   HTML/CSS (AWS-themed UI: White + Orange)
    

**Screenshots:**

-   UI Screenshot → `screenshots/notes-ui.png` <img width="1440" height="503" alt="image" src="https://github.com/user-attachments/assets/0aa3a5f6-47ea-4916-a73e-679f0487e501" />

    
-   Architecture Diagram → `screenshots/architecture.png`
    

* * *

## **Step 1 — AWS EC2 Setup**

1.  Launch **EC2 instance** in **private subnet** (no public IP)
    
    **Resource Details:**
    
    -   **Instance ID:** `i-0179a0233ed5ae485`
        
    -   **Instance Name:** `jatin-notes-app-instance`
        
    -   **IAM Role:** `Jatin-EC2-Role`
        
    -   **Security Group:** `sg-0b291f899827c571f` (`jatin-ec2-sg`)
        
2.  Configure **Security Group**:
    
    -   Inbound: HTTP 80 → ALB Security Group
        
    -   Outbound: All traffic
        
3.  Connect via **AWS SSM**:
    

`aws ssm start-session --target i-0179a0233ed5ae485`

**Screenshot placeholder:** `screenshots/ec2-setup.png`

* * *

## **Step 2 — Application Load Balancer (ALB)**

1.  **ALB Name:** `jatin-notes-alb`
    
2.  **ALB Security Group:** `sg-008fd6af212588aed`
    
3.  Internet-facing ALB in **public subnet**
    
4.  Target group: register **private EC2 instance (`jatin-notes-app-instance`)**
    
5.  Health check path: `/`
    

**Screenshot placeholder:** `screenshots/alb-setup.png`

* * *

## **Step 3 — Install Docker & Docker Compose**

`sudo apt update -y sudo apt install -y docker.io sudo systemctl enable --now docker sudo usermod -aG docker $USER  sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose sudo chmod +x /usr/local/bin/docker-compose`

-   Verify installation:
    

`docker --version docker-compose --version`

**Screenshot placeholder:** `screenshots/docker-install.png`

* * *

## **Step 4 — Project Folder & Files**

Create the project structure:

`notes-app/ ├── app/ │   ├── app.py │   ├── requirements.txt │   └── templates/index.html ├── db/init.sql ├── nginx/default.conf ├── Dockerfile ├── docker-compose.yml └── README.md`

**Screenshot placeholder:** `screenshots/project-structure.png`

* * *

## **Step 5 — Flask Application**

**app/app.py**

-   Flask app with POST form to save notes
    
-   Connects to MySQL database using environment variables
    

**app/requirements.txt**

-   Dependencies: `flask`, `mysql-connector-python`
    

**app/templates/index.html**

-   Modern **AWS-themed UI** (White + Orange)
    
-   Responsive, clean design
    
-   Screenshot: `screenshots/notes-ui.png`
    

* * *

## **Step 6 — MySQL Database**

**db/init.sql**

`CREATE DATABASE IF NOT EXISTS notesdb; USE notesdb; CREATE TABLE IF NOT EXISTS notes (   id INT AUTO_INCREMENT PRIMARY KEY,   content TEXT,   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );`

-   Docker volume `mysql_data` ensures **persistent storage**
    
-   Environment variables set root password and database name
    

**Screenshot placeholder:** `screenshots/mysql-setup.png`

* * *

## **Step 7 — Nginx Configuration**

**nginx/default.conf**

`server {     listen 80;     location / {         proxy_pass http://flask_app:5000;         proxy_set_header Host $host;         proxy_set_header X-Real-IP $remote_addr;         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;     } }`

-   Acts as **reverse proxy** to Flask app container
    
-   Handles HTTP requests from ALB
    

**Screenshot placeholder:** `screenshots/nginx-setup.png`

* * *

## **Step 8 — Dockerfile & Docker Compose**

**Dockerfile (Flask App)**

-   Base: `python:3.9-slim`
    
-   Copies `app/` folder
    
-   Installs dependencies
    
-   Runs Flask on port 5000
    

**docker-compose.yml**

-   Services: `flask_app`, `nginx`, `mysql_db`
    
-   Networks: `app-network`
    
-   Volumes:
    
    -   `./app:/app` → live updates for Flask app
        
    -   `mysql_data:/var/lib/mysql` → persistent MySQL data
        

**Screenshot placeholder:** `screenshots/docker-compose.png`

* * *

## **Step 9 — Deploy Application**

1.  Start services:
    

`cd ~/notes-app sudo docker-compose up -d --build`

2.  Verify containers:
    

`sudo docker ps`

3.  Access app using **ALB DNS**:
    

`http://jatin-notes-alb-437994785.us-west-2.elb.amazonaws.com`

4.  Save notes → verify database:
    

`sudo docker exec -it mysql_db mysql -uroot -prootpassword -e "USE notesdb; SELECT * FROM notes;"`

**Screenshot placeholder:** `screenshots/app-running.png`

* * *

## **Step 10 — Reset / Start Fresh**

-   Clear all notes:
    

`sudo docker exec -it mysql_db mysql -uroot -prootpassword -e "USE notesdb; TRUNCATE TABLE notes;"`

-   Or recreate database volume:
    

`sudo docker-compose down sudo docker volume rm notes-app_mysql_data sudo docker-compose up -d`

**Screenshot placeholder:** `screenshots/reset-app.png`
