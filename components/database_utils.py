"""
Direct database access utilities for Streamlit frontend
"""

import sqlite3
import pandas as pd
import os
import streamlit as st

def get_db_connection():
    """Get SQLite database connection"""
    db_path = os.path.join(os.getcwd(), 'student_management.db')
    return sqlite3.connect(db_path)

def init_database():
    """Initialize database if it doesn't exist"""
    db_path = os.path.join(os.getcwd(), 'student_management.db')
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                reg_no TEXT UNIQUE NOT NULL,
                department TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

def get_all_students():
    """Get all students from database directly"""
    try:
        init_database()  # Ensure database exists
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT id, name, age, reg_no, department FROM students ORDER BY id", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return pd.DataFrame()

def add_student(name, reg_no, department, age):
    """Add student directly to database"""
    try:
        init_database()  # Ensure database exists
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
        st.error(f"Error adding student: {str(e)}")
        return False

def update_student(student_id, name, reg_no, department, age):
    """Update student directly in database"""
    try:
        init_database()  # Ensure database exists
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
        st.error(f"Error updating student: {str(e)}")
        return False

def delete_student(student_id):
    """Delete student directly from database"""
    try:
        init_database()  # Ensure database exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error deleting student: {str(e)}")
        return False
