-- ==========================================================
-- Library Management System - Complete Schema
-- Admin: Rahul Pal
-- Brainware University | DBMS Lab Project
-- ==========================================================

DROP DATABASE IF EXISTS LibraryDB;
CREATE DATABASE LibraryDB;
USE LibraryDB;

-- ==========================================================
-- TABLE CREATION
-- ==========================================================

-- Roles Table
CREATE TABLE Roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

-- Users Table
CREATE TABLE Users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  FirstName VARCHAR(100) NOT NULL,
  LastName VARCHAR(100) NOT NULL,
  email VARCHAR(150),
  password VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  full_name VARCHAR(150),
  role_id INT,
  FOREIGN KEY (role_id) REFERENCES Roles(id)
);

-- Authors Table
CREATE TABLE Author (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Biography TEXT,
    YearOfPublication YEAR
);

-- Staff Table
CREATE TABLE Staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Username VARCHAR(50) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Role VARCHAR(50)
);

-- Authentication System
CREATE TABLE AuthenticationSystem (
    LoginID INT PRIMARY KEY AUTO_INCREMENT,
    StaffID INT UNIQUE,
    Password VARCHAR(255) NOT NULL,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);

-- BookDetails Table
CREATE TABLE BookDetails (
  book_detail_id INT AUTO_INCREMENT PRIMARY KEY,
  isbn VARCHAR(20) UNIQUE NOT NULL,
  title VARCHAR(200) NOT NULL,
  author VARCHAR(150),
  category VARCHAR(100),
  price DECIMAL(8,2) CHECK (price >= 0)
);

-- Books Table (Inventory)
CREATE TABLE Books (
  id INT AUTO_INCREMENT PRIMARY KEY,
  book_detail_id INT NOT NULL,
  location VARCHAR(100),
  quantity INT DEFAULT 1 CHECK (quantity >= 0),
  FOREIGN KEY (book_detail_id) REFERENCES BookDetails(book_detail_id)
);

-- Members Table
CREATE TABLE Members (
  id INT AUTO_INCREMENT PRIMARY KEY,
  membership_no VARCHAR(20) UNIQUE,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(150),
  phone VARCHAR(20),
  join_date DATE,
  active BOOLEAN DEFAULT TRUE
);

-- Loans Table
CREATE TABLE Loans (
  id INT AUTO_INCREMENT PRIMARY KEY,
  book_id INT,
  member_id INT,
  issued_by INT,
  issue_date DATE,
  due_date DATE,
  return_date DATE,
  status ENUM('issued','returned','overdue') DEFAULT 'issued',
  FOREIGN KEY (book_id) REFERENCES Books(id),
  FOREIGN KEY (member_id) REFERENCES Members(id),
  FOREIGN KEY (issued_by) REFERENCES Users(id)
);

-- Fines Table
CREATE TABLE Fines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  loan_id INT UNIQUE,
  fine_amount DECIMAL(8,2) DEFAULT 0,
  paid ENUM('paid','unpaid') DEFAULT 'unpaid',
  FOREIGN KEY (loan_id) REFERENCES Loans(id)
);

-- ==========================================================
-- DATA INSERTION
-- ==========================================================

-- Insert Roles
INSERT INTO Roles (name) VALUES 
('Admin'), 
('Librarian'), 
('Assistant'), 
('Intern');

-- Insert Users (Rahul Pal is Admin)
INSERT INTO Users (FirstName, LastName, email, password, phone, full_name, role_id) VALUES
('Rahul','Pal','rahulpal1@gmail.com', 'rahul123','+9198356545678', 'Rahul Pal', 1),
('Subhadip','Jana','subhadipjana7@gmail.com', 'subha123','+919812347678', 'Subhadip Jana', 2),
('Ajay','Das','ajaydas9@gmail.com', 'ajay123','+919912345678', 'Ajay Kumar Das', 2),
('Pritam','Maity','pritammaity5@gmail.com', 'pritam123','+919815345678', 'Pritam Maity', 3),
('Santunu','Mog','santunumog3@gmail.com', 'santunu123','+919812367678', 'Santunu Mog', 3);

