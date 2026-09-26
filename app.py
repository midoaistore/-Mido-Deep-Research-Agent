import streamlit as st
import os
from dotenv import load_dotenv
from langchain_nebius import ChatNebius
from deepagents import create_deep_agent
from prompts import RESEARCH_WORKFLOW_INSTRUCTIONS, SUBAGENT_DELEGATION_INSTRUCTIONS, RESEARCHER_INSTRUCTIONS, TASK_DESCRIPTION_PREFIX
from tools import tavily_search, think_tool

load_dotenv()

st.set_page_config(page_title="Mido Deep Research", page_icon="🔍", layout="wide")

st.title("🔍 Mido AI - وكيل الأبحاث العميقة")
st.caption("مدعوم من Nebius Token Factory + Tavily | Mido AI Store")

with st.sidebar:
    st.header("🔑 المفاتيح")
    st.markdown("جيب مفاتيحك المجانية:")
    st.code("NEBIUS_API_KEY\nTAVILY_API_KEY", language="bash")
    st.link_button("🎁 Nebius $25 مجانا", "https://tokenfactory.nebius.com")
    st.link_button("🔍 Tavily $25 بكود NEBIUS25", "https://tavily.com")

question = st.text_area("✍️ اكتب سؤالك البحثي هنا (عربي أو انجليزي):", height=120, placeholder="مثال: ايه افضل طرق بيع المنتجات الرقمية في مصر 2026؟")

if st.button("🚀 ابدأ البحث العميق", type="primary", use_container_width=True):
    if not question:
        st.warning("اكتب سؤال الأول!")
    else:
        if not os.getenv("NEBIUS_API_KEY") or not os.getenv("TAVILY_API_KEY"):
            st.error("حط المفاتيح في ملف .env الأول!")
            st.code("NEBIUS_API_KEY=...\nTAVILY_API_KEY=...", language="bash")
        else:
            with st.spinner("🤖 الميدو بيبحث في جوجل... بيخطط وبيفكر..."):
                try:
                    model = ChatNebius(model="MiniMaxAI/MiniMax-M3", api_key=os.getenv("NEBIUS_API_KEY"))
                    
                    agent = create_deep_agent(
                        model=model,
                        tools=[tavily_search, think_tool],
                        system_prompt=RESEARCH_WORKFLOW_INSTRUCTIONS
                    )
                    
                    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
                    
                    st.success("✅ التقرير جاهز!")
                    final = result.get("final_report", "التقرير اتعمل في /final_report.md")
                    st.markdown(final)
                    
                    st.download_button("📥 حمل التقرير", final, file_name="Mido_Report.md")
                except Exception as e:
                    st.error(f"حصل خطأ: {e}")

st.divider()
st.markdown("Made with ❤️ by **Mido AI Store** | midoaistore@gmail.com | 01221804050")
