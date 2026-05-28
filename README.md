# GetPlaced - Placement Portal Application

A full-stack Placement Portal Application built using **Flask**, **Vue.js**, **Redis**, and **Celery** that enables students, companies, and administrators to interact through a centralized placement management system.

---

# Project Overview

GetPlaced is a web-based placement management platform designed for institutes to streamline placement activities.

The system supports three major roles:

* **Admin**
* **Company**
* **Student**

The platform enables:

* Company registrations and approvals
* Placement drive management
* Student applications
* Resume uploads
* Application tracking
* Automated reminders and reports
* CSV export functionality

---

# Tech Stack

## Backend

* Flask
* Flask-RESTful
* Flask-Security
* SQLAlchemy ORM
* Celery
* Redis
* Flask-Mail

## Frontend

* Vue.js
* Bootstrap 5

## Database

* MySQL

---

# Features

## Admin Dashboard

* View overall placement statistics
* Approve/reject companies
* Approve/reject placement drives
* Search students, companies, and drives
* Manage users
* Blacklist/deactivate users
* Trigger reminder emails manually
* Trigger monthly reports manually

---

## Company Dashboard

* Company registration
* Create placement drives
* Manage applicants
* Update application status:

  * Shortlisted
  * Selected
  * Rejected

---

## Student Dashboard

* Student registration/login
* Browse approved placement drives
* Apply for drives
* Upload resume (PDF)
* Track application status
* Edit profile
* Export application history

---

# Background Jobs (Celery)

## Daily Reminder Emails

Automatically sends reminder emails to students for drives closing within 3 days.

## Monthly Activity Report

Generates and emails HTML placement reports to admin.

## CSV Export

Exports student application history asynchronously and sends it via email.

---

# Redis Caching

Redis is used for:

* API response caching
* Celery message broker
* Cache invalidation on updates

---

# Authentication & Authorization

Implemented using Flask-Security with:

* JWT Authentication
* Role-Based Access Control

Roles:

* Admin
* Company
* Student

---

# Database Design

The application uses a relational database schema with:

* Users
* Roles
* Students
* Companies
* Placement Drives
* Applications

### Key Design Decisions

* Unified user authentication model
* Many-to-many role mapping
* One-to-one profile mapping
* Unique application constraints
* Status-based filtering for dashboards

---

# API Endpoints

## Admin APIs

| Endpoint                  | Method | Description            |
| ------------------------- | ------ | ---------------------- |
| `/api/admin/dashboard`    | GET    | Dashboard statistics   |
| `/api/admin/students`     | GET    | All students           |
| `/api/admin/companies`    | GET    | All companies          |
| `/api/admin/company/<id>` | PUT    | Approve/reject company |
| `/api/admin/drives`       | GET    | All drives             |
| `/api/admin/drive/<id>`   | PUT    | Approve/reject drive   |
| `/api/admin/applications` | GET    | All applications       |
| `/api/admin/search`       | GET    | Search functionality   |

---

## Student APIs

| Endpoint                    | Method | Description          |
| --------------------------- | ------ | -------------------- |
| `/api/student/profile`      | GET    | Student profile      |
| `/api/student/profile`      | PUT    | Update profile       |
| `/api/student/resume`       | POST   | Upload resume        |
| `/api/student/drives`       | GET    | Approved drives      |
| `/api/student/apply`        | POST   | Apply for drive      |
| `/api/student/applications` | GET    | Student applications |

---

## Company APIs

| Endpoint                        | Method | Description      |
| ------------------------------- | ------ | ---------------- |
| `/api/company/profile`          | GET    | Company profile  |
| `/api/company/drives`           | GET    | Company drives   |
| `/api/company/drive`            | POST   | Create drive     |
| `/api/company/applicants`       | GET    | Drive applicants |
| `/api/company/application/<id>` | PUT    | Update status    |

---

# Project Structure

```bash
GetPlaced/
│
├── backend/
│   ├── resources/
│   ├── services/
│   ├── tasks/
│   ├── models.py
│   ├── app.py
│   └── config.py
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── router/
│   │   └── assets/
│   │
│   └── package.json
│
├── requirements.txt
└── README.md
```

---

# Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/your-username/GetPlaced-Placement-Portal.git
cd GetPlaced-Placement-Portal
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Setup Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
SECURITY_PASSWORD_SALT=your_salt

MAIL_USERNAME=your_email
MAIL_PASSWORD=your_password

DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=get_placed_db
```

---

## 5. Start Redis Server

Make sure Redis server is running.

---

## 6. Run Flask Backend

```bash
python app.py
```

---

## 7. Start Celery Worker

```bash
celery -A app.celery worker --loglevel=info --pool=solo
```

---

## 8. Start Celery Beat

```bash
celery -A app.celery beat --loglevel=info
```

---

## 9. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# Future Improvements

* Real-time notifications
* AI-based resume screening
* Interview scheduling system
* Analytics dashboard
* Cloud deployment

---

# AI Usage Declaration

Approximately **30% AI assistance** was used for:

* Backend job implementation
* Error fixing
* Frontend styling
* UI improvements

---

# Screenshots

Add your project screenshots here.

Example:

```md
![Dashboard](screenshots/dashboard.png)
```

---

# Video Demo

Add your project demo video link here.

Example:

```md
https://youtube.com/your-demo-link
```
