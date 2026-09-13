import os
import sys
import streamlit as st
import pandas as pd
from pathlib import Path

from modules.pdf_analyzer import analyze_pdf, extract_pdf_text
from modules.text_analyzer import analyze_text
from modules.data_analyzer import analyze_dataframe
from modules.report_generator import build_text_report
from modules.ats_analyzer import analyze_resume
from recommendation_engine import document_recommendations, ats_recommendations

st.set_page_config(
    page_title="InsightSphere AI",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {
    background: #f7f9fc;
    border: 1px solid #e6eaf0;
    padding: 16px;
    border-radius: 16px;
}
.hero {
    padding: 24px 26px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #1f2937);
    color: white;
    margin-bottom: 18px;
}
.hero h1 {margin:0; font-size: 2.1rem;}
.hero p {margin:8px 0 0 0; opacity:.86;}
.card {
    background: #ffffff;
    padding: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    margin-bottom: 12px;
}
.small-muted {color:#6b7280; font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🧠 InsightSphere AI</h1>
  <p>Document Intelligence • Data Analytics • ATS Resume Scoring • Recommendation System</p>
</div>
""", unsafe_allow_html=True)

module = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📄 Document Analyzer", "📊 Data Dashboard", "🧾 ATS Resume Analyzer"]
)

with st.sidebar:
    st.markdown("---")
    st.caption("Unified final-year analytics project")
    st.caption("Python • Streamlit • NLP • Data Analytics • ATS")

if module == "🏠 Home":
    st.subheader("Unified Intelligence Dashboard")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
        <h3>📄 Document Intelligence</h3>
        <p>Analyze PDFs/TXT, summarize content, extract important points and keywords.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
        <h3>📊 Data Analytics</h3>
        <p>Analyze CSV/Excel files using quality checks, distributions, correlation and trends.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
        <h3>🧾 ATS + Recommendations</h3>
        <p>Score resumes, compare with job descriptions and recommend improvements.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### System Workflow")
    st.code("""
Upload PDF / TXT / CSV / Excel / Resume
                ↓
        Content Extraction
                ↓
        Intelligent Analysis
        ↙       ↓        ↘
  Summary    Dashboard    ATS
      ↓          ↓         ↓
Important    Graphs      Match
 Points      Trends      Score
        ↘       ↓       ↙
       Recommendation Engine
                ↓
          Final Insights
    """, language="text")

elif module == "📄 Document Analyzer":
    st.subheader("📄 Document Intelligence")
    left, right = st.columns([1, 1])

    with left:
        uploaded = st.file_uploader(
            "Upload PDF or TXT",
            type=["pdf", "txt"],
            key="doc_file"
        )
    with right:
        summary_sentences = st.slider("Summary sentences", 3, 15, 7)
        top_keywords = st.slider("Top keywords", 5, 30, 15)

    if uploaded:
        suffix = Path(uploaded.name).suffix.lower()

        if suffix == ".pdf":
            result = analyze_pdf(uploaded, summary_sentences, top_keywords)
        else:
            text = uploaded.read().decode("utf-8", errors="ignore")
            result = analyze_text(text, summary_sentences, top_keywords)
            result["pages"] = 1

        a, b, c, d = st.columns(4)
        a.metric("Pages", result["pages"])
        b.metric("Words", result["word_count"])
        c.metric("Sentences", result["sentence_count"])
        d.metric("Characters", result["character_count"])

        tabs = st.tabs([
            "📝 Summary",
            "⭐ Important Points",
            "📊 Graph Dashboard",
            "🔑 Keywords",
            "💡 Recommendations",
            "📃 Full Text"
        ])

        with tabs[0]:
            st.subheader("Executive Summary")
            st.write(result["summary"])

        with tabs[1]:
            for i, point in enumerate(result["important_points"], 1):
                st.markdown(f"**{i}.** {point}")

        with tabs[2]:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Keyword Importance")
                kw_df = pd.DataFrame(result["keywords"], columns=["Keyword", "Score"])
                if not kw_df.empty:
                    st.bar_chart(kw_df.head(12).set_index("Keyword")["Score"])

            with col2:
                st.markdown("#### Sentence Length Trend")
                sent = pd.DataFrame({
                    "Sentence": [f"S{i+1}" for i in range(len(result["sentence_lengths"]))],
                    "Words": result["sentence_lengths"]
                })
                if not sent.empty:
                    st.line_chart(sent.set_index("Sentence")["Words"])

            st.markdown("#### Document Composition")
            comp = pd.DataFrame({
                "Metric": ["Words", "Sentences", "Important Points", "Keywords"],
                "Value": [
                    result["word_count"],
                    result["sentence_count"],
                    len(result["important_points"]),
                    len(result["keywords"])
                ]
            })
            st.bar_chart(comp.set_index("Metric")["Value"])

        with tabs[3]:
            kw_df = pd.DataFrame(result["keywords"], columns=["Keyword", "Score"])
            st.dataframe(kw_df, use_container_width=True, hide_index=True)

        with tabs[4]:
            st.subheader("Recommended Next Actions")
            for i, rec in enumerate(document_recommendations(result), 1):
                st.markdown(f"**{i}.** {rec}")

        with tabs[5]:
            st.text_area("Extracted text", result["text"], height=500)

        report = build_text_report(
            filename=uploaded.name,
            summary=result["summary"],
            important_points=result["important_points"],
            keywords=[k for k, _ in result["keywords"]],
            stats={
                "Pages": result["pages"],
                "Words": result["word_count"],
                "Sentences": result["sentence_count"],
                "Characters": result["character_count"]
            }
        )

        st.download_button(
            "⬇️ Download Document Report",
            report,
            file_name=f"{Path(uploaded.name).stem}_report.txt",
            mime="text/plain"
        )

elif module == "📊 Data Dashboard":
    st.subheader("📊 Interactive Data Dashboard")
    uploaded = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
        key="dataset_file"
    )

    if uploaded:
        suffix = Path(uploaded.name).suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        analyze_dataframe(df, uploaded.name)

elif module == "🧾 ATS Resume Analyzer":
    st.subheader("🧾 ATS Resume Intelligence")

    col1, col2 = st.columns([1, 1])
    with col1:
        resume_file = st.file_uploader(
            "Upload resume",
            type=["pdf", "txt"],
            key="ats_file"
        )
    with col2:
        job_description = st.text_area(
            "Target job description",
            height=180,
            placeholder="Paste the job description here for role-specific ATS analysis..."
        )

    if resume_file:
        suffix = Path(resume_file.name).suffix.lower()
        if suffix == ".pdf":
            resume_text, pages = extract_pdf_text(resume_file)
        else:
            resume_text = resume_file.read().decode("utf-8", errors="ignore")
            pages = 1

        ats = analyze_resume(resume_text, job_description)
        score = ats["ats_score"]

        a, b, c, d = st.columns(4)
        a.metric("ATS Score", f"{score}/100")
        b.metric("Format", f"{ats['format_score']}/100")
        c.metric("Sections", f"{ats['section_score']}/100")
        d.metric("Skills Found", len(ats["skills"]))

        tabs = st.tabs([
            "📊 ATS Dashboard",
            "✅ Matched Skills",
            "❌ Missing Skills",
            "🧩 Resume Sections",
            "💡 Recommendations",
            "📃 Extracted Resume"
        ])

        with tabs[0]:
            chart = pd.DataFrame({
                "Metric": ["ATS", "Formatting", "Sections", "Contact"],
                "Score": [
                    ats["ats_score"],
                    ats["format_score"],
                    ats["section_score"],
                    ats["contact_score"]
                ]
            })
            st.bar_chart(chart.set_index("Metric")["Score"])

            if job_description.strip():
                st.markdown("#### Job Match Dashboard")
                jd_chart = pd.DataFrame({
                    "Metric": ["Skill Match", "Keyword Match"],
                    "Score": [
                        ats.get("skill_match_score", 0),
                        ats.get("keyword_match_score", 0)
                    ]
                })
                st.bar_chart(jd_chart.set_index("Metric")["Score"])

            st.markdown("#### Resume Profile")
            r1, r2, r3 = st.columns(3)
            r1.metric("Words", ats["word_count"])
            r2.metric("Pages", pages)
            r3.metric("Links", len(ats["links"]))

        with tabs[1]:
            matched = ats.get("matched_skills", ats["skills"])
            if matched:
                st.dataframe(
                    pd.DataFrame({"Matched Skill": matched}),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No matched skills detected.")

        with tabs[2]:
            missing = ats.get("missing_skills", [])
            if missing:
                st.dataframe(
                    pd.DataFrame({"Missing Skill": missing}),
                    use_container_width=True,
                    hide_index=True
                )
            elif job_description.strip():
                st.success("No major missing skills detected.")
            else:
                st.info("Paste a job description to identify missing skills.")

        with tabs[3]:
            section_df = pd.DataFrame({
                "Section": [x.title() for x in ats["sections"]],
                "Detected": ["Yes" if x else "No" for x in ats["sections"].values()]
            })
            st.dataframe(section_df, use_container_width=True, hide_index=True)

        with tabs[4]:
            st.subheader("Personalized Resume Recommendations")
            for i, rec in enumerate(ats_recommendations(ats), 1):
                st.markdown(f"**{i}.** {rec}")

            if job_description.strip():
                st.info(
                    "Only add missing keywords or skills if they truthfully reflect your experience."
                )

        with tabs[5]:
            st.text_area("Resume text", resume_text, height=500)

        report = [
            "ATS RESUME INTELLIGENCE REPORT",
            "=" * 50,
            f"ATS Score: {ats['ats_score']}/100",
            f"Format Score: {ats['format_score']}/100",
            f"Section Score: {ats['section_score']}/100",
            "",
            "SKILLS",
            ", ".join(ats["skills"]),
            "",
            "RECOMMENDATIONS",
        ]
        for i, rec in enumerate(ats_recommendations(ats), 1):
            report.append(f"{i}. {rec}")

        st.download_button(
            "⬇️ Download ATS Report",
            "\n".join(report),
            file_name=f"{Path(resume_file.name).stem}_ATS_report.txt",
            mime="text/plain"
        )
