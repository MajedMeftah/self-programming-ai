import aiohttp
import asyncio
import logging
import json
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin
import re
from datetime import datetime

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class WebResearcher:
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.search_engines = {
            "duckduckgo": "https://api.duckduckgo.com/",
            "bing": "https://api.bing.microsoft.com/v7.0/search",
            "google": "https://www.googleapis.com/customsearch/v1"
        }
        self.rate_limit_delay = 1.0  # seconds between requests
        self.last_request_time = 0
        
    async def initialize(self):
        """تهيئة باحث الويب"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        logger.info("Web Researcher initialized successfully")
        
    async def search(self, query: str, max_results: int = 5, focus_on: Optional[List[str]] = None) -> List[Dict]:
        """البحث على الإنترنت مع إمكانيات محسنة"""
        await self._rate_limit()
        
        try:
            # محاولة استخدام DuckDuckGo API أولاً
            results = await self._search_duckduckgo(query, max_results)
            
            if not results:
                # العودة إلى البحث المحاكي إذا فشل API
                results = await self._fallback_search(query, max_results)
            
            # تحسين النتائج بناء على التركيز المطلوب
            if focus_on:
                results = await self._filter_results_by_focus(results, focus_on)
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return await self._fallback_search(query, max_results)

    async def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict]:
        """البحث باستخدام DuckDuckGo API"""
        try:
            if not self.session:
                await self.initialize()
                
            # DuckDuckGo Instant Answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            async with self.session.get(self.search_engines["duckduckgo"], params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    # استخراج النتائج من الاستجابة
                    if 'RelatedTopics' in data:
                        for topic in data['RelatedTopics'][:max_results]:
                            if isinstance(topic, dict) and 'Text' in topic:
                                results.append({
                                    'title': topic.get('Text', '')[:100] + '...',
                                    'url': topic.get('FirstURL', ''),
                                    'snippet': topic.get('Text', ''),
                                    'source': 'DuckDuckGo'
                                })
                    
                    return results
                    
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []

    async def _fallback_search(self, query: str, max_results: int) -> List[Dict]:
        """البحث الاحتياطي عند فشل APIs الخارجية"""
        # قائمة مواقع مفيدة للبحث البرمجي
        programming_sites = [
            "https://stackoverflow.com/search?q=",
            "https://github.com/search?q=",
            "https://docs.python.org/3/search.html?q=",
            "https://developer.mozilla.org/en-US/search?q=",
            "https://www.w3schools.com/search/search_asp.asp?search="
        ]
        
        results = []
        for i, site in enumerate(programming_sites[:max_results]):
            results.append({
                'title': f"Search results for '{query}' - {site.split('//')[1].split('/')[0]}",
                'url': f"{site}{query.replace(' ', '+')}",
                'snippet': f"Search results for '{query}' on {site.split('//')[1].split('/')[0]}. This is a fallback search result.",
                'source': 'Fallback',
                'relevance_score': 0.7 - (i * 0.1)
            })
        
        return results

    async def _filter_results_by_focus(self, results: List[Dict], focus_areas: List[str]) -> List[Dict]:
        """تصفية النتائج بناء على مجالات التركيز"""
        filtered_results = []
        
        for result in results:
            relevance_score = 0
            text_to_check = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
            
            for focus_area in focus_areas:
                if focus_area.lower() in text_to_check:
                    relevance_score += 1
            
            if relevance_score > 0:
                result['relevance_score'] = relevance_score / len(focus_areas)
                filtered_results.append(result)
        
        # ترتيب النتائج حسب الصلة
        filtered_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return filtered_results

    async def _rate_limit(self):
        """تطبيق حد معدل الطلبات"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    async def extract_content(self, url: str) -> str:
        """استخراج المحتوى من URL"""
        if not self.session:
            await self.initialize()
            
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    
                    # إزالة العناصر غير المرغوب فيها
                    for element in soup(["script", "style", "nav", "footer", "header"]):
                        element.decompose()
                    
                    # استخراج النص الرئيسي
                    text = soup.get_text()
                    
                    # تنظيف النص
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    return text
                else:
                    logger.error(f"Failed to fetch URL: {url}, Status: {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {e}")
            return ""
    
    async def close(self):
        """إغلاق الجلسة"""
        if self.session:
            await self.session.close()
            logger.info("Web Researcher session closed")
