import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# حالة التطبيق
ai_core = None
knowledge_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # بدء التشغيل
    global ai_core, knowledge_manager
    try:
        # استيراد هنا لتجنب مشاكل التبعية عند التشغيل
        from app.ai_core import AICore
        from app.knowledge_manager import KnowledgeManager
        
        ai_core = AICore()
        knowledge_manager = KnowledgeManager()
        await ai_core.initialize()
        logger.info("AI Core initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI Core: {e}")
        raise
    yield
    # إيقاف التشغيل
    if ai_core:
        await ai_core.close()

app = FastAPI(
    title="Self-Programming AI",
    description="ذكاء اصطناعي قادر على البرمجة والتعلم الذاتي",
    version="0.1.0",
    lifespan=lifespan
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Self-Programming AI API", 
        "status": "active",
        "platform": "Zeabur"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "version": "0.1.0",
        "platform": "Zeabur"
    }

@app.post("/generate")
async def generate_code(request: CodeRequest):
    try:
        # استيراد هنا لتجنب مشاكل التبعية
        from app.models import CodeRequest
        from app.ai_core import AICore
        
        code = await ai_core.generate_code(
            task=request.task,
            language=request.language,
            context=request.context
        )
        return {"code": code, "status": "success"}
    except Exception as e:
        logger.error(f"Error generating code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learn")
async def learn(request: LearnRequest):
    try:
        # استيراد هنا لتجنب مشاكل التبعية
        from app.models import LearnRequest
        
        result = await ai_core.learn_topic(
            topic=request.topic,
            sources=request.sources,
            depth=request.depth
        )
        return {"result": result, "status": "success"}
    except Exception as e:
        logger.error(f"Error learning topic: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/improve")
async def improve(request: ImproveRequest):
    try:
        # استيراد هنا لتجنب مشاكل التبعية
        from app.models import ImproveRequest
        
        result = await ai_core.improve_code(
            code=request.code,
            language=request.language,
            suggestions=request.suggestions
        )
        return {"improved_code": result, "status": "success"}
    except Exception as e:
        logger.error(f"Error improving code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/{topic}")
async def get_knowledge(topic: str):
    try:
        knowledge = knowledge_manager.get_knowledge(topic)
        return {"topic": topic, "knowledge": knowledge, "status": "success"}
    except Exception as e:
        logger.error(f"Error getting knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# نقطة الدخول الرئيسية للتشغيل على Zeabur
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)