import os
import aiohttp
import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from app.knowledge_manager import KnowledgeManager
from app.web_research import WebResearcher
from app.code_generator import CodeGenerator
from app.self_improvement import SelfImprover

logger = logging.getLogger(__name__)

class AICore:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager()
        self.web_researcher = WebResearcher()
        self.code_generator = CodeGenerator(self.knowledge_manager)
        self.self_improver = SelfImprover(self.knowledge_manager)
        self.initialized = False
        self._init_done = False
        
    async def initialize(self):
        """تهيئة النواة الأساسية"""
        if self._init_done:
            return
            
        try:
            # تحميل المعرفة الأساسية
            await self.knowledge_manager.load_base_knowledge()
            
            # تهيئة باحث الويب
            await self.web_researcher.initialize()
            
            # تحميل نماذج توليد الأكواد
            await self.code_generator.initialize()
            
            self.initialized = True
            self._init_done = True
            logger.info("AI Core initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Core: {e}")
            raise

    async def generate_code(self, task: str, language: str = "python", context: Optional[str] = None) -> str:
        """توليد كود بناء على المهمة"""
        if not self.initialized:
            await self.initialize()
            
        # البحث عن معرفة ذات صلة
        relevant_knowledge = await self.knowledge_manager.find_relevant_knowledge(task, language)
        
        # توليد الكود
        code = await self.code_generator.generate(
            task=task, 
            language=language, 
            context=context,
            knowledge=relevant_knowledge
        )
        
        return code

    async def learn_topic(self, topic: str, sources: Optional[List[str]] = None, depth: str = "intermediate") -> Dict:
        """تعلم موضوع جديد"""
        if not self.initialized:
            await self.initialize()
            
        learned_data = {}
        
        # إذا لم يتم توفير مصادر، البحث على الإنترنت
        if not sources:
            search_results = await self.web_researcher.search(f"{topic} programming {depth}")
            sources = [result["url"] for result in search_results[:3]]
        
        # جمع المعلومات من المصادر
        for source in sources:
            try:
                content = await self.web_researcher.extract_content(source)
                processed = await self.knowledge_manager.process_content(topic, content, source)
                learned_data.update(processed)
            except Exception as e:
                logger.error(f"Failed to learn from {source}: {e}")
                continue
        
        # حفظ المعرفة المكتسبة
        await self.knowledge_manager.save_knowledge(topic, learned_data, sources)
        
        return learned_data

    async def improve_code(self, code: str, language: str, suggestions: Optional[List[str]] = None) -> str:
        """تحسين كود موجود"""
        if not self.initialized:
            await self.initialize()
            
        # تحليل الكود الحالي
        analysis = await self.self_improver.analyze_code(code, language)
        
        # البحث عن تحسينات
        improvements = await self.self_improver.find_improvements(
            code, language, analysis, suggestions
        )
        
        # تطبيق التحسينات
        improved_code = await self.self_improver.apply_improvements(
            code, language, improvements
        )
        
        return improved_code

    async def self_reflect(self) -> Dict:
        """التفكير الذاتي وتحسين الأداء"""
        if not self.initialized:
            await self.initialize()
            
        return await self.self_improver.self_reflect()

    async def close(self):
        """إغلاق الموارد"""
        await self.web_researcher.close()
        logger.info("AI Core resources released")