import os
import json
import pickle
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib
from datetime import datetime

import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class KnowledgeManager:
    def __init__(self, knowledge_path: Optional[str] = None):
        self.knowledge_path = Path(knowledge_path or os.getenv("KNOWLEDGE_PATH", "./knowledge_base"))
        self.knowledge_path.mkdir(exist_ok=True, parents=True)
        
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        
    async def initialize(self):
        """تهيئة مدير المعرفة"""
        try:
            # تحميل نموذج التضمين
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # تهيئة قاعدة بيانات المتجهات
            self.chroma_client = chromadb.Client(Settings(
                persist_directory=str(self.knowledge_path / "chroma_db"),
                chroma_db_impl="duckdb+parquet"
            ))
            
            # إنشاء أو تحميل المجموعة
            self.collection = self.chroma_client.get_or_create_collection("knowledge")
            
            logger.info("Knowledge Manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Knowledge Manager: {e}")
            raise

    async def load_base_knowledge(self):
        """تحميل المعرفة الأساسية للبرمجة"""
        base_topics = [
            "python_programming",
            "javascript_programming", 
            "algorithms",
            "data_structures",
            "software_design_patterns",
            "api_design",
            "database_design",
            "web_development",
            "machine_learning_basics"
        ]
        
        for topic in base_topics:
            base_path = self.knowledge_path / "base" / f"{topic}.json"
            if base_path.exists():
                try:
                    with open(base_path, 'r', encoding='utf-8') as f:
                        knowledge = json.load(f)
                    await self.save_knowledge(topic, knowledge, ["base_knowledge"])
                    logger.info(f"Loaded base knowledge: {topic}")
                except Exception as e:
                    logger.error(f"Failed to load base knowledge {topic}: {e}")

    async def process_content(self, topic: str, content: str, source: str) -> Dict[str, Any]:
        """معالجة المحتوى واستخلاص المعرفة"""
        # تقسيم المحتوى إلى أجزاء
        chunks = self._chunk_content(content)
        
        knowledge = {
            "topic": topic,
            "chunks": [],
            "key_points": [],
            "examples": [],
            "best_practices": [],
            "common_mistakes": [],
            "related_topics": [],
            "sources": [source],
            "processed_at": datetime.now().isoformat()
        }
        
        # معالجة كل جزء
        for chunk in chunks:
            # استخراج النقاط الرئيسية
            key_points = await self._extract_key_points(chunk)
            knowledge["key_points"].extend(key_points)
            
            # استخراج الأمثلة
            examples = await self._extract_examples(chunk, topic)
            if examples:
                knowledge["examples"].extend(examples)
                
            # تخزين المتجهات للبحث الدلالي
            embedding = self.embedding_model.encode(chunk).tolist()
            chunk_id = hashlib.md5(chunk.encode()).hexdigest()
            
            knowledge["chunks"].append({
                "id": chunk_id,
                "content": chunk,
                "embedding": embedding
            })
            
            # إضافة إلى قاعدة المتجهات
            if self.collection:
                self.collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{"topic": topic, "source": source}]
                )
        
        return knowledge

    async def save_knowledge(self, topic: str, knowledge: Dict[str, Any], sources: List[str]):
        """حفظ المعرفة"""
        try:
            # إنشاء مجلد للموضوع إذا لم يكن موجوداً
            topic_path = self.knowledge_path / "topics" / topic
            topic_path.mkdir(exist_ok=True, parents=True)
            
            # حفظ المعرفة بصيغة JSON
            knowledge_file = topic_path / "knowledge.json"
            with open(knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge, f, ensure_ascii=False, indent=2)
                
            # حفظ المصادر
            sources_file = topic_path / "sources.json"
            with open(sources_file, 'w', encoding='utf-8') as f:
                json.dump({"sources": sources}, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Knowledge saved for topic: {topic}")
        except Exception as e:
            logger.error(f"Failed to save knowledge for {topic}: {e}")

    async def find_relevant_knowledge(self, query: str, language: str = None) -> List[Dict]:
        """البحث عن معرفة ذات صلة"""
        if not self.collection:
            return []
            
        try:
            # تضمين الاستعلام
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # البحث في قاعدة المتجهات
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=5,
                include=["documents", "metadatas", "distances"]
            )
            
            relevant_knowledge = []
            for i, doc in enumerate(results["documents"][0]):
                relevant_knowledge.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i],
                    "similarity": 1 - results["distances"][0][i]  # تحويل المسافة إلى تشابه
                })
                
            return relevant_knowledge
        except Exception as e:
            logger.error(f"Failed to find relevant knowledge: {e}")
            return []

    def _chunk_content(self, content: str, chunk_size: int = 500) -> List[str]:
        """تقسيم المحتوى إلى أجزاء"""
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            
        return chunks

    async def _extract_key_points(self, content: str) -> List[str]:
        """استخراج النقاط الرئيسية من المحتوى"""
        # هذه وظيفة تحتاج إلى تنفيذ أكثر تطوراً
        # حالياً نعود بقائمة بسيطة
        return [content[:100] + "..."]

    async def _extract_examples(self, content: str, topic: str) -> List[str]:
        """استخراج الأمثلة البرمجية من المحتوى"""
        # هذه وظيفة تحتاج إلى تنفيذ أكثر تطوراً
        # حالياً نعود بقائمة فارغة
        return []

    async def close(self):
        """إغلاق الموارد"""
        if self.chroma_client:
            self.chroma_client.persist()