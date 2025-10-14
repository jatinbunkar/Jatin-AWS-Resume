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

-   UI Screenshot →  <img width="1440" height="503" alt="image" src="https://github.com/user-attachments/assets/0aa3a5f6-47ea-4916-a73e-679f0487e501" />

    
-   Architecture Diagram → <img width="808" height="804" alt="image" src="https://github.com/user-attachments/assets/e545b803-5cdd-457f-b7ae-7d5775959223" />

    

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
        
3.  Connect via **AWS Session Manager**:

    


**Screenshot placeholder:** <img width="1273" height="685" alt="image" src="https://github.com/user-attachments/assets/4c0e99a2-5cec-4680-93f8-c75e196591ce" />

* * *

## **Step 2 — Application Load Balancer (ALB)**

1.  **ALB Name:** `jatin-notes-alb`
    
2.  **ALB Security Group:** `sg-008fd6af212588aed`
    
3.  Internet-facing ALB in **public subnet**
    
4.  Target group: register **private EC2 instance (`jatin-notes-app-instance`)**
    
5.  Health check path: `/`
    

**Screenshot placeholder:** <img width="1237" height="660" alt="image" src="https://github.com/user-attachments/assets/5d93467b-4857-4343-9b5a-9c36064c8096" />


* * *

## **Step 3 — Install Docker & Docker Compose**

`sudo apt update -y sudo apt install -y docker.io sudo systemctl enable --now docker sudo usermod -aG docker $USER  sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose sudo chmod +x /usr/local/bin/docker-compose`

-   Verify installation:
    

`docker --version docker-compose --version`

**Screenshot placeholder:** <img width="944" height="758" alt="image" src="https://github.com/user-attachments/assets/2418b317-02c2-45cc-9704-703bd3eeaf68" />
<img width="631" height="426" alt="image" src="https://github.com/user-attachments/assets/4bceb201-c1e2-4e66-adc6-b0bd5527ff36" />



* * *

## **Step 4 — Project Folder & Files**

Create the project structure:

`notes-app/ ├── app/ │   ├── app.py │   ├── requirements.txt │   └── templates/index.html ├── db/init.sql ├── nginx/default.conf ├── Dockerfile ├── docker-compose.yml └── README.md`

**Screenshot placeholder:** <img width="702" height="70" alt="image" src="https://github.com/user-attachments/assets/90cd1b0c-f2a2-4546-91af-13464050f1db" />


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
    
-   Screenshot: <img width="1440" height="373" alt="image" src="https://github.com/user-attachments/assets/b4533387-92c1-4fe2-bb47-b0cd9c9a9d4d" />

    

* * *

## **Step 6 — MySQL Database**

**db/init.sql**

`CREATE DATABASE IF NOT EXISTS notesdb; USE notesdb; CREATE TABLE IF NOT EXISTS notes (   id INT AUTO_INCREMENT PRIMARY KEY,   content TEXT,   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );`

-   Docker volume `mysql_data` ensures **persistent storage**
    
-   Environment variables set root password and database name
    

**Screenshot placeholder:** 
<img width="631" height="308" alt="image" src="https://github.com/user-attachments/assets/9a035743-16d2-4f1b-9790-c0f4bfd6f8dc" />


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
        



* * *

## **Step 9 — Deploy Application**

1.  Start services:
    

`cd ~/notes-app sudo docker-compose up -d --build`


**Screenshot placeholder:** 
<img width="1156" height="696" alt="image" src="https://github.com/user-attachments/assets/29e378f6-d3e5-49d0-91b2-73b5b548a98f" />

<img width="1119" height="464" alt="image" src="https://github.com/user-attachments/assets/4d661fce-5de3-484e-ad2e-7a6628e4f9e2" />

2.  Verify containers:
    

`sudo docker ps`

3.  Access app using **ALB DNS**:
    

`http://jatin-notes-alb-437994785.us-west-2.elb.amazonaws.com`

4.  Save notes → verify database:
    

`sudo docker exec -it mysql_db mysql -uroot -prootpassword -e "USE notesdb; SELECT * FROM notes;"`

**Screenshot placeholder:** 
<img width="1440" height="557" alt="image" src="https://github.com/user-attachments/assets/a38d9225-78c8-4185-b232-5d7c7fd829f6" />

<img width="646" height="463" alt="image" src="https://github.com/user-attachments/assets/0019946c-f9da-4706-93e0-3d48aafa0626" />


* * *

## **Step 10 — Reset / Start Fresh**

-   Clear all notes:
    

`sudo docker exec -it mysql_db mysql -uroot -prootpassword -e "USE notesdb; TRUNCATE TABLE notes;"`


