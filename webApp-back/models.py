from sqlalchemy import Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .database import Base

# สร้างโมเดลสำหรับฐานข้อมูล
class PersonDB(Base):
    __tablename__ = "person"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    role_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('role.id'), nullable= True)
    faculty_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('faculty.id'), nullable = True)
    department_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('department.id'), nullable= True)

    #CheckConstraint
    __table_args__ = (
        CheckConstraint("age >= 1 AND age <=130", name="check_age"),
    )

    #Relations
    role: Mapped["RoleDB"] = relationship(back_populates="users")
    faculty: Mapped["FacultyDB"] = relationship(back_populates="users")
    department: Mapped["DepartmentDB"] = relationship(back_populates="users")
    contact : Mapped["ContactDB"] = relationship(back_populates="users")
    floor: Mapped["FloorDB"] = relationship(back_populates="users")

class RoleDB(Base):
    #Columns
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50))

    #Relations
    users: Mapped[List["PersonDB"]] = relationship(back_populates="role")

class FacultyDB(Base):
    __tablename__ = "faculty"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50))
    
    #Relations
    users: Mapped[List["PersonDB"]] = relationship(back_populates="faculty")

class DepartmentDB(Base):
    __tablename__ = "department"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50))

    #Relations
    users: Mapped[List["PersonDB"]] = relationship(back_populates="department")

class ContactDB(Base):
    __tablename__ = "contact"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    person_id: Mapped[int] = mapped_column(Integer,ForeignKey("person.id"))
    phone_number: Mapped[str] = mapped_column(String(10))
    lineID: Mapped[Optional[str]] = mapped_column(String(50), nullable = True)
    facebook: Mapped[Optional[str]] = mapped_column(String(50), nullable= True)

    #Relations
    users: Mapped[List["PersonDB"]] = relationship(back_populates="contact")

class FloorDB(Base):
    __tablename__ = "floor"
    #Columns
    floorNum: Mapped[int] = mapped_column(Integer, primary_key = True)
    security_cam_id: Mapped[int] = mapped_column(Integer, nullable=False)
    person_id: Mapped[int] = mapped_column(Integer,ForeignKey("person.id"))

    #CheckConstraint
    __table_args__ = (
    CheckConstraint("security_cam_id >= 1", name="check_security_cam_id"),
    )

    #Relations
    users: Mapped[List["PersonDB"]] = relationship(back_populates="floor")

class FaceDB(Base):
    __tablename__ = "faces"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    person_id: Mapped[int] = mapped_column(Integer,ForeignKey("person.id"))
    embedding: Mapped[List[float]] = mapped_column(String, nullable=False)  # Store as a string representation of a list

    #Relations
    users: Mapped["PersonDB"] = relationship(back_populates="faces")