-- Insert Authors
INSERT INTO Author (FirstName, LastName, Biography, YearOfPublication) VALUES
('R.K.', 'Narayan', 'Indian author known for creating the fictional town of Malgudi and works like Swami and Friends.', 2007),
('Chetan', 'Bhagat', 'Indian author and columnist, famous for novels like Five Point Someone and 2 States.', 2002),
('Arundhati', 'Roy', 'Booker Prize-winning author of The God of Small Things.', 1989),
('J.K.', 'Rowling', 'British author best known for the Harry Potter series.', 2005),
('George', 'Orwell', 'English novelist and essayist, author of 1984 and Animal Farm.', 2003),
('Jane', 'Austen', 'English novelist known for Pride and Prejudice and Sense and Sensibility.', 2008),
('Mark', 'Twain', 'American writer and humorist, author of The Adventures of Tom Sawyer and Huckleberry Finn.', 2004),
('Ruskin', 'Bond', 'Indian author of British descent, known for short stories and novels set in the Himalayas.', 1979),
('Paulo', 'Coelho', 'Brazilian author best known for The Alchemist.', 2004),
('Khaled', 'Hosseini', 'Afghan-American author of The Kite Runner and A Thousand Splendid Suns.', 1989);

-- Insert Staff (Rahul Pal is Admin - StaffID 1)
INSERT INTO Staff (FirstName, LastName, Username, PasswordHash, Role) VALUES
('Rahul', 'Pal', 'rahul.pal', '5e69', 'Admin'),
('Subhadip', 'Jana', 'subhadip.jana', '5cf99', 'Librarian'),
('Ajay', 'Das', 'ajay.das', '22e03', 'Librarian'),
('Pritam', 'Maity', 'pritam.maity', '2624d0b', 'Assistant'),
('Santunu', 'Mog', 'santunu.mog', '5ca4', 'Assistant');

-- Insert Authentication (Rahul Pal - StaffID 1)
INSERT INTO AuthenticationSystem (StaffID, Password) VALUES
(1, 'rahul123'),
(2, 'subha123'),
(3, 'ajay123'),
(4, 'pritam123'),
(5, 'santunu123');

-- Insert BookDetails
INSERT INTO BookDetails (isbn, title, author, category, price) VALUES
('9780132149181', 'Database System Concepts', 'Abraham Silberschatz', 'Database Management', 650.00),
('9780131103627', 'Computer Networks', 'Andrew S. Tanenbaum', 'Networking', 720.00),
('9780133594140', 'Operating System Concepts', 'Abraham Silberschatz', 'Operating Systems', 700.00),
('9780321486813', 'Introduction to Algorithms', 'Thomas H. Cormen', 'Algorithms', 950.00),
('9780132269933', 'Let Us C', 'Yashavant Kanetkar', 'Programming in C', 420.00),
('9780131479418', 'Computer Organization and Design', 'David A. Patterson', 'Computer Architecture', 680.00),
('9780134685991', 'Effective Java', 'Joshua Bloch', 'Programming in Java', 580.00),
('9780596009205', 'Head First Design Patterns', 'Eric Freeman', 'Software Design', 520.00),
('9780201633610', 'Design Patterns', 'Erich Gamma', 'Software Engineering', 750.00),
('9780135957059', 'The Pragmatic Programmer', 'David Thomas', 'Software Development', 620.00);

-- Insert Books (Inventory)
INSERT INTO Books (book_detail_id, location, quantity) VALUES
(1, 'Shelf A1', 3),
(2, 'Shelf A2', 4),
(3, 'Shelf B1', 2),
(4, 'Shelf B2', 5),
(5, 'Shelf C1', 4),
(6, 'Shelf C2', 3),
(7, 'Shelf D1', 2),
(8, 'Shelf D2', 3),
(9, 'Shelf E1', 2),
(10, 'Shelf E2', 4);

