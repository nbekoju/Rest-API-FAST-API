"""
main app with all routes
"""

import logging
from fastapi import FastAPI, HTTPException, status

from database import create_connection
from models import Employee
from helper_function import insert_initial_data, add_employee, get_employee_by_id

logging.basicConfig(level=logging.INFO)

app = FastAPI()
insert_initial_data()


@app.get("/employees")
def get_all_employee():
    """return all the employees from database"""
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
            "department": employee[2],
        }
        employees_data.append(employee_dict)

    return employees_data


@app.get("/employees/{emp_id}")
def get_employee_by_id_handler(emp_id: int):
    """return the employee with given employee id"""
    employee = get_employee_by_id(emp_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found",
        )
    return {"employee_detail": employee}


@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee_handler(employee: Employee):
    """
    create ew employee given the employee information
    """
    add_employee(employee)
    return {"message": "Employee added successfully", "employee": employee}


@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    """
    delete the employee if it is present in table, else return 404 error message
    """
    employee = get_employee_by_id(emp_id)
    if employee:
        conn = create_connection()
        with conn:
            c = conn.cursor()
            c.execute("DELETE FROM employee WHERE id=?", (emp_id,))
        conn.close()
        return {"message": f"Employee with ID {emp_id} successfully deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found",
        )


@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, employee: Employee):
    """
    update the employee with given id if found in database, else return 404 error message
    """
    present_employee = get_employee_by_id(emp_id)
    if not present_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {emp_id} not found",
        )

    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(
            "UPDATE employee SET name = ?, department = ? WHERE id = ?",
            (employee.name, employee.department, emp_id),
        )

    updated_employee_details = get_employee_by_id(emp_id)

    return {"updated_employee": updated_employee_details}
