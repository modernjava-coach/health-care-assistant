from fastapi import FastAPI
import uvicorn
from .api.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare AI Assistant", 
    description="API for SOAP Note and Medical Code Generation using AWS Bedrock and Google Vertex AI"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router, prefix="/api/v1/medical", tags=["medical"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
