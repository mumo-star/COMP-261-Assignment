import streamlit as st
import requests
import pandas as pd
from .utils import get_api_base_url, get_auth_headers, handle_api_error

def students_page():
    st.title("Student Management System")
    st.markdown("A simplified system to digitize student record handling and grants permisssions to people based on their roles that is admin(lecturers and other staff) or users(students)")
    
    #Display current role and permissions
    st.info(f"Current Role: {st.session_state.role.upper()}")
    if st.session_state.role == "admin":
        st.success("Admin access: You can perform all operations")
    else:
        st.warning("Student access: You can view and search data only")
    
    #Tabbed interface for different operations
    if st.session_state.role == "admin":
        tab1, tab2, tab3, tab4 = st.tabs(["View Students", "Add Student", "Update Student", "Search Student"])
        
        with tab1:
            view_students()
        
        with tab2:
            add_student()
        
        with tab3:
            update_student_tab()
        
        with tab4:
            search_student()
    else:
        tab1, tab2 = st.tabs(["View Students", "Search Student"])
        
        with tab1:
            view_students()
        
        with tab2:
            search_student()

#Display all students in a table with role-based action buttons.
def view_students():
    st.markdown("### All Students")
    
    #Refresh button
    if st.button("Refresh", use_container_width=False):
        st.rerun()
    
    try:
        # Fetch students from API
        with st.spinner("Loading students..."):
            response = requests.get(
                f"{get_api_base_url()}/students/",
                headers=get_auth_headers(),
                timeout=10
            )
        
        if response.status_code == 200:
            students = response.json()
            
            if students:
                #Create DataFrame for display
                df = pd.DataFrame(students)
                df = df[['id', 'name', 'age', 'department', 'reg_no', 'created_at']]
                df.columns = ['ID', 'Name', 'Age', 'Department', 'Registration No', 'Created At']
                df['Created At'] = pd.to_datetime(df['Created At']).dt.strftime('%Y-%m-%d %H:%M')
                
                #Show role-specific information
                if st.session_state.role == "admin":
                    st.info("Admin mode: Delete options available below table")
                else:
                    st.info("Student mode: View only")
                
                #Display student data
                st.dataframe(df, use_container_width=True)
                
                #Admin delete options in view students
                if st.session_state.role == "admin" and students:
                    st.markdown("---")
                    st.markdown("### Admin Actions - Delete Students")
                    
                    # Create a more compact delete interface
                    delete_options = {f"{s['name']} ({s['reg_no']}) - ID: {s['id']}": s['id'] for s in students}
                    selected_to_delete = st.selectbox("Select student to delete:", options=list(delete_options.keys()), key="delete_view_student")
                    
                    if selected_to_delete:
                        student_id = delete_options[selected_to_delete]
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Delete Selected Student", type="secondary", key="confirm_delete_view"):
                                delete_student(student_id)
                        with col2:
                            st.info(f"Student ID: {student_id}")
                        
            else:
                st.warning("No students found")
                st.info("Add some students to see them here!")
                
        else:
            handle_api_error(response)
            
    except requests.exceptions.Timeout:
        st.error("Students data request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check if backend is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

#Add new student for
def add_student():
    st.markdown("### Add New Student")
    
    # Check admin permissions
    if st.session_state.role != "admin":
        st.error("Only administrators can add students")
        return
    
    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("Student Name", placeholder="Enter student name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        reg_no = st.text_input("Registration Number", placeholder="Enter registration number")
        department = st.text_input("Department", placeholder="Enter department")
        submit_button = st.form_submit_button("Add Student", use_container_width=True, type="primary")
        
        if submit_button:
            if name and age and reg_no and department:
                with st.spinner("Adding student..."):
                    try:
                        response = requests.post(
                            f"{get_api_base_url()}/students/",
                            json={
                                "name": name,
                                "age": age,
                                "reg_no": reg_no,
                                "department": department
                            },
                            headers=get_auth_headers(),
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            st.success("Student added successfully!")
                            st.rerun()
                        else:
                            handle_api_error(response)
                            
                    except requests.exceptions.Timeout:
                        st.error("Add student request timed out. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("Connection error. Please check if backend is running.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")
            else:
                st.error("Please fill in all fields")

#Update student tab (admin o
def update_student_tab():
    #Check admin permissions
    if st.session_state.role != "admin":
        st.error("Only admins can update students!")
        return
    
    st.markdown("### Update Student")
    
    # Get all students for selection
    try:
        response = requests.get(
            f"{get_api_base_url()}/students/",
            headers=get_auth_headers(),
            timeout=10
        )
        
        if response.status_code == 200:
            students = response.json()
            
            if students:
                # Create student selection dropdown
                student_options = {f"{s['name']} ({s['reg_no']})": s['id'] for s in students}
                selected_student = st.selectbox("Select student to update:", options=list(student_options.keys()), key="update_student_tab")
                
                if selected_student:
                    student_id = student_options[selected_student]
                    update_student_form(student_id)
            else:
                st.warning("No students available to update")
        else:
            handle_api_error(response)
            
    except requests.exceptions.Timeout:
        st.error("Students data request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check if backend is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
#Update student form (admin only).
def update_student_form(student_id):
       
    #Check admin permissions
    if st.session_state.role != "admin":
        st.error("Only admins can update students!")
        return
    
    st.markdown(f"### Update Student {student_id}")
    
    try:
        # Fetch existing student data
        with st.spinner("Loading student data..."):
            response = requests.get(
                f"{get_api_base_url()}/students/{student_id}",
                headers=get_auth_headers(),
                timeout=10
            )
        
        if response.status_code == 200:
            student = response.json()
            
            with st.form(f"update_student_form_{student_id}"):
                name = st.text_input("Student Name", value=student['name'])
                age = st.number_input("Age", min_value=1, max_value=100, step=1, value=student['age'])
                reg_no = st.text_input("Registration Number", value=student['reg_no'])
                department = st.text_input("Department", value=student['department'])
                submit_button = st.form_submit_button("Update Student", use_container_width=True, type="primary")
                
                if submit_button:
                    # Only send changed fields
                    update_data = {}
                    if name != student['name']:
                        update_data['name'] = name
                    if age != student['age']:
                        update_data['age'] = age
                    if reg_no != student['reg_no']:
                        update_data['reg_no'] = reg_no
                    if department != student['department']:
                        update_data['department'] = department
                    
                    if update_data:
                        with st.spinner("Updating student..."):
                            try:
                                response = requests.put(
                                    f"{get_api_base_url()}/students/{student_id}",
                                    json=update_data,
                                    headers=get_auth_headers(),
                                    timeout=10
                                )
                                
                                if response.status_code == 200:
                                    st.success("Student updated successfully!")
                                    st.rerun()
                                else:
                                    handle_api_error(response)
                                    
                            except requests.exceptions.Timeout:
                                st.error("Update student request timed out. Please try again.")
                            except requests.exceptions.ConnectionError:
                                st.error("Connection error. Please check if backend is running.")
                            except Exception as e:
                                st.error(f"An unexpected error occurred: {str(e)}")
                    else:
                        st.info("No changes detected")
        else:
            handle_api_error(response)
            
    except requests.exceptions.Timeout:
        st.error("Student data request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check if backend is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        
#Delete a student (admin only)
def delete_student(student_id):
   
    #Check admin permissions
    if st.session_state.role != "admin":
        st.error("Only admins can delete students!")
        return
    
    try:
        with st.spinner("Deleting student..."):
            response = requests.delete(
                f"{get_api_base_url()}/students/{student_id}",
                headers=get_auth_headers(),
                timeout=10
            )
            
        if response.status_code == 200:
            st.success("Student deleted successfully!")
            st.rerun()
        else:
            handle_api_error(response)
            
    except requests.exceptions.Timeout:
        st.error("Delete student request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check if backend is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        
#Search for students by ID or registration numb
def search_student():
    st.markdown(" Search Students")
    
    search_type = st.radio("Search by:", ["Registration Number", "Student ID"])
    
    if search_type == "Registration Number":
        reg_no = st.text_input("Enter Registration Number", placeholder="e.g., REG001")
        if reg_no and st.button("Search by Registration"):
            try:
                response = requests.get(
                    f"{get_api_base_url()}/students/reg/{reg_no}",
                    headers=get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    student = response.json()
                    df = pd.DataFrame([student])
                    df = df[['id', 'name', 'age', 'department', 'reg_no', 'created_at']]
                    df.columns = ['ID', 'Name', 'Age', 'Department', 'Registration No', 'Created At']
                    df['Created At'] = pd.to_datetime(df['Created At']).dt.strftime('%Y-%m-%d %H:%M')
                    
                    st.dataframe(df, use_container_width=True)
                    
                    # Admin delete option for search results
                    if st.session_state.role == "admin":
                        st.markdown("---")
                        st.markdown("### Admin Actions")
                        if st.button(f"Delete {student['name']} (ID: {student['id']})", type="secondary", key=f"delete_search_{student['id']}"):
                            delete_student(student['id'])
                else:
                    handle_api_error(response)
                    
            except requests.exceptions.Timeout:
                st.error("Search request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Connection error. Please check if backend is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
    
    else:
        student_id = st.number_input("Enter Student ID", min_value=1, step=1)
        if student_id and st.button("Search by ID"):
            try:
                response = requests.get(
                    f"{get_api_base_url()}/students/{student_id}",
                    headers=get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    student = response.json()
                    df = pd.DataFrame([student])
                    df = df[['id', 'name', 'age', 'department', 'reg_no', 'created_at']]
                    df.columns = ['ID', 'Name', 'Age', 'Department', 'Registration No', 'Created At']
                    df['Created At'] = pd.to_datetime(df['Created At']).dt.strftime('%Y-%m-%d %H:%M')
                    
                    st.dataframe(df, use_container_width=True)
                    
                    # Admin delete option for search results
                    if st.session_state.role == "admin":
                        st.markdown("---")
                        st.markdown("### Admin Actions")
                        if st.button(f"Delete {student['name']} (ID: {student['id']})", type="secondary", key=f"delete_search_{student['id']}"):
                            delete_student(student['id'])
                else:
                    handle_api_error(response)
                    
            except requests.exceptions.Timeout:
                st.error("Search request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Connection error. Please check if backend is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
