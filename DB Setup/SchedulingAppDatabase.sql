DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS prerequisites CASCADE;
DROP TABLE IF EXISTS corequisites CASCADE;
DROP TABLE IF EXISTS requirements CASCADE;
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
(sID varchar (10) PRIMARY KEY,
 lID varchar (50) 
);

--Courses
CREATE TABLE courses
(sID varchar (10),
 cID int,
 title varchar (150), --Primary Key?
 hours int,
 description varchar (4000),
 --attributes varchar (30),
 PRIMARY KEY (sID, cID),
 FOREIGN KEY (sID) REFERENCES subjects
);

--Requirements
CREATE TABLE requirements
(sID varchar (10),
 cID int,
 rsID varchar (10),
 rcID int,
 concurrent bool,
 minGrade varchar (1),
 index int,
 PRIMARY KEY (sID, cID, rsID, rcID, index),
 FOREIGN KEY (sID, cID) REFERENCES courses,
 FOREIGN KEY (rsID, rcID) REFERENCES courses (sID, cID)
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
 campus varchar (20),
 online varchar (20),
 building varchar (30),
 room varchar (10), --incase its 124-j
 FOREIGN KEY (sID, cID) REFERENCES courses,
 FOREIGN KEY (term) REFERENCES term
);

--Instructors
CREATE TABLE instructors
(CRN int,
 instructor varchar (60),
 PRIMARY KEY (CRN, instructor),
 FOREIGN KEY (CRN) REFERENCES classes
);

--Enrollment
CREATE TABLE enrollment
(CRN int PRIMARY KEY,
 enrollment int,
 enrollmentMax int,
 waitlist int,
 FOREIGN KEY (CRN) REFERENCES classes
);

--Taken Classes
CREATE TABLE taken
(username varchar (50),
 sID varchar (10),
 cID int,
 PRIMARY KEY (username, sID, cID),
 FOREIGN KEY (username) REFERENCES accounts,
 FOREIGN KEY (sID, cID) REFERENCES courses
);

--User Schedules
CREATE TABLE schedules
(username varchar (50),
 sID varchar (10),
 cID int,
 sIndex int,
 PRIMARY KEY (username, sID, cID, sIndex),
 FOREIGN KEY (username) REFERENCES accounts,
 FOREIGN KEY (sID, cID) REFERENCES courses
);
