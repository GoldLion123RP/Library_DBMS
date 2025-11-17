# 📚 Library Management System

> A full-stack cloud-deployed Library Management System built as a DBMS Lab Project for Brainware University

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://goldlion123rp.github.io/Library_DBMS/)
[![Backend API](https://img.shields.io/badge/API-live-blue)](https://library-dbms-1tp2.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌐 Live Demo

**🔗 Application:** [https://goldlion123rp.github.io/Library_DBMS/](https://goldlion123rp.github.io/Library_DBMS/)

**🔗 Backend API:** [https://library-dbms-1tp2.onrender.com](https://library-dbms-1tp2.onrender.com)

**🔗 Source Code:** [https://github.com/goldlion123rp/Library_DBMS](https://github.com/goldlion123rp/Library_DBMS)

---

## 🔐 Demo Credentials

### Admin Account (Full Access)
- **Username:** `rahul.pal`
- **Password:** `rahul123`

### Librarian Account
- **Username:** `ajay.das`
- **Password:** `ajay123`

### Assistant Account
- **Username:** `santunu.mog`
- **Password:** `santunu123`

---

## ✨ Features

### 📖 Core Functionality
- ✅ **User Authentication** - Secure login with role-based access control
- ✅ **Book Management** - Add, edit, delete, and search books
- ✅ **Member Management** - Manage library members and memberships
- ✅ **Loan Tracking** - Issue and return books with due date tracking
- ✅ **Fine Management** - Automatic fine calculation for overdue books
- ✅ **Reports & Analytics** - Comprehensive insights and statistics

### 🎨 User Experience
- ✅ **Responsive Design** - Mobile-friendly interface
- ✅ **Real-time Search** - Instant search and filtering
- ✅ **Clean UI** - Modern, intuitive interface with color-coded elements
- ✅ **Dashboard** - Overview of library statistics at a glance

### 🔒 Security & Access Control
- ✅ **Role-Based Access Control (RBAC)**
  - **Admin:** Full access including staff management
  - **Librarian:** Book and member management, loan operations
  - **Assistant:** View and basic operations
- ✅ **Token-based Authentication**
- ✅ **Secure API endpoints**

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with CSS variables
- **Vanilla JavaScript** - ES6+ features
- **Hosted on:** GitHub Pages

### Backend
- **Python 3.9+** - Core language
- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **PyMySQL 1.1.0** - MySQL database driver
- **Gunicorn 21.2.0** - WSGI HTTP server
- **Hosted on:** Render.com (Free tier)

### Database
- **MySQL 8.4** - Relational database
- **11 Normalized Tables** - Optimized schema design
- **Hosted on:** Clever Cloud (Free tier - 256MB)

---

## 📊 Database Schema

### Tables (11 total)
1. **Roles** - User role definitions
2. **Users** - System users
3. **Staff** - Library staff information
4. **AuthenticationSystem** - Login credentials
5. **Author** - Book authors
6. **BookDetails** - Book metadata
7. **Books** - Physical book inventory
8. **Members** - Library members
9. **Loans** - Borrowing transactions
10. **Fines** - Overdue fines
11. **BorrowHistory** - Analytics data

### Relationships
- Foreign key constraints for data integrity
- Indexed columns for optimized queries
- Normalized to 3NF (Third Normal Form)

---

## 🚀 Deployment Architecture
