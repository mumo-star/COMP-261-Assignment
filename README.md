# SMS (Student Management System)

A simplified system to digitize student record handling with role-based access control.

## Features

### Core Functionality
- **Student Management**: Complete CRUD operations (Create, Read, Update, Delete).
- **Department Tracking**: Students can be assigned to different departments.
- **Role-Based Access**: User and Admin roles with different permissions.
- **Search**: Find students by name, registration number, or department.
- **Database Persistence**: SQLite database for data storage.

### Technical Features
- **Streamlit Frontend**: Modern web interface with Python framework.
- **SQLite Database**: Lightweight, file-based database with auto-initialization.
- **Direct Database Access**: No backend API needed - simplified architecture.
- **Error Handling**: Comprehensive error messages and validation.
- **Docker Support**: Containerized deployment ready.

## Project Structure

```
SMS App/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration for deployment
├── README.md             # Project documentation
├── .streamlit/           # Streamlit configuration
│   └── secrets.toml      # Secrets for deployment
├── components/           # UI components
│   ├── __init__.py
│   ├── students_simple.py    # Student management interface
│   └── database_utils.py     # Database operations
└── student_management.db # SQLite database (auto-created)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Docker (optional, for deployment)

### Local Development

1. **Clone or download project**
   ```bash
   cd "SMS App"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

   The application will be available at: http://localhost:8501

## Deployment

### Render Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin master
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Create Web Service with Docker runtime
   - Render will auto-detect your Dockerfile

3. **Configuration**
   - Name: `sms-student-management`
   - Runtime: Docker
   - Instance Type: Free (to start)

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t sms-app .
   ```

2. **Run container**
   ```bash
   docker run -p 8501:8501 sms-app
   ```

## Usage

### Accessing the System

1. **Open web interface**: http://localhost:8501
2. **Select your role**: Choose "user" or "admin" from the sidebar
3. **Start managing students!**

### Role-Based Access

#### User Role
- **View Students**: Browse all student records
- **Search Students**: Find students by name, registration number, or department

#### Admin Role
- **All User permissions** plus:
- **Add Student**: Create new student records
- **Update Student**: Modify existing student information
- **Delete Student**: Remove student records

### Student Management

- **View Students**: Browse all students in a sortable table
- **Add Student**: Enter name, registration number, department, and age
- **Update Student**: Edit existing student information
- **Delete Student**: Remove students from the system
- **Search**: Find students by name, registration number, or department

## Data Models

### Student Model
- **id**: Integer (Primary Key, Auto-increment)
- **name**: String (Full name, required)
- **age**: Integer (Age, required, 16-100)
- **reg_no**: String (Registration number, unique, required)
- **department**: String (Department name, required)
- **created_at**: Timestamp (Auto-generated)
- **updated_at**: Timestamp (Auto-updated)

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change port: `streamlit run app.py --server.port 8502`
   - Kill existing processes on the port

2. **Database Connection Error**
   - Database auto-creates on first run
   - Check file permissions for `student_management.db`

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **Deployment Issues**
   - Ensure `.streamlit/secrets.toml` exists
   - Check Dockerfile configuration
   - Verify all files are pushed to GitHub

### Getting Help

For issues:
- Check the error messages in the app interface
- Verify all dependencies are installed
- Ensure the database file has proper permissions
- Review the deployment logs on Render

## Development Notes

### Architecture
- **Single Service**: Streamlit frontend with direct database access
- **No Backend API**: Simplified architecture for easier deployment
- **Auto-Database**: Database initializes automatically on first run
- **Error Handling**: User-friendly error messages throughout

### Best Practices
- **Input Validation**: All forms have required field validation
- **Error Messages**: Clear, actionable error descriptions
- **Clean Code**: Modular design with separated concerns
- **Security**: Input sanitization and role-based access control

