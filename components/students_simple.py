import streamlit as st
import pandas as pd
from .database_utils import get_all_students, add_student, update_student, delete_student

def students_page():
    st.title("Student Management System")
    st.markdown("A simplified system to digitize student record handling and grants permisssions to people based on their roles that is admin(lecturers and other staff) or users(students)")
    
    # Display current role and permissions
    st.info(f"Current Role: {st.session_state.role.upper()}")
    if st.session_state.role == "admin":
        st.success("Admin access: You can perform all operations")
    else:
        st.warning("Student access: You can view and search data only")
    
    # Tabbed interface for different operations
    if st.session_state.role == "admin":
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["View Students", "Add Student", "Update Student", "Delete Student", "Search Student"])
        
        with tab1:
            view_students()
        
        with tab2:
            add_student_form()
        
        with tab3:
            update_student_tab()
        
        with tab4:
            delete_student_tab()
        
        with tab5:
            search_student()
    else:
        tab1, tab2 = st.tabs(["View Students", "Search Student"])
        
        with tab1:
            view_students()
        
        with tab2:
            search_student()

def view_students():
    st.markdown("### All Students")
    
    # Refresh button
    if st.button("Refresh", use_container_width=False):
        st.rerun()
    
    try:
        # Fetch students directly from database
        students_df = get_all_students()
        
        if students_df.empty:
            st.info("No students found in the database.")
        else:
            # Display students in a table
            st.dataframe(students_df, use_container_width=True)
            
            # Note for admin about update/delete tabs
            if st.session_state.role == "admin" and not students_df.empty:
                st.info("💡 Admin: Use the 'Update Student' and 'Delete Student' tabs to modify student records.")
    
    except Exception as e:
        st.error(f"Error loading students: {str(e)}")

def add_student_form():
    st.markdown("### Add New Student")
    
    with st.form("add_student_form"):
        name = st.text_input("Full Name*", placeholder="Enter student's full name")
        reg_no = st.text_input("Registration Number*", placeholder="Enter registration number")
        department = st.text_input("Department*", placeholder="Enter department name")
        age = st.number_input("Age*", min_value=16, max_value=100, value=18)
        
        submitted = st.form_submit_button("Add Student", use_container_width=True)
        
        if submitted:
            if name and reg_no and department:
                if add_student(name, reg_no, department, age):
                    st.success(f"Student '{name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add student. Please try again.")
            else:
                st.error("Please fill in all required fields.")

def update_student_tab():
    st.markdown("### Update Student")
    
    # Get all students for selection
    students_df = get_all_students()
    
    if students_df.empty:
        st.info("No students available to update.")
        return
    
    with st.form("update_student_form"):
        student_id = st.selectbox(
            "Select student to update:",
            options=students_df['id'].tolist(),
            format_func=lambda x: f"ID: {x} - {students_df[students_df['id'] == x]['name'].iloc[0]}"
        )
        
        # Get current student data
        current_student = students_df[students_df['id'] == student_id].iloc[0]
        
        name = st.text_input("Full Name*", value=current_student['name'])
        reg_no = st.text_input("Registration Number*", value=current_student['reg_no'])
        department = st.text_input("Department*", value=current_student['department'])
        age = st.number_input("Age*", min_value=16, max_value=100, value=int(current_student['age']))
        
        submitted = st.form_submit_button("Update Student", use_container_width=True)
        
        if submitted:
            if name and reg_no and department:
                if update_student(student_id, name, reg_no, department, age):
                    st.success(f"Student '{name}' updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update student. Please try again.")
            else:
                st.error("Please fill in all required fields.")

def search_student():
    st.markdown("### Search Students")
    
    search_term = st.text_input("Search by name, registration number, or department:", placeholder="Enter search term...")
    
    if search_term:
        students_df = get_all_students()
        
        if students_df.empty:
            st.info("No students found in the database.")
            return
        
        # Filter students based on search term
        filtered_df = students_df[
            students_df['name'].str.contains(search_term, case=False, na=False) |
            students_df['reg_no'].str.contains(search_term, case=False, na=False) |
            students_df['department'].str.contains(search_term, case=False, na=False)
        ]
        
        if filtered_df.empty:
            st.warning(f"No students found matching '{search_term}'")
        else:
            st.success(f"Found {len(filtered_df)} student(s) matching '{search_term}'")
            st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("Enter a search term to find students.")

def delete_student_tab():
    st.markdown("### Delete Student")
    
    # Get all students for selection
    students_df = get_all_students()
    
    if students_df.empty:
        st.info("No students available to delete.")
        return
    
    with st.form("delete_student_form"):
        student_id = st.selectbox(
            "Select student to delete:",
            options=students_df['id'].tolist(),
            format_func=lambda x: f"ID: {x} - {students_df[students_df['id'] == x]['name'].iloc[0]}"
        )
        
        # Get current student data for confirmation
        current_student = students_df[students_df['id'] == student_id].iloc[0]
        
        # Show student details for confirmation
        st.markdown("#### Student to Delete:")
        st.write(f"**Name:** {current_student['name']}")
        st.write(f"**Registration No:** {current_student['reg_no']}")
        st.write(f"**Department:** {current_student['department']}")
        st.write(f"**Age:** {current_student['age']}")
        
        st.warning("⚠️ This action cannot be undone!")
        
        submitted = st.form_submit_button("Delete Student", use_container_width=True, type="primary")
        
        if submitted:
            if delete_student(student_id):
                st.success(f"Student '{current_student['name']}' deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete student. Please try again.")
