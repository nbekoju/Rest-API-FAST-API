from fastapi import HTTPException, status
import sqlite3
import logging

from models import Employee
from database import create_connection


logging.basicConfig(level=logging.INFO)


def insertInitialData():
    """
    insert the initial data if the table is empty
    """
    initial_data = [
        (
            "John Doe",
            "AI Engineering",
        ),
        ("Mark Jackson", "Data Engineering"),
    ]

    conn = create_connection()
    # check if the table has data before adding initial data
    with conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM employee")
        row = c.fetchone()
        total_rows = row[0] if row else 0
    # if table has no data, insert initial data
    if total_rows == 0:
        logging.info("Inserting the initial data.")
        with conn:
            c = conn.cursor()
            c.executemany(
                "INSERT INTO employee (name, department) VALUES (?, ?)",
                initial_data,
            )
        conn.close()


def add_employee(employee: Employee):
    """
    helper function to create employee
    """
    conn = create_connection()
    with conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO employee (name, department) VALUES (?, ?)",
            (employee.name, employee.department),
        )
        employee_id = c.lastrowid
    conn.close()
    return employee_id


def get_employee_by_id(employee_id: int):
    conn = create_connection()
    with conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM employee WHERE id=?", (employee_id,))
        employee = c.fetchone()
    conn.close()
    if employee:
        return dict(employee)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"employee with ID {employee_id} not found",
        )
