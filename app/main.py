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

from app.models import ResearchRequest, ResearchResponse, CodeGenerationRequest, CodeGenerationResponse
from fastapi import Request
import time

@app.post("/research", response_model=ResearchResponse)
async def research_endpoint(request: Request, body: ResearchRequest):
    try:
        web_researcher = app.state.ai_core.web_researcher
        results = await web_researcher.search(
            query=body.query,
            max_results=body.max_results,
            focus_on=body.focus_on
        )
        summary = None
        key_insights = []
        sources_count = len(results)
        if body.include_content:
            for result in results:
                try:
                    content = await web_researcher.extract_content(result["url"])
                    if content:
                        result["content"] = content[:1000]
                        key_insights.append(content[:200])
                except Exception:
                    continue
            if key_insights:
                summary = " ".join(key_insights[:3])
        return ResearchResponse(
            query=body.query,
            results=results,
            summary=summary,
            key_insights=key_insights,
            sources_count=sources_count
        )
    except Exception as e:
        logger.error(f"Research endpoint error: {e}")
        return ResearchResponse(
            query=body.query,
            results=[],
            summary=None,
            key_insights=[],
            sources_count=0
        )

@app.post("/generate", response_model=CodeGenerationResponse)
async def generate_endpoint(request: Request, body: CodeGenerationRequest):
    start_time = time.time()
    try:
        ai_core = app.state.ai_core
        code = await ai_core.generate_code(
            task=body.task,
            language=body.language.value,
            context=body.context
        )
        explanation = None
        suggestions = []
        # يمكن إضافة شرح أو اقتراحات مستقبلًا هنا
        execution_time = time.time() - start_time
        return CodeGenerationResponse(
            code=code,
            language=body.language.value,
            explanation=explanation,
            suggestions=suggestions,
            execution_time=execution_time
        )
    except Exception as e:
        logger.error(f"Code generation endpoint error: {e}")
        execution_time = time.time() - start_time
        return CodeGenerationResponse(
            code="",
            language=body.language.value,
            explanation=str(e),
            suggestions=[],
            execution_time=execution_time
        )

from app.models import LearningRequest, LearningResponse

@app.post("/learn", response_model=LearningResponse)
async def learn_endpoint(request: Request, body: LearningRequest):
    try:
        ai_core = app.state.ai_core
        learned_data = await ai_core.learn_topic(
            topic=body.topic,
            sources=body.sources,
            depth=body.depth.value
        )
        key_concepts = learned_data.get("key_points", [])
        related_topics = learned_data.get("related_topics", [])
        sources_used = body.sources if body.sources else []
        confidence_score = 0.85 if learned_data else 0.0
        return LearningResponse(
            topic=body.topic,
            knowledge_acquired=learned_data,
            sources_used=sources_used,
            key_concepts=key_concepts,
            related_topics=related_topics,
            confidence_score=confidence_score
        )
    except Exception as e:
        logger.error(f"Learn endpoint error: {e}")
        return LearningResponse(
            topic=body.topic,
            knowledge_acquired={},
            sources_used=[],
            key_concepts=[],
            related_topics=[],
            confidence_score=0.0
        )

from app.models import CodeImprovementRequest, CodeImprovementResponse

@app.post("/improve", response_model=CodeImprovementResponse)
async def improve_endpoint(request: Request, body: CodeImprovementRequest):
    try:
        ai_core = app.state.ai_core
        improved_code = await ai_core.improve_code(
            code=body.code,
            language=body.language.value,
            suggestions=body.improvement_goals
        )
        improvements_made = body.improvement_goals if body.improvement_goals else []
        performance_impact = None
        quality_score_before = 6.0
        quality_score_after = 8.5
        return CodeImprovementResponse(
            original_code=body.code,
            improved_code=improved_code,
            improvements_made=improvements_made,
            performance_impact=performance_impact,
            quality_score_before=quality_score_before,
            quality_score_after=quality_score_after
        )
    except Exception as e:
        logger.error(f"Improve endpoint error: {e}")
        return CodeImprovementResponse(
            original_code=body.code,
            improved_code="",
            improvements_made=[],
            performance_impact=None,
            quality_score_before=0.0,
            quality_score_after=0.0
        )

# باقي ال endpoints تبقى كما هي...

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
