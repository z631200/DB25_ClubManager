CREATE TABLE Logistic (
    lName VARCHAR(50) PRIMARY KEY,
    Job_Desc VARCHAR(100)
);

CREATE TABLE Activity (
    aSeq CHAR(10) PRIMARY KEY,
    aName VARCHAR(50) NOT NULL,
    activityDate DATE NOT NULL,
    aLocation VARCHAR(50) NOT NULL
);

CREATE TABLE Program (
    aSeq CHAR(10),              -- 對應活動編號（外鍵）
    programTime TIME,           -- 與 aSeq 組成複合主鍵
    Song VARCHAR(100),
    PRIMARY KEY (aSeq, programTime),
    FOREIGN KEY (aSeq) REFERENCES Activity(aSeq)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Student (
    sID CHAR(10) PRIMARY KEY,
    sName VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    Grade INT,
    Department VARCHAR(50) NOT NULL,
    isMember BOOLEAN NOT NULL,
    lName VARCHAR(50) NULL,
    FOREIGN KEY (lName) REFERENCES Logistic(lName)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Equipment (
    eID CHAR(10) PRIMARY KEY,
    eName VARCHAR(50),
    eLocation VARCHAR(50),
    Quantity INT,
    Note VARCHAR(100),
    lName VARCHAR(50),
    FOREIGN KEY (lName) REFERENCES Logistic(lName)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 學生參與活動：StudentJoin
DROP TABLE IF EXISTS StudentJoin;
CREATE TABLE StudentJoin (
    sID CHAR(10),
    aSeq CHAR(10),
    PRIMARY KEY (sID, aSeq),
    FOREIGN KEY (sID) REFERENCES Student(sID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (aSeq) REFERENCES Activity(aSeq)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 學生參與節目：Perform （參照 Program 複合鍵）
DROP TABLE IF EXISTS StudentPerform;
CREATE TABLE StudentPerform (
    sID CHAR(10),
    aSeq CHAR(10),
    programTime TIME,
    PRIMARY KEY (sID, aSeq, programTime),
    FOREIGN KEY (sID) REFERENCES Student(sID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (aSeq, programTime) REFERENCES Program(aSeq, programTime)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 節目使用器材：Use （參照 Program 複合鍵）
DROP TABLE IF EXISTS EquipmentUse;
CREATE TABLE EquipmentUse (
    eID CHAR(10),
    aSeq CHAR(10),
    programTime TIME,
    PRIMARY KEY (eID, aSeq, programTime),
    FOREIGN KEY (eID) REFERENCES Equipment(eID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (aSeq, programTime) REFERENCES Program(aSeq, programTime)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);