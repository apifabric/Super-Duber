# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Personnel(Base):
    """description: Table to store personnel details."""
    __tablename__ = 'personnel'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone_number = Column(String(50), nullable=True)

class Skill(Base):
    """description: Table to store skill details."""
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    description = Column(String(250), nullable=True)

class JobRole(Base):
    """description: Table to store job role details."""
    __tablename__ = 'job_role'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=True)
    description = Column(String(250), nullable=True)

class RoleSkillRequirement(Base):
    """description: Table to store skill requirements for a job role."""
    __tablename__ = 'role_skill_requirement'
    id = Column(Integer, primary_key=True)
    job_role_id = Column(Integer, ForeignKey('job_role.id'))
    skill_id = Column(Integer, ForeignKey('skill.id'))
    level_required = Column(String(50), nullable=True)

class PersonnelSkill(Base):
    """description: Table to store skills associated with personnel."""
    __tablename__ = 'personnel_skill'
    id = Column(Integer, primary_key=True)
    personnel_id = Column(Integer, ForeignKey('personnel.id'))
    skill_id = Column(Integer, ForeignKey('skill.id'))
    proficiency_level = Column(String(50), nullable=True)

class Department(Base):
    """description: Table to store department details."""
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    head = Column(Integer, ForeignKey('personnel.id'))

class Project(Base):
    """description: Table to store project details."""
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

class ProjectAssignment(Base):
    """description: Table to store project assignments."""
    __tablename__ = 'project_assignment'
    id = Column(Integer, primary_key=True)
    personnel_id = Column(Integer, ForeignKey('personnel.id'))
    project_id = Column(Integer, ForeignKey('project.id'))
    role = Column(String(100), nullable=True)

class Training(Base):
    """description: Table to store details about training programs."""
    __tablename__ = 'training'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    description = Column(String(250), nullable=True)
    date_provided = Column(Date, nullable=True)

class PersonnelTraining(Base):
    """description: Table to link personnel with their trainings."""
    __tablename__ = 'personnel_training'
    id = Column(Integer, primary_key=True)
    personnel_id = Column(Integer, ForeignKey('personnel.id'))
    training_id = Column(Integer, ForeignKey('training.id'))
    date_completed = Column(Date, nullable=True)

class Feedback(Base):
    """description: Table to store feedback given by personnel for projects."""
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    personnel_id = Column(Integer, ForeignKey('personnel.id'))
    project_id = Column(Integer, ForeignKey('project.id'))
    feedback_note = Column(String(500), nullable=True)

class Meeting(Base):
    """description: Table to store meeting details."""
    __tablename__ = 'meeting'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=True)
    description = Column(String(250), nullable=True)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    personnel1 = Personnel(id=1, first_name='John', last_name='Doe', email='john.doe@example.com', phone_number='123-456-7890')
    
    
    
    session.add_all([personnel1])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
