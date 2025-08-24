import logging
from typing import Dict, List, Any, Optional
import ast
import inspect

logger = logging.getLogger(__name__)

class SelfImprover:
    def __init__(self, knowledge_manager):
        self.knowledge_manager = knowledge_manager
        
    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """تحليل الكود لتحديد مجالات التحسين"""
        analysis = {
            "complexity": 0,
            "readability": 0,
            "efficiency": 0,
            "best_practices": 0,
            "issues": [],
            "suggestions": []
        }
        
        try:
            if language == "python":
                return await self._analyze_python_code(code, analysis)
            else:
                return await self._analyze_general_code(code, language, analysis)
        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            analysis["issues"].append(f"فشل التحليل: {e}")
            return analysis
    
    async def _analyze_python_code(self, code: str, analysis: Dict) -> Dict:
        """تحليل كود Python"""
        try:
            # تحليل الشجرة المجردة للكود
            tree = ast.parse(code)
            
            # حساب التعقيد (عدد الوظائف والفئات)
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            
            analysis["complexity"] = len(functions) + len(classes)
            
            # التحقق من أفضل الممارسات
            has_docstrings = any(ast.get_docstring(node) for node in functions + classes)
            if not has_docstrings:
                analysis["issues"].append("الكود يفتقد إلى التوثيق (docstrings)")
                analysis["suggestions"].append("إضافة docstrings للوظائف والفئات الرئيسية")
            
            # التحقق من معالجة الأخطاء
            has_error_handling = any(
                isinstance(node, ast.Try) for node in ast.walk(tree)
            )
            if not has_error_handling:
                analysis["suggestions"].append("إضافة معالجة للأخطاء باستخدام try-except")
                
        except SyntaxError as e:
            analysis["issues"].append(f"أخطاء syntax: {e}")
            
        return analysis
    
    async def _analyze_general_code(self, code: str, language: str, analysis: Dict) -> Dict:
        """تحليل كود بلغات أخرى"""
        # تحليل أساسي للكود
        lines = code.split('\n')
        analysis["complexity"] = len(lines)
        
        # التحقق من التعليقات
        comment_lines = [line for line in lines if line.strip().startswith(('//', '#', '/*', '*'))]
        comment_ratio = len(comment_lines) / len(lines) if lines else 0
        
        if comment_ratio < 0.1:  # أقل من 10% تعليقات
            analysis["issues"].append("نسبة التعليقات منخفضة")
            analysis["suggestions"].append("إضافة المزيد من التعليقات التوضيحية")
            
        return analysis
    
    async def find_improvements(self, code: str, language: str, 
                               analysis: Dict, suggestions: Optional[List[str]] = None) -> List[str]:
        """البحث عن تحسينات للكود"""
        improvements = []
        
        # إضافة الاقتراحات من التحليل
        improvements.extend(analysis.get("suggestions", []))
        
        # إضافة الاقتراحات المقدمة من المستخدم
        if suggestions:
            improvements.extend(suggestions)
            
        # البحث عن تحسينات بناء على المعرفة
        knowledge_based = await self._find_knowledge_based_improvements(code, language)
        improvements.extend(knowledge_based)
        
        return list(set(improvements))  # إزالة التكرارات
    
    async def _find_knowledge_based_improvements(self, code: str, language: str) -> List[str]:
        """البحث عن تحسينات بناء على المعرفة المخزنة"""
        improvements = []
        
        # البحث عن معرفة ذات صلة
        relevant_knowledge = await self.knowledge_manager.find_relevant_knowledge(
            f"{language} code best practices improvements"
        )
        
        for knowledge in relevant_knowledge:
            content = knowledge.get("content", "")
            # استخراج نصائح التحسين من المعرفة
            if "تحسين" in content or "improve" in content.lower():
                improvements.append(content[:150] + "...")
                
        return improvements
    
    async def apply_improvements(self, code: str, language: str, improvements: List[str]) -> str:
        """تطبيق التحسينات على الكود"""
        improved_code = code
        
        for improvement in improvements:
            try:
                if language == "python":
                    improved_code = await self._apply_python_improvement(improved_code, improvement)
                else:
                    # تطبيق تحسينات عامة
                    if "تعليقات" in improvement or "comments" in improvement.lower():
                        improved_code = self._add_comments(improved_code, language)
            except Exception as e:
                logger.error(f"Failed to apply improvement '{improvement}': {e}")
                continue
                
        return improved_code
    
    async def _apply_python_improvement(self, code: str, improvement: str) -> str:
        """تطبيق تحسينات على كود Python"""
        # هذا تنفيذ أساسي، يحتاج إلى مزيد من التطوير
        if "docstrings" in improvement or "توثيق" in improvement:
            # محاولة إضافة docstrings أساسية
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
                        # إضافة docstring بسيط
                        indent = " " * 4
                        docstring = f'{indent}"""{node.name} function."""'
                        function_code = ast.get_source_segment(code, node)
                        if function_code:
                            first_line = function_code.split('\n')[0]
                            improved_function = f"{first_line}\n{docstring}\n{function_code[len(first_line):]}"
                            code = code.replace(function_code, improved_function)
            except:
                pass
                
        return code
    
    def _add_comments(self, code: str, language: str) -> str:
        """إضافة تعليقات إلى الكود"""
        lines = code.split('\n')
        commented_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not any(stripped.startswith(c) for c in ['//', '#', '/*', '*']):
                if i % 10 == 0:  # إضافة تعليق كل 10 أسطر تقريباً
                    if language == "python":
                        commented_lines.append(f"# Line {i+1}: {stripped[:30]}...")
                    elif language in ["javascript", "java", "c++"]:
                        commented_lines.append(f"// Line {i+1}: {stripped[:30]}...")
            commented_lines.append(line)
            
        return '\n'.join(commented_lines)
    
    async def self_reflect(self) -> Dict:
        """التفكير الذاتي وتحسين الأداء"""
        reflection = {
            "knowledge_topics": await self._get_knowledge_stats(),
            "code_generation_quality": await self._assess_code_quality(),
            "improvement_opportunities": await self._find_self_improvements()
        }
        
        return reflection
    
    async def _get_knowledge_stats(self) -> Dict:
        """الحصول على إحصائيات المعرفة"""
        # سيعود بإحصائيات أساسية (يتطلب تنفيذاً أكثر تطوراً)
        return {
            "total_topics": 10,  # سيتغير مع التطوير
            "coverage": "متوسطة",
            "update_required": False
        }
    
    async def _assess_code_quality(self) -> Dict:
        """تقييم جودة توليد الأكواد"""
        # سيعود بتقييم أساسي (يتطلب تنفيذاً أكثر تطوراً)
        return {
            "score": 7,
            "strengths": ["وضوح الكود", "التزام بالتنسيق"],
            "weaknesses": ["معالجة الأخطاء", "التوثيق"]
        }
    
    async def _find_self_improvements(self) -> List[str]:
        """البحث عن فرص تحسين الذات"""
        return [
            "تحسين دقة توليد الأكواد المعقدة",
            "زيادة معرفة أنماط التصميم",
            "تحسين كفاءة البحث على الإنترنت",
            "إضافة دعم للغات برمجة إضافية"
        ]