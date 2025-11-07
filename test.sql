-- 1) 後勤 / 組別
CREATE TABLE Logistic (
  iName        VARCHAR(50) PRIMARY KEY,   -- 組別名稱
  job_desc     TEXT                       -- 工作內容
);

-- 2) 學生
CREATE TABLE Student (
  sId          VARCHAR(10) PRIMARY KEY,
  sName        VARCHAR(50) NOT NULL,
  gender       VARCHAR(10) CHECK (gender IN ('Male','Female','Other')),
  grade        INT,
  department   VARCHAR(50),
  isMember     BOOLEAN DEFAULT FALSE,
  iName        VARCHAR(50),               -- 所屬組別（可為空）
  CONSTRAINT fk_student_group
    FOREIGN KEY (iName) REFERENCES Logistic(iName)
      ON UPDATE CASCADE ON DELETE SET NULL
);

-- 3) 器材
CREATE TABLE Equipment (
  eId          VARCHAR(10) PRIMARY KEY,
  eName        VARCHAR(100) NOT NULL,
  eLocation    VARCHAR(100),
  quantity     INT NOT NULL CHECK (quantity >= 0),
  note         TEXT,
  iName        VARCHAR(50),               -- 管轄組別（可為空）
  CONSTRAINT fk_equipment_group
    FOREIGN KEY (iName) REFERENCES Logistic(iName)
      ON UPDATE CASCADE ON DELETE SET NULL
);

-- 4) 活動
CREATE TABLE Activity (
  aSeq         INT PRIMARY KEY,           -- 活動序號
  aName        VARCHAR(100) NOT NULL,
  "date"       DATE NOT NULL,
  aLocation    VARCHAR(100) NOT NULL
);

-- 5) 節目（某活動在某時間要唱/演出的曲目）
CREATE TABLE Program (
  aSeq         INT NOT NULL,
  "time"       TIME NOT NULL,
  song         VARCHAR(100) NOT NULL,
  PRIMARY KEY (aSeq, "time"),
  CONSTRAINT fk_program_activity
    FOREIGN KEY (aSeq) REFERENCES Activity(aSeq)
      ON UPDATE CASCADE ON DELETE CASCADE
);

-- 6) 參與（學生參加哪個活動）
CREATE TABLE JoinActivity (
  aSeq         INT NOT NULL,
  sId          VARCHAR(10) NOT NULL,
  PRIMARY KEY (aSeq, sId),
  CONSTRAINT fk_join_activity
    FOREIGN KEY (aSeq) REFERENCES Activity(aSeq)
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_join_student
    FOREIGN KEY (sId)  REFERENCES Student(sId)
      ON UPDATE CASCADE ON DELETE CASCADE
);

-- 7) 演出（學生在某活動的某節目時間上台）
CREATE TABLE Perform (
  aSeq         INT NOT NULL,
  "time"       TIME NOT NULL,
  sId          VARCHAR(10) NOT NULL,
  PRIMARY KEY (aSeq, "time", sId),
  CONSTRAINT fk_perform_program
    FOREIGN KEY (aSeq, "time") REFERENCES Program(aSeq, "time")
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_perform_student
    FOREIGN KEY (sId) REFERENCES Student(sId)
      ON UPDATE CASCADE ON DELETE CASCADE
);

-- 8) 使用（活動節目時間使用哪些器材）
CREATE TABLE UseEquipment (
  eId          VARCHAR(10) NOT NULL,
  "time"       TIME NOT NULL,
  aSeq         INT NOT NULL,
  PRIMARY KEY (eId, aSeq, "time"),
  CONSTRAINT fk_use_equipment
    FOREIGN KEY (eId) REFERENCES Equipment(eId)
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_use_program
    FOREIGN KEY (aSeq, "time") REFERENCES Program(aSeq, "time")
      ON UPDATE CASCADE ON DELETE CASCADE
);
