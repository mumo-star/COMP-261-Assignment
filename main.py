from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import engine
from models.models import Base
from api.students import router as students_router

#Create database tables
Base.metadata.create_all(bind=engine)

#Initialize FastAPI application
app = FastAPI(
    title="Student Management System API",
    description="A simplified Student Management System with no authentication",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

#Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include API routers
app.include_router(students_router)

#Root endpoint
@app.get("/")
def read_root():
    
    return {
        "message": "Student Management System API", 
        "version": "2.0.0", 
        "auth": "disabled",
        "status": "running"
    }

#Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Run application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
