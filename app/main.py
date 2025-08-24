import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Self-Programming AI",
    description="ذكاء اصطناعي قادر على البرمجة والتعلم الذاتي",
    version="0.1.0"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        from app.ai_core import AICore
        from app.knowledge_manager import KnowledgeManager
        
        app.state.ai_core = AICore()
        app.state.knowledge_manager = KnowledgeManager()
        await app.state.ai_core.initialize()
        logger.info("AI Core initialized successfully on Render")
    except Exception as e:
        logger.error(f"Failed to initialize AI Core: {e}")

@app.get("/")
async def root():
    return {
        "message": "Self-Programming AI API", 
        "status": "active",
        "platform": "Render.com"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "version": "0.1.0",
        "platform": "Render.com"
    }

# باقي ال endpoints تبقى كما هي...

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)