-- Insert Members
INSERT INTO Members (membership_no, name, email, phone, join_date, active) VALUES
('M001', 'Subhadip Jana', 'subhadip.jana@bwu.ac.in', '+919876543211', '2023-01-10', TRUE),
('M002', 'Ajay Kumar Das', 'ajay.das@bwu.ac.in', '+919812345678', '2023-02-14', TRUE),
('M003', 'Pritam Maity', 'pritam.maity@bwu.ac.in', '+919123456789', '2023-03-20', TRUE),
('M004', 'Santunu Mog', 'santunu.mog@bwu.ac.in', '+919898989898', '2023-04-05', TRUE),
('M005', 'Rahul Pal', 'rahul.pal@bwu.ac.in', '+919777777777', '2023-05-10', TRUE),
('M006', 'Ananya Sharma', 'ananya.sharma@bwu.ac.in', '+919666666666', '2023-06-15', TRUE),
('M007', 'Rohan Gupta', 'rohan.gupta@bwu.ac.in', '+919555555555', '2023-07-20', TRUE),
('M008', 'Priya Singh', 'priya.singh@bwu.ac.in', '+919444444444', '2023-08-25', TRUE);

-- Insert Loans
INSERT INTO Loans (book_id, member_id, issued_by, issue_date, due_date, return_date, status) VALUES
(1, 1, 1, '2024-09-01', '2024-09-15', '2024-09-14', 'returned'),
(2, 2, 2, '2024-10-01', '2024-10-15', NULL, 'issued'),
(3, 3, 3, '2024-10-05', '2024-10-20', NULL, 'issued'),
(4, 4, 1, '2024-10-10', '2024-10-24', NULL, 'issued'),
(5, 5, 2, '2024-09-20', '2024-10-04', '2024-10-06', 'returned'),
(6, 6, 3, '2024-10-12', '2024-10-26', NULL, 'issued'),
(7, 7, 1, '2024-08-15', '2024-08-29', '2024-09-05', 'returned'),
(8, 8, 2, '2024-10-15', '2024-10-29', NULL, 'issued');

-- Insert Fines
INSERT INTO Fines (loan_id, fine_amount, paid) VALUES
(1, 0.00, 'paid'),
(5, 10.00, 'unpaid'),
(7, 35.00, 'paid');

-- ==========================================================
-- CREATE INDEXES
-- ==========================================================

CREATE INDEX idx_bookid ON Loans(book_id);
CREATE INDEX idx_memberid ON Loans(member_id);
CREATE INDEX idx_isbn ON BookDetails(isbn);
CREATE INDEX idx_membership ON Members(membership_no);
CREATE INDEX idx_loan_status ON Loans(status);

-- ==========================================================
-- CREATE BORROW HISTORY TABLE (FOR ANALYTICS)
-- ==========================================================

CREATE TABLE BorrowHistory AS
SELECT 
    l.id AS loan_id, 
    m.id AS member_id, 
    b.id AS book_id,
    l.issue_date, 
    l.due_date, 
    l.return_date, 
    l.status
FROM Loans l
JOIN Members m ON l.member_id = m.id
JOIN Books b ON l.book_id = b.id;

-- ==========================================================
-- VERIFICATION QUERIES
-- ==========================================================

-- Show all tables
SHOW TABLES;

-- Count records in each table
SELECT 'Roles' AS TableName, COUNT(*) AS RecordCount FROM Roles
UNION ALL
SELECT 'Users', COUNT(*) FROM Users
UNION ALL
SELECT 'Staff', COUNT(*) FROM Staff
UNION ALL
SELECT 'Author', COUNT(*) FROM Author
UNION ALL
SELECT 'BookDetails', COUNT(*) FROM BookDetails
UNION ALL
SELECT 'Books', COUNT(*) FROM Books
UNION ALL
SELECT 'Members', COUNT(*) FROM Members
UNION ALL
SELECT 'Loans', COUNT(*) FROM Loans
UNION ALL
SELECT 'Fines', COUNT(*) FROM Fines;

-- Verify Admin User
SELECT 
    s.StaffID,
    s.FirstName,
    s.LastName,
    s.Username,
    s.Role,
    a.Password
FROM Staff s
JOIN AuthenticationSystem a ON s.StaffID = a.StaffID
WHERE s.Role = 'Admin';

-- ==========================================================
-- END OF SCHEMA
-- ==========================================================

-- Success Message
SELECT '✅ Database LibraryDB created successfully!' AS Status;
SELECT '✅ All tables created and populated!' AS Status;
SELECT '✅ Admin User: rahul.pal | Password: rahul123' AS Status;