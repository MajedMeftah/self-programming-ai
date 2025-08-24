from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class ProgrammingLanguage(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"

class LearningDepth(str, Enum):
    """Learning depth levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class CodeGenerationRequest(BaseModel):
    """Request model for code generation"""
    task: str = Field(..., description="Description of the coding task", min_length=5, max_length=1000)
    language: ProgrammingLanguage = Field(default=ProgrammingLanguage.PYTHON, description="Target programming language")
    context: Optional[str] = Field(None, description="Additional context or requirements", max_length=2000)
    include_tests: bool = Field(default=False, description="Whether to include unit tests")
    include_docs: bool = Field(default=True, description="Whether to include documentation")

class CodeGenerationResponse(BaseModel):
    """Response model for code generation"""
    code: str = Field(..., description="Generated code")
    language: str = Field(..., description="Programming language used")
    explanation: Optional[str] = Field(None, description="Explanation of the generated code")
    suggestions: List[str] = Field(default=[], description="Additional suggestions or improvements")
    execution_time: float = Field(..., description="Time taken to generate code in seconds")

class LearningRequest(BaseModel):
    """Request model for learning new topics"""
    topic: str = Field(..., description="Topic to learn about", min_length=2, max_length=200)
    sources: Optional[List[str]] = Field(None, description="Specific sources to learn from (URLs)")
    depth: LearningDepth = Field(default=LearningDepth.INTERMEDIATE, description="Learning depth level")
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to focus on")

class LearningResponse(BaseModel):
    """Response model for learning"""
    topic: str = Field(..., description="Topic that was learned")
    knowledge_acquired: Dict[str, Any] = Field(..., description="Knowledge that was acquired")
    sources_used: List[str] = Field(..., description="Sources that were used for learning")
    key_concepts: List[str] = Field(default=[], description="Key concepts learned")
    related_topics: List[str] = Field(default=[], description="Related topics for further learning")
    confidence_score: float = Field(..., description="Confidence score of the learned knowledge (0-1)")

class CodeImprovementRequest(BaseModel):
    """Request model for code improvement"""
    code: str = Field(..., description="Code to be improved", min_length=10)
    language: ProgrammingLanguage = Field(..., description="Programming language of the code")
    improvement_goals: Optional[List[str]] = Field(None, description="Specific improvement goals")
    focus_on: Optional[List[str]] = Field(None, description="Areas to focus on (performance, readability, security, etc.)")

class CodeImprovementResponse(BaseModel):
    """Response model for code improvement"""
    original_code: str = Field(..., description="Original code")
    improved_code: str = Field(..., description="Improved code")
    improvements_made: List[str] = Field(..., description="List of improvements made")
    performance_impact: Optional[str] = Field(None, description="Expected performance impact")
    quality_score_before: float = Field(..., description="Quality score before improvement (0-10)")
    quality_score_after: float = Field(..., description="Quality score after improvement (0-10)")

class KnowledgeQuery(BaseModel):
    """Request model for knowledge queries"""
    topic: str = Field(..., description="Topic to query knowledge about", min_length=2, max_length=200)
    include_examples: bool = Field(default=True, description="Whether to include code examples")
    include_related: bool = Field(default=True, description="Whether to include related topics")

class KnowledgeResponse(BaseModel):
    """Response model for knowledge queries"""
    topic: str = Field(..., description="Queried topic")
    knowledge: Dict[str, Any] = Field(..., description="Knowledge about the topic")
    examples: List[str] = Field(default=[], description="Code examples related to the topic")
    related_topics: List[str] = Field(default=[], description="Related topics")
    sources: List[str] = Field(default=[], description="Sources of the knowledge")
    last_updated: Optional[str] = Field(None, description="When the knowledge was last updated")

class ResearchRequest(BaseModel):
    """Request model for web research"""
    query: str = Field(..., description="Research query", min_length=3, max_length=500)
    max_results: int = Field(default=5, description="Maximum number of results to return", ge=1, le=20)
    include_content: bool = Field(default=True, description="Whether to extract content from found URLs")
    focus_on: Optional[List[str]] = Field(None, description="Specific aspects to focus on")

class ResearchResponse(BaseModel):
    """Response model for web research"""
    query: str = Field(..., description="Original research query")
    results: List[Dict[str, Any]] = Field(..., description="Research results")
    summary: Optional[str] = Field(None, description="Summary of findings")
    key_insights: List[str] = Field(default=[], description="Key insights from the research")
    sources_count: int = Field(..., description="Number of sources researched")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="System status")
    version: str = Field(..., description="API version")
    platform: str = Field(..., description="Deployment platform")
    uptime: Optional[float] = Field(None, description="System uptime in seconds")
    memory_usage: Optional[Dict[str, Any]] = Field(None, description="Memory usage statistics")
    active_connections: Optional[int] = Field(None, description="Number of active connections")

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

class APIStats(BaseModel):
    """API usage statistics"""
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")
    average_response_time: float = Field(..., description="Average response time in seconds")
    most_used_endpoints: List[Dict[str, Any]] = Field(..., description="Most frequently used endpoints")
    active_users: int = Field(..., description="Number of active users")

class SelfReflectionResponse(BaseModel):
    """Response model for AI self-reflection"""
    knowledge_stats: Dict[str, Any] = Field(..., description="Knowledge base statistics")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    improvement_suggestions: List[str] = Field(..., description="Self-improvement suggestions")
    learning_progress: Dict[str, Any] = Field(..., description="Learning progress indicators")
    system_health: Dict[str, Any] = Field(..., description="System health indicators")
