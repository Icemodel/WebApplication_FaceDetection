from sqlalchemy import Integer, String, ForeignKey, CheckConstraint, DateTime, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from base import Base

# สร้างโมเดลสำหรับฐานข้อมูล
class PersonDB(Base):
    __tablename__ = "person"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    role_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('role.id'), nullable= True)
    faculty_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('faculty.id'), nullable = True)
    department_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('department.id'), nullable= True)

    #CheckConstraint
    __table_args__ = (
        CheckConstraint("age >= 1 AND age <=130", name="check_age"),
    )

    #Relations
    role: Mapped["RoleDB"] = relationship(back_populates="person")
    faculty: Mapped["FacultyDB"] = relationship(back_populates="person")
    department: Mapped["DepartmentDB"] = relationship(back_populates="person")
    contact : Mapped["ContactDB"] = relationship(back_populates="person")
    floor_person: Mapped["FloorPersonDB"] = relationship(back_populates="person")
    user: Mapped[List["UserDB"]] = relationship(back_populates="person")
    faces: Mapped[List["FaceDB"]] = relationship(back_populates="person")  

class UserDB(Base):
    #Columns
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Integer, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Integer, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    person_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("person.id"), nullable=True)

    #Relations
    person: Mapped[Optional["PersonDB"]] = relationship(back_populates="user") 

class RoleDB(Base):
    #Columns
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    #Relations
    person: Mapped[List["PersonDB"]] = relationship(back_populates="role")

class FacultyDB(Base):
    __tablename__ = "faculty"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    #Relations
    person: Mapped[List["PersonDB"]] = relationship(back_populates="faculty")

class DepartmentDB(Base):
    __tablename__ = "department"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    #Relations
    person: Mapped[List["PersonDB"]] = relationship(back_populates="department")

class ContactDB(Base):
    __tablename__ = "contact"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    person_id: Mapped[int] = mapped_column(Integer,ForeignKey("person.id"))
    phone_number: Mapped[str] = mapped_column(String(10), nullable=False)
    lineID: Mapped[Optional[str]] = mapped_column(String(50), nullable = True)
    facebook: Mapped[Optional[str]] = mapped_column(String(50), nullable= True)

    #Relations
    person: Mapped[List["PersonDB"]] = relationship(back_populates="contact")

class FloorDB(Base):
    __tablename__ = "floor"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    floor_name: Mapped[str] = mapped_column(String(50), nullable=False)

    #Relations
    floor_camera: Mapped[List["FloorCameraDB"]] = relationship(back_populates="floor")
    floor_person: Mapped[List["FloorPersonDB"]] = relationship(back_populates="floor")

class CameraDB(Base):
    __tablename__ = "camera"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    camera_name: Mapped[str] = mapped_column(String(50), nullable=False)

    #Relations
    floor_camera: Mapped[List["FloorCameraDB"]] = relationship(back_populates="camera")

class FloorCameraDB(Base):
    __tablename__ = "floor_camera"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    floor_id: Mapped[int] = mapped_column(Integer, ForeignKey("floor.id"))
    camera_id: Mapped[int] = mapped_column(Integer, ForeignKey("camera.id"))
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    #Relations
    floor: Mapped["FloorDB"] = relationship(back_populates="floor_camera")
    camera: Mapped["CameraDB"] = relationship(back_populates="floor_camera")

class FloorPersonDB(Base):
    __tablename__ = "floor_person"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    floor_id: Mapped[int] = mapped_column(Integer, ForeignKey("floor.id"))
    person_id: Mapped[int] = mapped_column(Integer, ForeignKey("person.id"))
    entered_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    exited_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration: Mapped[timedelta | None] = mapped_column(Interval, nullable=True)

    #Relations
    floor: Mapped["FloorDB"] = relationship(back_populates="floor_person")
    person: Mapped["PersonDB"] = relationship(back_populates="floor_person")

class FaceDB(Base):
    __tablename__ = "faces"
    #Columns
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    person_id: Mapped[int] = mapped_column(Integer,ForeignKey("person.id"))
    embedding: Mapped[List[float]] = mapped_column(Vector(128), nullable=False)  

    #Relations
    person: Mapped["PersonDB"] = relationship(back_populates="faces")


