# 🧠 InsightSphere AI

## Intelligent Document, Data Analytics, ATS & Recommendation System

**InsightSphere AI** is an intelligent analytics platform designed to analyze documents, structured datasets, and resumes through a single interactive dashboard. The system extracts useful information, summarizes large documents, identifies important points and keywords, generates visual analytics, evaluates resumes using an ATS-style system, and provides personalized recommendations.

---

## 🎯 Project Objective

The main objective of InsightSphere AI is to reduce the time required to manually analyze large amounts of information. The system transforms raw documents and datasets into understandable summaries, important insights, graphs, dashboards, ATS scores, and actionable recommendations.

---

## ✨ Main Features

### 📄 Document Analyzer

The Document Analyzer processes PDF and TXT documents and automatically provides:

* Complete text extraction
* Automatic document summarization
* Important-point identification
* Keyword extraction using TF-IDF
* Word, sentence, page, and character statistics
* Keyword importance visualization
* Sentence-length analysis
* Document composition dashboard
* Personalized recommendations
* Downloadable analysis report

### 📊 Data Analytics Dashboard

The Data Dashboard supports CSV and Excel datasets and provides:

* Dataset overview
* Total rows and columns
* Data-type identification
* Missing-value detection
* Duplicate-row detection
* Descriptive statistics
* Numeric data analysis
* Categorical data analysis
* Distribution graphs
* Correlation analysis
* Time-series/trend analysis
* Automatic data insights
* Data-analysis recommendations
* Downloadable analyzed CSV

### 🧾 ATS Resume Analyzer

The ATS module evaluates resumes and compares them with job descriptions.

Features include:

* Resume PDF/TXT upload
* ATS compatibility score
* Resume formatting score
* Resume section detection
* Contact-information detection
* Technical skill extraction
* Job-description comparison
* Skill-match percentage
* Keyword-match percentage
* Matched skills
* Missing skills
* Missing job keywords
* Resume improvement recommendations
* ATS performance graphs
* Downloadable ATS report

> **Note:** The ATS score is an educational heuristic. Actual commercial ATS platforms use different proprietary parsing and ranking algorithms.

### 💡 Recommendation System

InsightSphere AI includes a rule-based recommendation engine that generates suggestions according to analysis results.

It provides:

* Document-analysis recommendations
* Dataset cleaning recommendations
* Data-exploration recommendations
* Resume improvement suggestions
* Missing-skill recommendations
* Job keyword recommendations
* Resume structure recommendations
* Suggested next analysis steps

---

## 🏗️ System Architecture

```text
                 User
                   │
                   ▼
              Upload File
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
    PDF/TXT    CSV/Excel     Resume
       │           │           │
       ▼           ▼           ▼
   Document       Data         ATS
   Processing   Processing   Processing
       │           │           │
       ▼           ▼           ▼
   Summary      Statistics    Resume
   Keywords     Cleaning      Parsing
   Key Points   Correlation   JD Matching
       │           │           │
       └───────────┼───────────┘
                   ▼
            Visualization
                   │
                   ▼
         Recommendation Engine
                   │
                   ▼
        Interactive Dashboard
                   │
                   ▼
             Final Report
```

---

## 🛠️ Technology Stack

| Technology        | Purpose                           |
| ----------------- | --------------------------------- |
| Python            | Core programming language         |
| Streamlit         | Web application and dashboard     |
| Pandas            | Dataset processing                |
| NumPy             | Numerical analysis                |
| Scikit-learn      | TF-IDF and text analytics         |
| PyPDF             | PDF text extraction               |
| OpenPyXL          | Excel file processing             |
| NLP               | Text processing and summarization |
| TF-IDF            | Keyword extraction                |
| Rule-Based Engine | Recommendation generation         |

---

## 📁 Project Structure

```text
pdf_data_intelligence_dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── sample_data.csv
│
└── modules/
    ├── __init__.py
    ├── pdf_analyzer.py
    ├── text_analyzer.py
    ├── data_analyzer.py
    ├── ats_analyzer.py
    ├── recommendation_engine.py
    └── report_generator.py
```

### Important Files

**app.py**
Main Streamlit application containing the user interface and navigation.

**pdf_analyzer.py**
Extracts and processes text from PDF documents.

**text_analyzer.py**
Performs text cleaning, summarization, important-point extraction, and keyword analysis.

**data_analyzer.py**
Performs CSV/Excel analysis and generates statistical dashboards.

