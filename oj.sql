PRAGMA FOREIGN_KEYS = ON;

CREATE TABLE users (
  user_id       INTEGER PRIMARY KEY,
  secret        BINARY(60),
  role          CHAR(4)
);

CREATE TABLE problems (
  prob_id       INTEGER PRIMARY KEY,
  created_by    INTEGER REFERENCES users (user_id),
  created_at    INTEGER,
  last_modified DATETIME
  due_when        DATETIME
  description     TEXT
);

CREATE TABLE testcases (
  case_id       INTEGER PRIMARY KEY,
  prob_id       INTEGER REFERENCES problems (prob_id),
  created_by    INTEGER REFERENCES users    (user_id),
  created_at    DATETIME,
  ref_in_file    CHAR(255),
  ref_out_file  CHAR(255)
);

CREATE TABLE submissions (
  sub_id        INTEGER PRIMARY KEY,
  prob_id       INTEGER REFERENCES problems (prob_id),
  sub_type      CHAR(8),
  content        TEXT,
  languange      TEXT,
  submitted_at   DATETIME
);

CREATE TABLE evaluations (
  eval_id       INTEGER PRIMARY KEY,
  sub_id        INTEGER REFERENCES submissions (sub_id),
  case_id       INTEGER REFERENCES testcases   (case_id),
  evaluated_at  INTEGER,
  status        CHAR(16) DEFAULT "PENDING"
);