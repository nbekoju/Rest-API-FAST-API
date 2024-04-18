"""structure of the data to add in database"""
from pydantic import BaseModel


class Employee(BaseModel):
    """
    structure of the employee
    """

    name: str
    department: str
