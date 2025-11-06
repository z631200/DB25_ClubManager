ALTER TABLE member
  ADD COLUMN lname VARCHAR(64),
  ADD COLUMN fname VARCHAR(64);

UPDATE member
SET
  lname = substr(name, 1, 1),
  fname = substr(name, 2);

ALTER TABLE member
    DROP COLUMN name;

INSERT INTO member (mid, lname, fname, account, password, identity)
VALUES
(6, '王', '大明', 'abc', 'abc', 'user');

