from pydantic import BaseModel, Field
from typing import Optional

# โมเดลข้อมูลสำหรับรับข้อมูลจาก API
class Person(BaseModel):
    name: str = Field(... , max_length=50)
    surname: str = Field(... , max_length=50)
    age: int = Field(... , ge=0, le=130)
    gender: str = Field(... , max_length=10)
    role_id: Optional[int] = None
    faculty_id: Optional[int] = None
    department_id: Optional[int] = None

class PersonCreate(Person):
    pass

class PersonResponse(PersonCreate):
    id: int
    class Config:
        from_attributes = True

#---------------------------------#

class Role(BaseModel):
    name: str = Field(... , max_length=50)

class RoleCreate(Role):
    pass

class RoleResponse(RoleCreate):
    id:int
    class Config:
        from_attributes = True

#---------------------------------#

class Faculty(BaseModel):
    name: str = Field(... , max_length=50)

class FacultyCreate(Faculty):
    pass

class FacultyResponse(FacultyCreate):
    id:int
    class Config:
        from_attributes = True

#---------------------------------#

class Department(BaseModel):
    name: str = Field(... , max_length=50)

class DepartmentCreate(Department):
    pass

class DepartmentResponse(DepartmentCreate):
    id:int
    class Config:
        from_attributes = True

#---------------------------------#

class Contact(BaseModel):
    person_id: int = Field(... , ge = 1)
    phone_number: str = Field(... , max_length=10)
    lineID: Optional[str] = None
    Facebook: Optional[str] = None

class ContractCreate(Contact):
    pass

class ContractResponse(Contact):
    id: int
    class Config:
        from_attributes = True

#----------------------------------#

class Floor(BaseModel):
    securityCamId: int
    person_id: int = Field(... , ge = 1)

class FloorCreate(Floor):
    pass

class FloorResponse(FloorCreate):
    floorNum:int
    class Config:
        from_attributes = True

#----------------------------------#

class Face(BaseModel):
    person_id: int = Field(... , ge = 1)
    embedding: list[float] = Field(... , min_length=128, max_length=128)

class FaceCreate(Face):
    pass

class FaceResponse(FaceCreate):
    id: int
    class Config:
        from_attributes = True






