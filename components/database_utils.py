"""
Direct database access utilities for Streamlit frontend
"""

import sqlite3
import pandas as pd
from models.database import get_db_connection

def get_all_students():
    """Get all students from database directly"""
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM students ORDER BY id", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def add_student(name, email, course, age):
    """Add student directly to database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, course, age) VALUES (?, ?, ?, ?)",
            (name, email, course, age)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def update_student(student_id, name, email, course, age):
    """Update student directly in database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET name=?, email=?, course=?, age=? WHERE id=?",
            (name, email, course, age, student_id)
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
