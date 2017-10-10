from sqlalchemy import Column, ForeignKey, INTEGER, TEXT, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __table__ = 'users'
    user_id     = Column(INTEGER, primary_key=True)
    secret = Column(BLOB)
    role   =  Column(TEXT)

class Problem(Base):
    __table__ = 'problems'
    prob_id     = Column(INTEGER, primary_key=True)
    created_by_user_id  = Column(INTEGER, ForeignKey(User.user_id))
    created_by = relationship(User)
    last_modified = Column(INTEGER)
    due_when      = Column(INTEGER)
    decription    = Column(TEXT)

class TestCase(Base):
    __table__ = 'testcases'
    case_id   = Column(INTEGER, primary_key=True)
    prob_id   = Column(INTEGER, ForeignKey(Problem.prob_id))
    problem   = relationship(Problem)
    created_by_user_id = Column(INTEGER, ForeignKey(User.user_id))
    created_by = relationship(User)
    ref_in_file = Column(TEXT)
    ref_out_file = Column(TEXT)

class Submission(Base):
    __table__ = 'submissions'
    sub_id    = Column(INTEGER, primary_key=True)
    prob_id   = Column(INTEGER, ForeignKey(Problem.prob_id))
    problem   = relationship(Problem)
    sub_type  = Column(TEXT)
    content   = Column(TEXT)
    submitted_at = Column(INTEGER)

class Evaluation(Base):
    __table__ = 'evaluations'
    eval_id   = Column(INTEGER, primary_key=True)
    sub_id    = Column(INTEGER, ForeignKey(Submission.sub_id))
    submission = relationship(Submission)
    case_id   = Column(INTEGER, ForeignKey(TestCase.case_id))
    testcase  = relationship(TestCase)
    evaluated_at = Column(INTEGER)
    time_elapsed = Column(INTEGER)
    s