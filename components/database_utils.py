"""
Direct database access utilities for Streamlit frontend
"""

import sqlite3
import pandas as pd

def get_db_connection():
    """Get SQLite database connection"""
    return sqlite3.connect('student_management.db')

def get_all_students():
    """Get all students from database directly"""
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT id, name, age, reg_no, department FROM students ORDER BY id", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def add_student(name, reg_no, department, age):
    """Add student directly to database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, reg_no, department, age) VALUES (?, ?, ?, ?)",
            (name, reg_no, department, age)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def update_student(student_id, name, reg_no, department, age):
    """Update student directly in database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET name=?, reg_no=?, department=?, age=? WHERE id=?",
            (name, reg_no, department, age, student_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def delete_student(student_id):
    """Delete student directly from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False