**ats_analyzer.py**
Analyzes resumes, calculates ATS scores, extracts skills, and compares resumes with job descriptions.

**recommendation_engine.py**
Generates personalized recommendations from document, dataset, and ATS results.

**report_generator.py**
Creates downloadable analysis reports.

---

# 🚀 Installation and Execution

## 1. Install Python

Python **3.10, 3.11, or 3.12** is recommended.

Check Python:

```bash
python --version
```

---

## 2. Open the Project

Extract the project ZIP and open the project folder using **Visual Studio Code**.

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run the Application

```bash
streamlit run app.py
```

If Streamlit is not recognized:

```bash
python -m streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

# 🔄 Application Workflow

```text
Upload File
    ↓
Identify File Type
    ↓
Extract Content
    ↓
Clean & Preprocess
    ↓
Analyze Information
    ↓
Generate Summary / Statistics
    ↓
Extract Important Insights
    ↓
Create Graphs & Dashboard
    ↓
Generate Recommendations
    ↓
Display Results
    ↓
Download Report
```

---

# 📈 Dashboard Sections

## Document Dashboard

Displays:

* Document statistics
* Keyword importance
* Sentence-length trends
* Important points
* Document composition
* Recommendations

## Data Dashboard

Displays:

* Dataset statistics
* Missing values
* Numeric distributions
* Category distributions
* Correlations
* Trends
* Recommendations

## ATS Dashboard

Displays:

* Overall ATS score
* Formatting score
* Section score
* Contact-information score
* Skill-match percentage
* Keyword-match percentage
* Matched and missing skills
* Resume recommendations

---

# 🧮 ATS Scoring

When a job description is provided, the educational ATS score uses:

```text
Resume Structure & Formatting → 35%
Skill Matching                → 40%
JD Keyword Matching           → 25%
                              ─────
Overall ATS Score             → 100%
```

The recommendation system then identifies possible improvements based on the detected gaps.

---

# 📂 Supported Files

| Format | Purpose                    |
| ------ | -------------------------- |
| PDF    | Documents and resumes      |
| TXT    | Text documents and resumes |
| CSV    | Dataset analysis           |
| XLSX   | Excel dataset analysis     |
| XLS    | Excel dataset analysis     |

---

# 🔮 Future Enhancements

The system can be further enhanced by adding:

* OCR for scanned PDFs
* Transformer/LLM-based summarization
* Chat with uploaded PDF
* Question answering from documents
* Multiple-document comparison
* Named Entity Recognition
* Topic modeling
* Sentiment analysis
* AI-based recommendation engine
* Advanced resume parsing
* Job recommendations based on resume skills
* Resume ranking for recruiters
* Multiple-resume comparison
* User authentication
* Analysis history
* Database integration
* PDF report generation
* Cloud deployment
* REST API integration

---

# 🎓 Project Domain

**Artificial Intelligence / Natural Language Processing / Data Analytics**

---

# 💼 Applications

InsightSphere AI can be useful for:

* Students
* Researchers
* Job seekers
* Recruiters
* Data analysts
* Businesses
* Educational institutions
* Organizations handling large documents and datasets

---

🌐 Live Demo

Experience InsightSphere AI directly through the deployed web application.

🚀 Live Application:
Replace the URL above with your actual deployment URL after deploying the project.

Demo Modules

The live application allows users to:

📄 Upload and analyze PDF/TXT documents
📝 Generate document summaries and important points
🔑 Extract important keywords
📊 Analyze CSV and Excel datasets
📈 Generate interactive dashboards and graphs
🧾 Analyze resumes using the ATS system
🎯 Compare resumes with job descriptions
💡 Receive personalized recommendations



<img width="1536" height="1024" alt="LIVE-IMG" src="https://github.com/user-attachments/assets/528f10f5-26a8-4c29-bca1-05a75aae5eca" />


# ⚠️ Limitations

* Scanned/image-only PDFs require OCR support.
* Extractive summarization may not understand document context as deeply as large language models.
* Automatic recommendations depend on the information available in the uploaded file.
* ATS scoring is an approximation and does not represent the exact algorithm used by individual employers.
* Very complex PDF layouts may affect text extraction quality.

---

# 📌 Conclusion

InsightSphere AI combines **document intelligence, NLP, data analytics, visualization, ATS resume analysis, and recommendation generation** into a unified platform. The system converts large amounts of raw information into concise summaries, meaningful insights, interactive dashboards, ATS evaluations, and actionable recommendations, helping users understand their information more quickly and make better data-driven decisions.
