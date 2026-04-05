import streamlit as st  #Used for UI design
import pandas as pd  #Used for data manipulation
from components.students_simple import students_page

#Configure Streamlit page settings
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    
    #Initialize session state for user data
    if 'role' not in st.session_state:
        st.session_state.role = "user"

    #Sidebar configuration
    with st.sidebar:
        
        #Role selection for the user or admin
        role = st.selectbox(
            "Select Role",
            ["user", "admin"],
            index=0 if st.session_state.role == "user" else 1,
            key="role_selector",
            help="Choose your role to access different features"
        )
        
        #Update session state when role changes
        if role != st.session_state.role:
            st.session_state.role = role
            st.rerun()
        
        st.write(f"Current Role: {st.session_state.role.upper()}")
        st.markdown("---")
        
    
    #Direct to students page (no menu needed)
    students_page()

if __name__ == "__main__":
    main()
