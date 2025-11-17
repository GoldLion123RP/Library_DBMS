# 📚 Library Management System

> A full-stack cloud-deployed Library Management System built as a DBMS Lab Project for Brainware University

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://goldlion123rp.github.io/Library_DBMS/)
[![Backend API](https://img.shields.io/badge/API-live-blue)](https://library-dbms-1tp2.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Mobile Responsive](https://img.shields.io/badge/mobile-responsive-success)](https://goldlion123rp.github.io/Library_DBMS/)

---

## 🌐 Live Demo

**🔗 Application:** <a href="https://goldlion123rp.github.io/Library_DBMS/" target="_blank">https://goldlion123rp.github.io/Library_DBMS/</a>

**🔗 Backend API:** <a href="https://library-dbms-1tp2.onrender.com" target="_blank">https://library-dbms-1tp2.onrender.com</a>

**🔗 Source Code:** <a href="https://github.com/goldlion123rp/Library_DBMS" target="_blank">https://github.com/goldlion123rp/Library_DBMS</a>

> **Note:** First load may take 30-60 seconds as the free backend server wakes up. Subsequent requests are fast.

---

## 🔐 Demo Credentials

### Admin Account (Full Access)
- **Username:** `rahul.pal`
- **Password:** `rahul123`
- **Permissions:** Complete system access, staff management, all CRUD operations

### Librarian Account
- **Username:** `ajay.das`
- **Password:** `ajay123`
- **Permissions:** Book & member management, loan operations, reports

### Assistant Account
- **Username:** `santunu.mog`
- **Password:** `santunu123`
- **Permissions:** View access, basic loan operations

---

## ✨ Features

### 📖 Core Functionality
- ✅ **User Authentication** - Secure login with role-based access control (RBAC)
- ✅ **Book Management** - Complete CRUD operations with search and filtering
- ✅ **Member Management** - Track members, memberships, and borrowing history
- ✅ **Loan Tracking** - Issue and return books with automatic due date calculation (14-day period)
- ✅ **Fine Management** - Automatic fine calculation (₹5/day for overdue books)
- ✅ **Reports & Analytics** - Real-time statistics and performance insights
- ✅ **Staff Management** - Admin-only staff and role management

### 🎨 User Experience
- ✅ **Fully Responsive Design** - Seamless experience on desktop, tablet, and mobile
- ✅ **Mobile Hamburger Menu** - Touch-friendly navigation with slide-in sidebar
- ✅ **Real-time Search** - Instant search and filtering across all modules
- ✅ **Clean Modern UI** - Intuitive interface with color-coded elements
- ✅ **Interactive Dashboard** - Real-time statistics and quick insights
- ✅ **Smooth Animations** - Polished user interactions and transitions

### 🔒 Security & Access Control
- ✅ **Role-Based Access Control (RBAC)**
  - **Admin:** Full system access + staff management
  - **Librarian:** Book/member management + loan operations
  - **Assistant:** View access + basic operations
- ✅ **Token-based Authentication** - Secure session management
- ✅ **Secure API Endpoints** - Protected routes with authorization
- ✅ **Input Validation** - Client and server-side validation
- ✅ **CORS Protection** - Configured cross-origin policies
- ✅ **Login Audit Logging** - Tracks all login attempts with IP, user agent, and status

### 📱 Mobile Features
- ✅ **Hamburger Menu** - Animated slide-in navigation
- ✅ **Touch Optimized** - Large touch targets and swipe gestures
- ✅ **Responsive Tables** - Horizontal scroll for data tables
- ✅ **Adaptive Layouts** - Optimized for all screen sizes
- ✅ **No Content Overlap** - Perfect mobile viewing experience

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup and accessibility
- **CSS3** - Custom styling with CSS variables and media queries
- **Vanilla JavaScript (ES6+)** - Modern JavaScript features
- **Responsive Design** - Mobile-first approach with breakpoints
- **Hosted on:** GitHub Pages (Free CDN hosting)

### Backend
- **Python 3.9+** - Core programming language
- **Flask 3.0.0** - Lightweight web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **PyMySQL 1.1.0** - MySQL database connector
- **Gunicorn 21.2.0** - Production WSGI server
- **Hosted on:** Render.com (Free tier with auto-deploy)

### Database
- **MySQL 8.4** - Relational database management system
- **11 Normalized Tables** - 3NF schema design
- **Indexed Queries** - Optimized performance
- **Foreign Keys** - Referential integrity
- **Hosted on:** Clever Cloud (Free tier - 256MB storage)

---

## 📊 Database Schema

### Tables (12 total)
1. **Roles** - User role definitions (Admin, Librarian, Assistant)
2. **Users** - System users with role assignments
3. **Staff** - Library staff information and credentials
4. **AuthenticationSystem** - Login authentication data
5. **Author** - Book authors with biography
6. **BookDetails** - Book metadata (ISBN, title, author, category, price)
7. **Books** - Physical inventory (location, quantity)
8. **Members** - Library members and membership details
9. **Loans** - Borrowing transactions and status tracking
10. **Fines** - Overdue fine calculations and payment status
11. **BorrowHistory** - Historical data for analytics
12. **LoginAuditLog** - Security logging for login attempts

### Relationships & Integrity
- Foreign key constraints for referential integrity
- Indexed columns (book_id, member_id, isbn, membership_no)
- Normalized to Third Normal Form (3NF)
- CASCADE and RESTRICT rules for data consistency

---

## 🚀 Deployment Architecture

```

┌─────────────────────────────────────────────────────────┐
│                   USER DEVICES                          │
│         (Desktop | Tablet | Mobile)                     │
└────────────────────┬────────────────────────────────────┘
│ HTTPS
▼
┌────────────────────────────┐
│   GitHub Pages             │
│   (Static Frontend)        │
│   ✓ HTML/CSS/JavaScript    │
│   ✓ CDN Delivery           │
│   ✓ SSL Certificate        │
└────────────┬───────────────┘
│ REST API (HTTPS)
▼
┌────────────────────────────┐
│   Render.com               │
│   (Backend API)            │
│   ✓ Flask Application      │
│   ✓ Gunicorn Server        │
│   ✓ Auto Deploy from Git   │
└────────────┬───────────────┘
│ MySQL Connection
▼
┌────────────────────────────┐
│   Clever Cloud             │
│   (MySQL Database)         │
│   ✓ Managed MySQL 8.4      │
│   ✓ Automatic Backups      │
│   ✓ 256MB Free Tier        │
└────────────────────────────┘

````

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- MySQL 8.0 or higher
- Git
- Modern web browser

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone [https://github.com/goldlion123rp/Library_DBMS.git](https://github.com/goldlion123rp/Library_DBMS.git)
cd Library_DBMS
````

#### 2\. Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3\. Database Setup

```bash
# Using MySQL Command Line
mysql -u root -p

# Create database
CREATE DATABASE LibraryDB;
exit;

# Import schema
mysql -u root -p LibraryDB < ../database/schema.sql

# Or use phpMyAdmin:
# 1. Open http://localhost/phpmyadmin
# 2. Create database "LibraryDB"
# 3. Import database/schema.sql
```

#### 4\. Configure Environment Variables

**Create** `backend/.env` file:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=LibraryDB
DB_PORT=3306
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ORIGINS=*
```

#### 5\. Run Backend Server

```bash
# Make sure venv is activated
python app.py
```

Backend will run on `http://localhost:5000`

**Test backend:**

```bash
# Visit in browser
http://localhost:5000
# Should show JSON response
```

#### 6\. Run Frontend

```bash
# Open new terminal
# Navigate to project root
cd Library_DBMS

# Start HTTP server
python -m http.server 8000
```

Frontend will run on `http://localhost:8000`

#### 7\. Access Application

  - **Frontend:** http://localhost:8000
  - **Backend API:** http://localhost:5000
  - **Login:** Use demo credentials above

-----

## 🌍 Production Deployment

For complete deployment guide, see [DEPLOYMENT.md](https://www.google.com/search?q=DEPLOYMENT.md)

### Quick Deployment Summary

#### Database (Clever Cloud)

1.  Create free MySQL add-on at https://clever-cloud.com
2.  Get database credentials
3.  Import `database/schema_cloud.sql` via phpMyAdmin
4.  Note connection details for backend

#### Backend (Render.com)

1.  Sign up at https://render.com
2.  Connect GitHub repository
3.  Create Web Service:
      - **Root Directory:** `backend`
      - **Build Command:** `pip install -r requirements.txt`
      - **Start Command:** `gunicorn app:app`
4.  Add environment variables (DB credentials)
5.  Deploy and get backend URL

#### Frontend (GitHub Pages)

1.  Push code to GitHub
2.  Go to repository Settings → Pages
3.  Source: `main` branch, `/ (root)` folder
4.  Update `js/config.js` with backend URL
5.  Site will be live at `https://username.github.io/repo-name/`

-----

## 📈 Features Overview

### Dashboard

  - **Statistics Cards:** Total books, members, active loans, overdue books
  - **Books by Category:** Visual breakdown with progress bars
  - **Recent Loan Activity:** Real-time transaction feed
  - **Financial Summary:** Unpaid fines and counts
  - **Quick Actions:** Navigate to key modules

### Books Module

  - **Add Books:** ISBN, title, author, category, location, quantity, price
  - **Edit Books:** Update all book details and inventory
  - **Delete Books:** With validation (prevent deletion of loaned books)
  - **Search & Filter:** By title, author, ISBN, or category
  - **Category Management:** Automatic category detection
  - **Availability Status:** Real-time quantity tracking

### Members Module

  - **Register Members:** Membership number, name, contact, join date
  - **Edit Members:** Update member information
  - **View History:** Complete borrowing history per member
  - **Status Tracking:** Active/Inactive membership status
  - **Search Members:** By name, email, or membership number

### Loans Module

  - **Issue Books:** Select book and member, auto-calculate due date
  - **Return Books:** Mark as returned, automatic fine calculation
  - **Track Status:** Issued, Returned, Overdue with visual indicators
  - **Due Date Alerts:** Highlight overdue items
  - **Filter Options:** By status (issued/returned/overdue)
  - **Validation:** Prevent issuing to members with overdue books

### Fines Module

  - **Auto-calculation:** ₹5 per day for late returns
  - **View All Fines:** Paid and unpaid with details
  - **Mark as Paid:** Update payment status
  - **Total Summary:** Unpaid fines amount and count
  - **Filter by Status:** Paid/Unpaid filtering

### Reports & Analytics

  - **Top 10 Most Borrowed Books:** Ranked by popularity
  - **Top 10 Most Active Members:** Based on borrowing frequency
  - **Late Return Trends:** Average late days per member
  - **Monthly Statistics:** Issues vs returns over time
  - **Visual Insights:** Charts and trend analysis

### Staff Management (Admin Only)

  - **Add Staff:** Create new staff accounts with roles
  - **Edit Staff:** Update details and change roles
  - **Delete Staff:** With validation (prevent deletion of active issuers)
  - **Role Assignment:** Admin, Librarian, Assistant
  - **Credential Management:** Username and password setup

### Security & Auditing
- **Login Audit Logs:** New admin-only page to monitor all successful and failed login attempts.
- **Detailed Logging:** Captures username, timestamp, IP address, user agent, and failure reason.
- **Security Dashboard:** Displays stats like today's logins and failed attempts.
- **Role Protection:** The new page is strictly for Admin users.

-----

## 🧪 Testing

### Manual Testing Checklist

  - ✅ User login (all three roles)
  - ✅ Dashboard statistics display
  - ✅ Book CRUD operations
  - ✅ Member CRUD operations
  - ✅ Issue and return books
  - ✅ Fine calculation accuracy
  - ✅ Search and filter functionality
  - ✅ Reports data accuracy
  - ✅ Staff management (Admin)
  - ✅ Responsive design on mobile
  - ✅ Hamburger menu functionality

### API Testing

**Test endpoints using browser or Postman:**

```bash
# Health check
GET /

# Authentication
POST /api/auth/login
GET  /api/auth/verify

# Books
GET    /api/books
GET    /api/books/{id}
POST   /api/books
PUT    /api/books/{id}
DELETE /api/books/{id}

# Members
GET    /api/members
POST   /api/members
PUT    /api/members/{id}
DELETE /api/members/{id}

# Loans
GET  /api/loans
POST /api/loans/issue
PUT  /api/loans/{id}/return

# Fines
GET /api/fines
PUT /api/fines/{id}/pay
GET /api/fines/total

# Reports
GET /api/reports/dashboard
GET /api/reports/most-borrowed
GET /api/reports/active-members
GET /api/reports/monthly-stats

# Staff (Admin only)
GET    /api/staff
POST   /api/staff
PUT    /api/staff/{id}
DELETE /api/staff/{id}
```

-----

## 📚 API Documentation

### Base URLs

  - **Production:** `https://library-dbms-1tp2.onrender.com/api`
  - **Local:** `http://localhost:5000/api`

### Authentication

All protected endpoints require authentication header:

```
Authorization: Bearer {token}
```
#### Login Audit (Admin Only)
- `GET /api/auth/login-logs` - Get all login logs
- `GET /api/auth/login-stats` - Get login statistics

### Response Format

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Format

```json
{
  "success": false,
  "error": "Error message description"
}
```

-----

## 👥 Team

**Project Lead & Developer:**

  - **Rahul Pal** - [@goldlion123rp](https://github.com/goldlion123rp)

**Team Contributors:**

  - Subhadip Jana
  - Ajay Kumar Das
  - Pritam Maity
  - Santunu Mog

**Institution:** Brainware University  
**Department:** Computer Science & Engineering  
**Course:** DBMS Lab (PCC-CSG591)  
**Semester:** 5  
**Academic Year:** 2024-2025

-----

## 📝 Project Structure

```
Library_DBMS/
├── backend/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── books.py          # Book management
│   │   ├── members.py        # Member management
│   │   ├── loans.py          # Loan operations
│   │   ├── fines.py          # Fine management
│   │   ├── reports.py        # Analytics & reports
│   │   └── staff.py          # Staff management
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py        # Helper functions
│   ├── app.py                # Main Flask application
│   ├── config.py             # Configuration settings
│   ├── database.py           # Database connections
│   └── requirements.txt      # Python dependencies
├── database/
│   ├── schema.sql            # Local database schema
│   └── schema_cloud.sql      # Cloud deployment schema
├── css/
│   └── style.css             # Complete styling with responsive design
├── js/
│   ├── config.js             # API configuration
│   ├── auth.js               # Authentication logic
│   ├── mobile.js             # Mobile hamburger menu ⭐ NEW
│   ├── dashboard.js          # Dashboard functionality
│   ├── books.js              # Book operations
│   ├── members.js            # Member operations
│   ├── loans.js              # Loan operations
│   ├── fines.js              # Fine operations
│   ├── reports.js            # Reports & analytics
│   └── staff.js              # Staff management
├── index.html                # Login page
├── dashboard.html            # Dashboard
├── books.html                # Books module
├── members.html              # Members module
├── loans.html                # Loans module
├── login-logs.html           # Login audit log page ⭐ NEW
├── fines.html                # Fines module
├── reports.html              # Reports module
├── staff.html                # Staff module
├── favicon.svg               # Favicon
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── DEPLOYMENT.md             # Deployment guide
└── LICENSE                   # MIT License
```

-----

## ⚠️ Known Issues & Limitations

### Free Tier Limitations

**Backend (Render.com):**

  - ⏱️ Spins down after 15 minutes of inactivity
  - ⏱️ First request takes 30-60 seconds to wake up
  - ⏱️ Subsequent requests are fast (normal speed)
  - 💡 **Solution:** Use [UptimeRobot](https://uptimerobot.com/) to ping every 5 minutes

**Database (Clever Cloud):**

  - 💾 256MB storage limit (\~10,000+ records)
  - 💾 Sufficient for small to medium libraries

**GitHub Pages:**

  - 📄 Static files only (no backend processing)
  - 📄 100GB bandwidth/month

### Browser Compatibility

  - ✅ Chrome 90+
  - ✅ Firefox 88+
  - ✅ Safari 14+
  - ✅ Edge 90+
  - ❌ IE11 not supported

### Mobile Experience
- ✅ Fully responsive on all devices
- ✅ Touch-optimized controls
- ✅ Hamburger navigation menu
- ⚠️ Tables scroll horizontally on small screens due to large data content.

-----

## 🔮 Future Enhancements

### Planned Features

  - [ ] Email notifications for due dates and overdue books
  - [ ] QR code generation for books and membership cards
  - [ ] Book reservation system
  - [ ] Advanced analytics with interactive charts (Chart.js)
  - [ ] Export reports to PDF/Excel
  - [ ] Barcode scanner integration
  - [ ] Multi-language support (i18n)
  - [ ] Dark mode theme toggle
  - [ ] Progressive Web App (PWA) support
  - [ ] Real-time notifications with WebSocket

### Technical Improvements

  - [ ] Implement JWT refresh tokens
  - [ ] Add unit tests (pytest)
  - [ ] API rate limiting
  - [ ] Database query optimization
  - [ ] Implement caching (Redis)
  - [ ] Add API versioning
  - [ ] Implement logging system
  - [ ] Add data backup automation

### Mobile App

  - [ ] React Native mobile application
  - [ ] Offline mode support
  - [ ] Push notifications
  - [ ] Biometric authentication

### AI/ML Features

  - [ ] Book recommendation system
  - [ ] Demand prediction
  - [ ] Automatic categorization
  - [ ] Chatbot support

-----

## 🤝 Contributing

This is an academic project, but suggestions and feedback are welcome\!

### How to Contribute

1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

### Code Style

  - Follow PEP 8 for Python code
  - Use meaningful variable names
  - Comment complex logic
  - Write descriptive commit messages

-----

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

### Third-Party Licenses

  - Flask (BSD License)
  - Flask-CORS (MIT License)
  - PyMySQL (MIT License)
  - Gunicorn (MIT License)

-----

## 🙏 Acknowledgments

  - **Brainware University** - For the opportunity and academic support
  - **Department of Computer Science & Engineering** - For project guidance
  - **Render.com** - Free backend hosting platform
  - **GitHub Pages** - Free frontend hosting and CDN
  - **Clever Cloud** - Free MySQL database hosting
  - **Stack Overflow Community** - For troubleshooting assistance
  - **MDN Web Docs** - For web development references

-----

## 📞 Contact & Support

**Developer:** Rahul Pal  
**Email:** goldlion123.rp@gmail.com  
**GitHub:** [@goldlion123rp](https://github.com/goldlion123rp)  
**Project Link:** [https://github.com/goldlion123rp/Library\_DBMS](https://github.com/goldlion123rp/Library_DBMS)

### Issues & Bug Reports

Found a bug? [Open an issue](https://github.com/goldlion123rp/Library_DBMS/issues)

### Questions?

Have questions? Check [Discussions](https://github.com/goldlion123rp/Library_DBMS/discussions)

-----

## 🌟 Show Your Support

If you found this project helpful:

  - ⭐ **Star** this repository
  - 🍴 **Fork** for your own use
  - 📢 **Share** with others
  - 💬 **Provide feedback** via issues
  - 🤝 **Contribute** improvements

-----

## 📊 Project Stats

-----

## 🏆 Achievements

  - ✅ Full-stack cloud deployment
  - ✅ RESTful API architecture
  - ✅ Normalized database design (3NF)
  - ✅ Role-based access control
  - ✅ Responsive mobile-first design
  - ✅ Production-ready application
  - ✅ Complete documentation
  - ✅ Open-source contribution

-----
<div align="center">
  
  <h3><strong>Made with ❤️ by Rahul Pal & Team</strong></h3>

  <p><strong>Brainware University | Department of CSE | 2024-2025</strong></p>

  <p>
    <a href="https://goldlion123rp.github.io/Library_DBMS/">🌐 Live Demo</a> • 
    <a href="https://github.com/goldlion123rp/Library_DBMS">📖 Documentation</a> • 
    <a href="https://github.com/goldlion123rp/Library_DBMS/issues">🐛 Report Bug</a> • 
    <a href="https://github.com/goldlion123rp/Library_DBMS/issues">✨ Request Feature</a>
  </p>

  <hr>

  <p><strong>⭐ If this project helped you, please give it a star! ⭐</strong></p>

</div>