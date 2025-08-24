import os
import logging
from typing import Dict, List, Any, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, knowledge_manager):
        self.knowledge_manager = knowledge_manager
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        else:
            logger.warning("OPENAI_API_KEY not found, using fallback code generation")
    
    async def initialize(self):
        """تهيئة مولّد الأكواد"""
        logger.info("Code Generator initialized")
    
    async def generate(self, task: str, language: str = "python", 
                      context: Optional[str] = None, knowledge: List[Dict] = None) -> str:
        """توليد كود بناء على المهمة والمعرفة"""
        try:
            if self.openai_api_key:
                return await self._generate_with_ai(task, language, context, knowledge)
            else:
                return await self._generate_fallback(task, language, context)
        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return await self._generate_fallback(task, language, context)
    
    async def _generate_with_ai(self, task: str, language: str, 
                               context: Optional[str], knowledge: List[Dict]) -> str:
        """توليد الكود باستخدام الذكاء الاصطناعي"""
        # بناء الرسالة (prompt)
        messages = self._build_messages(task, language, context, knowledge)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            code = response.choices[0].message.content.strip()
            return self._clean_code(code, language)
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return await self._generate_fallback(task, language, context)
    
    def _build_messages(self, task: str, language: str, 
                       context: Optional[str], knowledge: List[Dict]) -> List[Dict]:
        """بناء رسائل المحادثة للذكاء الاصطناعي"""
        system_message = {
            "role": "system",
            "content": f"""أنت مساعد ذكاء اصطناعي خبير في البرمجة. مهمتك هي كتابة كود {language} عالي الجودة.
يجب أن يكون الكود:
- صحيحًا ومنطقيًا
- متبعًا لأفضل الممارسات
- واضحًا وسهل القراءة
- شاملًا للتعليقات التوضيحية عند الحاجة
- متضمنًا لمعالجة الأخطاء عندما يكون ذلك مناسبًا"""
        }
        
        user_content = f"المهمة: {task}\n\n"
        
        if context:
            user_content += f"السياق: {context}\n\n"
            
        if knowledge:
            user_content += "المعرفة ذات الصلة:\n"
            for i, item in enumerate(knowledge, 1):
                user_content += f"{i}. {item.get('content', '')[:200]}...\n"
        
        user_message = {"role": "user", "content": user_content}
        
        return [system_message, user_message]
    
    async def _generate_fallback(self, task: str, language: str, context: Optional[str]) -> str:
        """توليد كود بديل عند عدم توفر API"""
        if language == "python":
            code = f'''# كود لـ: {task}
def main():
    print("Hello from generated code!")
    # TODO: Implement the actual functionality
    pass

if __name__ == "__main__":
    main()'''
        else:
            code = f"// كود لـ: {task}\n// TODO: Implement the actual functionality"
        
        if context:
            code = f"# السياق: {context}\n\n{code}"
            
        return code
    
    def _clean_code(self, code: str, language: str) -> str:
        """تنظيف الكود المُولَّد"""
        # إزالة markdown code blocks إذا وجدت
        if code.startswith("```"):
            lines = code.split('\n')
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            code = '\n'.join(lines)
        
        return code