# 🎓 Conference Management Tool (CMT) - Centralized University Portal

[![Flask](https://img.shields.io/badge/Backend-Flask_v3.0-blue.svg)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38BDF8.svg)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modern, production-grade **Conference Management System (CMT)** developed for **Lok Jagruti Kendra University (LJKU)**, **CODEAPEX Technical Event**, and **IEEE Student Branch, LJ University**.

This application handles the entire lifecycle of academic conferences—from CFP publication, paper/poster submission, and payment gateway simulation, to administrative verification, live event timetables, and past proceedings archiving.

---

## 🌟 Key Features

### 👤 Dual Role Authentication & Authorization
- **Author (User) Portal**:
  - User registration (`/signup`) and secure authentication (`/login`).
  - Personal Author Dashboard (`/my-submissions`) tracking submitted papers, abstract IDs, verification statuses, and payment states.
- **Administrator Portal (`@admin_required`)**:
  - Full site management dashboard (`/admin`).
  - **Admin Security**: Dedicated settings page (`/admin/settings`) to update Admin ID (email), display name, and password with current password verification.
  - Delete invalid submissions with confirmation safety.

### 🏛️ Lifecycle State Management & Dynamic Filters
- **Manage Conference States**: Toggle lifecycle states between **Current (Home)**, **Upcoming (Open)**, and **Past (Archived)**.
- **Zero-Reload Instant Filtering**:
  - Filter author submissions by **Search Query** (Abstract ID, Author, Title, Email), **Department** (CSE, ECE, Mech, Civil, IT, AI-DS), **Verification Status** (Under Review, Verified, Accepted, Rejected), and **Presentation Type** (Paper vs Poster).
  - Filtering occurs **instantly in-place on the DOM** with zero page reloads and real-time badge count updates.

### 📅 Native Date Pickers & Automated Formatting
- Native `<input type="date">` selection dropdown pickers for Start Date, End Date, and Submission Deadline in the conference creation modal to eliminate date entry typos.
- Automatic backend string formatting converting ISO dates (e.g. `2026-10-15`) into human-readable academic dates (`October 15, 2026`).

### 📱 Responsive Design across Mobile, Tablet, and Widescreen
- Integrated **Tailwind CSS** and custom CSS media queries for fluid layouts.
- Collapsible hamburger navigation menu (`#mobileMenuBtn`) on mobile screens.
- Horizontal scroll wrappers (`overflow-x-auto`) for data tables to prevent horizontal overflow on narrow screens.

### 💳 Integrated Payment Gateway Simulation
- Authors can pay registration fees via **UPI / QR Code**, **Debit/Credit Card**, or **Net Banking**.
- Auto-generates official printable registration receipts with transaction reference IDs.

---

## 🔑 Demo Credentials

| Role | Email (User/Admin ID) | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@ljku.edu.in` | `admin123` | Full Site Control & Admin Settings |
| **Author (User)** | `aarav.sharma@example.edu` | `user123` | Submit Papers & Track Submissions |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/smit-ghori/Conference-Management-Tool.git
cd Conference-Management-Tool
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Seeding
Initialize the SQLite database with default admin accounts, sample conferences, schedules, updates, and author submissions:
```bash
python seed.py
```

### 5. Run the Application
Launch the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
**`http://127.0.0.1:5000`**

---

## 🧪 Running Automated Tests

The repository includes a comprehensive unit test suite (`test_app.py`) covering authentication, date parsing, admin setting updates, abstract ID generation, and role security:

```bash
python -m unittest test_app.py
```

---

## 📂 Project Structure

```text
Conference-Management-Tool/
├── app.py                      # Core Flask Application & API Routes
├── seed.py                     # Database Initialization & Seeding Script
├── test_app.py                 # Automated Unit Test Suite
├── requirements.txt            # Python Dependencies
├── database.db                 # SQLite Database Store
├── static/
│   ├── css/
│   │   └── style.css           # Global Design Tokens & Custom CSS
│   ├── js/
│   │   └── main.js             # Mobile Menu & Zero-Reload Auto-Filtering JS
│   └── uploads/                # Conference Brochures & Flyers Storage
└── templates/
    ├── base.html               # Master Layout with Navigation & Tailwind CDN
    ├── home.html               # Current Conferences & Live Schedule
    ├── upcoming.html           # Upcoming Events & Call for Papers
    ├── archive.html            # Past Proceedings & Outcome Reports
    ├── conference_detail.html  # Track Overview & Keynote Speakers
    ├── submit.html             # Author Paper & Poster Registration Form
    ├── lookup.html             # Abstract ID Tracker
    ├── payment.html            # Simulated Multi-Method Payment Gateway
    ├── receipt.html            # Printable Registration Receipt
    ├── login.html              # Login Page with Demo Credentials
    ├── signup.html             # Author Account Registration
    ├── my_submissions.html     # Protected Author Dashboard
    ├── admin.html              # Admin Lifecycle Management Dashboard
    └── admin_settings.html     # Admin ID & Password Security Panel
```

---

## 🤝 Institutional Credits

- **Lok Jagruti Kendra University (LJKU)**
- **CODEAPEX Technical Event Committee**
- **IEEE Student Branch, LJ University**

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
