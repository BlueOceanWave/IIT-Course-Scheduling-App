DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS prerequisites CASCADE;
DROP TABLE IF EXISTS corequisites CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS enrollment CASCADE;
DROP TABLE IF EXISTS term CASCADE;
DROP TABLE IF EXISTS instructors CASCADE;

--Account
CREATE TABLE accounts
(
 username varchar (50) PRIMARY KEY,
 password varchar (50),
 major varchar (50)
);

--Subjects
CREATE TABLE subjects
(sID varchar (10),
 lID varchar (20) PRIMARY KEY
);

--Courses
CREATE TABLE courses
(sID varchar (10),
 cID int,
 title varchar (25), --Primary Key?
 hours int,
 description varchar (200),
 --attributes varchar (30),
 PRIMARY KEY (sID, cID),
 FOREIGN KEY (sID) REFERENCES subjects
);

--Prerequisites
CREATE TABLE prerequisites
(sID varchar (10),
 cID int,
 psID varchar (10),
 pcID int,
 other varchar (20), --Placement tests, etc.
 concurrent bool,
 minGrade varchar (1),
 index int,
 PRIMARY KEY (sID, cID, psID, pcID),
 FOREIGN KEY (sID, cID) REFERENCES courses,
 FOREIGN KEY (psID, pcID) REFERENCES courses
);

--Corequisites
CREATE TABLE corequisites
(sID varchar (10),
 cID int,
 csID varchar (10),
 ccID int,
 other varchar (20), --Placement tests, etc.
 minGrade varchar (1),
 index int,
 PRIMARY KEY (sID, cID, csID, ccID),
 FOREIGN KEY (sID, cID) REFERENCES courses,
 FOREIGN KEY (csID, ccID) REFERENCES courses
);

--Term
CREATE TABLE term
(term varchar (15) PRIMARY KEY,
 startDate date,
 endDate date
);

--Classes
CREATE TABLE classes
(CRN int PRIMARY KEY,
 sID varchar (10),
 cID int,
 sNum varchar (10),
 term varchar (15),
 days varchar (5),
 startTime time,
 endTime time,
 campus varchar (10),
 online varchar (20),
 building varchar (30),
 room varchar (10), --incase its 124-j
 FOREIGN KEY (sID, cID) REFERENCES courses,
 FOREIGN KEY (term) REFERENCES term
);

--Instructors
CREATE TABLE instructors
(CRN int PRIMARY KEY,
 instructor varchar (30)
);

--Enrollment
CREATE TABLE enrollment
(CRN int PRIMARY KEY,
 enrollment int,
 enrollmentMax int,
 waitlist int,
 FOREIGN KEY (CRN) REFERENCES classes
);

