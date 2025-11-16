# 🚀 Library Management System - Deployment Guide

Complete step-by-step guide to deploy your Library Management System for **FREE**.

---

## 📋 Table of Contents

1. [Database Setup (Clever Cloud)](#1-database-setup-clever-cloud)
2. [Backend Deployment (Render)](#2-backend-deployment-render)
3. [Frontend Deployment (GitHub Pages)](#3-frontend-deployment-github-pages)
4. [Testing & Verification](#4-testing--verification)

---

## 1️⃣ Database Setup (Clever Cloud)

### **Step 1: Create Clever Cloud Account**

1. Go to: https://www.clever-cloud.com/
2. Click **"Sign Up"** → Sign up with **GitHub**
3. Verify your email

### **Step 2: Create MySQL Database**

1. Click **"Create"** → **"an add-on"**
2. Select **"MySQL"**
3. Choose **"DEV"** plan (FREE)
4. Name: `library-db`
5. Click **"Create"**

### **Step 3: Get Database Credentials**

1. Go to your MySQL add-on
2. Click **"Connection settings"** or **"Environment variables"**
3. Copy these details:
   - **Host**: `xxxxxx.mysql.clever-cloud.com`
   - **Port**: `3306`
   - **Database**: `xxxxxxxxx`
   - **User**: `uxxxxxxxxx`
   - **Password**: `xxxxxxxxxxxx`

### **Step 4: Import Database Schema**

**Option A: Using MySQL Workbench**

1. Download MySQL Workbench: https://dev.mysql.com/downloads/workbench/
2. Create new connection with Clever Cloud credentials
3. Open `database/schema.sql`
4. Execute the script

**Option B: Using phpMyAdmin (if available)**

1. Access Clever Cloud phpMyAdmin interface
2. Select your database
3. Go to **Import** tab
4. Upload `database/schema.sql`
5. Click **Go**

**Option C: Using Command Line**

```bash
mysql -h YOUR_HOST -u YOUR_USER -p YOUR_DATABASE < database/schema.sql