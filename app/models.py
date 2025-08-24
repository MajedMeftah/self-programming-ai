from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class CodeRequest(BaseModel):
    task: str = Field(..., description="المهمة المطلوبة برمجتها")
    language: str = Field(default="python", description="لغة البرمجة المطلوبة")
    context: Optional[str] = Field(default=None, description="سياق أو متطلبات إضافية")

class LearnRequest(BaseModel):
    topic: str = Field(..., description="الموضوع المراد تعلمه")
    sources: Optional[List[str]] = Field(default=None, description="مصادر خارجية للتعلم")
    depth: str = Field(default="intermediate", description="عمق التعلم (basic, intermediate, advanced)")

class ImproveRequest(BaseModel):
    code: str = Field(..., description="الكود المراد تحسينه")
    language: str = Field(..., description="لغة البرمجة")
    suggestions: Optional[List[str]] = Field(default=None, description="اقتراحات محددة للتحسين")

class SearchRequest(BaseModel):
    query: str = Field(..., description="استعلام البحث")
    max_results: int = Field(default=5, description="الحد الأقصى لنتائج البحث")

class KnowledgeItem(BaseModel):
    topic: str
    content: Dict[str, Any]
    sources: List[str]
    confidence: float
    last_updated: str