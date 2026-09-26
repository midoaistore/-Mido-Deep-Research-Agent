from langchain_core.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def tavily_search(query: str, max_results: int = 5) -> str:
    """
    بحث حقيقي في الويب باستخدام Tavily.
    استخدمه للبحث عن أي معلومة حديثة.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "خطأ: TAVILY_API_KEY مش موجود في .env"
    
    try:
        client = TavilyClient(api_key=api_key)
        result = client.search(
            query, 
            max_results=max_results, 
            include_answer=True, 
            search_depth="advanced",
            include_images=False
        )
        
        formatted = []
        for i, r in enumerate(result.get('results', []), 1):
            title = r.get('title', 'بدون عنوان')
            content = r.get('content', '')[:700]
            url = r.get('url', '')
            formatted.append(f"[{i}] {title}\n{content}\nالمصدر: {url}\n")
        
        if result.get('answer'):
            formatted.insert(0, f"ملخص سريع: {result.get('answer')}\n")
            
        return "\n---\n".join(formatted) if formatted else "مفيش نتائج"
    except Exception as e:
        return f"خطأ في البحث: {str(e)}"

@tool
def think_tool(thought: str) -> str:
    """
    أداة للتفكير العميق قبل الخطوة التالية.
    استخدمها بعد كل بحث.
    """
    return f"🧠 تفكير: {thought}\n"
