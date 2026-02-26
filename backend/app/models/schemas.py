from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import Literal

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    role: Literal["employee", "manager"]
    department: str
    status: Literal["active", "inactive"]
    password: str




class EmployeeResponse(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    role: str
    department: Optional[str]
    status: Optional[str]
    risk_score: Optional[int]

    class Config:
        orm_mode = True