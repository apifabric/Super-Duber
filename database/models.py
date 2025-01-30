# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  January 30, 2025 19:57:21
# Database: sqlite:////tmp/tmp.1KE34e24YY-01JJWCHW6RMHA6CJJGN5EKXKXF/Super_Duber/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class JobRole(Base):  # type: ignore
    """
    description: Table to store job role details.
    """
    __tablename__ = 'job_role'
    _s_collection_name = 'JobRole'  # type: ignore

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(250))

    # parent relationships (access parent)

    # child relationships (access children)
    RoleSkillRequirementList : Mapped[List["RoleSkillRequirement"]] = relationship(back_populates="job_role")



class Meeting(Base):  # type: ignore
    """
    description: Table to store meeting details.
    """
    __tablename__ = 'meeting'
    _s_collection_name = 'Meeting'  # type: ignore

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    description = Column(String(250))

    # parent relationships (access parent)

    # child relationships (access children)



class Personnel(Base):  # type: ignore
    """
    description: Table to store personnel details.
    """
    __tablename__ = 'personnel'
    _s_collection_name = 'Personnel'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(50))

    # parent relationships (access parent)

    # child relationships (access children)
    DepartmentList : Mapped[List["Department"]] = relationship(back_populates="personnel")
    FeedbackList : Mapped[List["Feedback"]] = relationship(back_populates="personnel")
    PersonnelSkillList : Mapped[List["PersonnelSkill"]] = relationship(back_populates="personnel")
    PersonnelTrainingList : Mapped[List["PersonnelTraining"]] = relationship(back_populates="personnel")
    ProjectAssignmentList : Mapped[List["ProjectAssignment"]] = relationship(back_populates="personnel")



class Project(Base):  # type: ignore
    """
    description: Table to store project details.
    """
    __tablename__ = 'project'
    _s_collection_name = 'Project'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    FeedbackList : Mapped[List["Feedback"]] = relationship(back_populates="project")
    ProjectAssignmentList : Mapped[List["ProjectAssignment"]] = relationship(back_populates="project")



class Skill(Base):  # type: ignore
    """
    description: Table to store skill details.
    """
    __tablename__ = 'skill'
    _s_collection_name = 'Skill'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(250))

    # parent relationships (access parent)

    # child relationships (access children)
    PersonnelSkillList : Mapped[List["PersonnelSkill"]] = relationship(back_populates="skill")
    RoleSkillRequirementList : Mapped[List["RoleSkillRequirement"]] = relationship(back_populates="skill")



class Training(Base):  # type: ignore
    """
    description: Table to store details about training programs.
    """
    __tablename__ = 'training'
    _s_collection_name = 'Training'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(250))
    date_provided = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    PersonnelTrainingList : Mapped[List["PersonnelTraining"]] = relationship(back_populates="training")



class Department(Base):  # type: ignore
    """
    description: Table to store department details.
    """
    __tablename__ = 'department'
    _s_collection_name = 'Department'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    head = Column(ForeignKey('personnel.id'))

    # parent relationships (access parent)
    personnel : Mapped["Personnel"] = relationship(back_populates=("DepartmentList"))

    # child relationships (access children)



class Feedback(Base):  # type: ignore
    """
    description: Table to store feedback given by personnel for projects.
    """
    __tablename__ = 'feedback'
    _s_collection_name = 'Feedback'  # type: ignore

    id = Column(Integer, primary_key=True)
    personnel_id = Column(ForeignKey('personnel.id'))
    project_id = Column(ForeignKey('project.id'))
    feedback_note = Column(String(500))

    # parent relationships (access parent)
    personnel : Mapped["Personnel"] = relationship(back_populates=("FeedbackList"))
    project : Mapped["Project"] = relationship(back_populates=("FeedbackList"))

    # child relationships (access children)



class PersonnelSkill(Base):  # type: ignore
    """
    description: Table to store skills associated with personnel.
    """
    __tablename__ = 'personnel_skill'
    _s_collection_name = 'PersonnelSkill'  # type: ignore

    id = Column(Integer, primary_key=True)
    personnel_id = Column(ForeignKey('personnel.id'))
    skill_id = Column(ForeignKey('skill.id'))
    proficiency_level = Column(String(50))

    # parent relationships (access parent)
    personnel : Mapped["Personnel"] = relationship(back_populates=("PersonnelSkillList"))
    skill : Mapped["Skill"] = relationship(back_populates=("PersonnelSkillList"))

    # child relationships (access children)



class PersonnelTraining(Base):  # type: ignore
    """
    description: Table to link personnel with their trainings.
    """
    __tablename__ = 'personnel_training'
    _s_collection_name = 'PersonnelTraining'  # type: ignore

    id = Column(Integer, primary_key=True)
    personnel_id = Column(ForeignKey('personnel.id'))
    training_id = Column(ForeignKey('training.id'))
    date_completed = Column(Date)

    # parent relationships (access parent)
    personnel : Mapped["Personnel"] = relationship(back_populates=("PersonnelTrainingList"))
    training : Mapped["Training"] = relationship(back_populates=("PersonnelTrainingList"))

    # child relationships (access children)



class ProjectAssignment(Base):  # type: ignore
    """
    description: Table to store project assignments.
    """
    __tablename__ = 'project_assignment'
    _s_collection_name = 'ProjectAssignment'  # type: ignore

    id = Column(Integer, primary_key=True)
    personnel_id = Column(ForeignKey('personnel.id'))
    project_id = Column(ForeignKey('project.id'))
    role = Column(String(100))

    # parent relationships (access parent)
    personnel : Mapped["Personnel"] = relationship(back_populates=("ProjectAssignmentList"))
    project : Mapped["Project"] = relationship(back_populates=("ProjectAssignmentList"))

    # child relationships (access children)



class RoleSkillRequirement(Base):  # type: ignore
    """
    description: Table to store skill requirements for a job role.
    """
    __tablename__ = 'role_skill_requirement'
    _s_collection_name = 'RoleSkillRequirement'  # type: ignore

    id = Column(Integer, primary_key=True)
    job_role_id = Column(ForeignKey('job_role.id'))
    skill_id = Column(ForeignKey('skill.id'))
    level_required = Column(String(50))

    # parent relationships (access parent)
    job_role : Mapped["JobRole"] = relationship(back_populates=("RoleSkillRequirementList"))
    skill : Mapped["Skill"] = relationship(back_populates=("RoleSkillRequirementList"))

    # child relationships (access children)
