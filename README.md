# SMS (Student Management System)

A simplified system to digitize student record handling with role-based access control.

## Features

### Core Functionality
- **Student Management**: Complete CRUD operations (Create, Read, Update, Delete).
- **Department Tracking**: Students can be assigned to different departments.
- **Role-Based Access**: Student and Admin roles with different permissions.
- **Search**: Find students by ID, registration number.

### Technical Features
- **FastAPI Backend**: RESTful API.
- **Streamlit Frontend**: Used to design Ui and is also apython framework.
- **SQLite Database**: Lightweight, file-based database.
- **Error Handling**: Comprehensive error messages and validation.

## Project Structure
- app.py- used to design interface thet is the main streamlit application
- main.py- FastAPI backend server
- requirements.txt- lists all the required packages
- students.py- performs Student CRUD operations
- utils.py- performs Utility functions
- students.py- Student API endpoints
- database.py- Database configuration
- models.py- SQLAlchemy models
- schemas.py- Pydantic schemas

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Docker and Docker Compose (optional, for containerized deployment)

### Option 1: Local Development

1. **Clone or download project**
   ```bash
   cd "SMS App"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Docker Deployment

1. **Clone or download project**
   ```bash
   cd "SMS App"
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   The application will be available at:
   - Frontend: http://localhost:8504
   - Backend API: http://localhost:8001
   - API Docs: http://localhost:8001/docs

## Running the Application

For development with auto-reload:
```bash
# Backend with auto-reload
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Frontend with auto-reload
streamlit run app.py --server.address 0.0.0.0 --server.port 8504
```

## Usage

### Accessing the System

1. **Open web interface**: http://localhost:8504.
2. **Select your role**: Choose "student" or "admin" from the sidebar.
3. **Student Management**: All functionality is directly available in SMS.

### Student Management
- **View Students**: Browse all student records (admin can delete from this view).
- **Add Student**: Create new student records(admin only).
- **Update Student**: Modify existing student information (admin only).
- **Delete Student**: Remove student records (admin only, available in view and search results).
- **Search**: Find students by ID, registration number.

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Key Endpoints
- GET- `/students/`- List all students.
- POST- `/students/`- Create new student.
- GET- `/students/{id}`- Get student by ID.
- GET-  `/students/reg/{reg_no}`- Get student by registration number.
- PUT-  `/students/{id}`- Update student.
- DELETE- `/students/{id}`- Delete student.

## Data Models

### Student Model
- **id**: Integer (Primary Key).
- **name**: String (100 characters).
- **age**: Integer.
- **reg_no**: String (50 characters, unique).
- **department**: String (100 characters).

## Error Handling

The system includes comprehensive error handling:
- **Validation Errors**: Client-side and server-side validation.
- **Connection Errors**: Network connectivity issues.
- **Timeout Errors**: Request timeout handling.
- **Permission Errors**: Role-based access control.
- **User-Friendly Messages**: Clear, actionableerror descriptions.

## Development Notes

### Code Quality
- **Documentation**: Comprehensive docstrings and comments.
- **Type Hints**: Full type annotation coverage.
- **Error Handling**: Try-catch blocks with specific exceptions.
- **Validation**: Input validation and sanitization.
- **Modular Design**: Separated concerns into logical modules.

### Best Practices
- **Security**: Input validation and error handling.
- **Performance**: Efficient database queries and pagination.
- **Maintainability**: Clean, readable code structure.

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change port numbers in run commands
   - Kill existing processes on ports

2. **Database Connection Error**
   - Ensure SQLite file permissions
   - Check if database file exists

3. **Import Errors**
   - Install all required dependencies
   - Check Python version compatibility

4. **Frontend Not Loading**
   - Verify backend is running first
   - Check network connectivity to localhost:8001

### Getting Help

For issues or questions:
- Verify all dependencies are installed
- Ensure both services are running
- Review the API documentation at /docs

