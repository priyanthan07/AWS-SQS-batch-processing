import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from routes import content_router


# Initialize FastAPI app with metadata
app = FastAPI()

# Define allowed origins for CORSS
origins = ["*"]

# Add CORS middleware to the application
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])



@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Health check endpoint
@app.get("/health")
async def health_check():
    return Response(status_code=200)


# Include routers
app.include_router(content_router, prefix="/generate")


# Start the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
