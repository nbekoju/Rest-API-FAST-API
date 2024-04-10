from fastapi import FastAPI, HTTPException, status
import logging

from database import create_connection
from models import Employee
from helper_function import insertInitialData, add_employee, get_employee_by_id

logging.basicConfig(level=logging.INFO)

app = FastAPI()
insertInitialData()


@app.get("/employees")
def get_all_employee():
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM employee")
        employees = c.fetchall()
    conn.close()

    employees_data = []
    for employee in employees:
        employee_dict = {
            "id": employee[0],
            "name": employee[1],
            "age": employee[2],  
        }
        employees_data.append(employee_dict)
    
    return employees_data

@app.get("/employees/{id}")
def get_employee_by_id_handler(id: int):
    employee = get_employee_by_id(id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {id} not found",
        )
    return {"employee_detail": employee}


@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee_handler(employee: Employee):
    add_employee(employee)
    return {"message": "Employee added successfully", "employee": employee}


@app.delete("/employees/{id}")
def delete_employee(id: int):
    """
    delete the employee if it is present in table, else return 404 error message
    """
    employee = get_employee_by_id(id)
    if employee:
        conn = create_connection()
        with conn:
            c = conn.cursor()
            c.execute("DELETE FROM employee WHERE id=?", (id,))
        conn.close()
        return {"message": f"Employee with ID {id} successfully deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {id} not found",
        )


@app.put("/employees/{id}")
def update_employee(id: int, employee: Employee):
    """
    update the employee with given id if found in database, else return 404 error message
    """
    present_employee = get_employee_by_id(id)
    if not present_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {id} not found",
        )

    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(
            "UPDATE employee SET name = ?, department = ? WHERE id = ?",
            (employee.name, employee.department, id),
        )

    updated_employee_details = get_employee_by_id(id)

    return {"updated_employee": updated_employee_details}
