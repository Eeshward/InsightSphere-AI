def document_recommendations(result):
    recs = []
    wc = result.get("word_count", 0)
    keywords = [k for k, _ in result.get("keywords", [])]
    summary = result.get("summary", "")

    if wc > 5000:
        recs.append("Create section-wise summaries because the document is long.")
    elif wc < 300:
        recs.append("The document is short; focus on extracting conclusions and key facts.")

    if len(keywords) >= 5:
        recs.append(
            "Review the top keywords to identify the main themes: "
            + ", ".join(keywords[:5]) + "."
        )

    if result.get("important_points"):
        recs.append("Use the extracted important points as the basis for a presentation or executive brief.")

    if "result" in summary.lower() or "conclusion" in summary.lower():
        recs.append("The document appears result-oriented; create a findings vs. conclusions comparison.")

    if not recs:
        recs.append("Use the summary and keyword dashboard to identify the document's main themes.")

    return recs


def data_recommendations(df):
    recs = []
    missing = df.isna().sum()
    missing_cols = missing[missing > 0].sort_values(ascending=False)

    if len(missing_cols):
        col = missing_cols.index[0]
        recs.append(
            f"Clean missing values before modeling. '{col}' has the highest missing-value count."
        )
    else:
        recs.append("No missing values were detected; the dataset is ready for deeper analysis.")

    duplicates = int(df.duplicated().sum())
    if duplicates:
        recs.append(f"Remove or review {duplicates} duplicate rows before further analysis.")

    numeric = list(df.select_dtypes(include="number").columns)
    categorical = list(df.select_dtypes(include=["object", "category", "bool"]).columns)

    if len(numeric) >= 2:
        recs.append("Use correlation and trend analysis to identify strongly related numerical variables.")

    if categorical:
        recs.append(
            f"Segment the data using categorical fields such as '{categorical[0]}' "
            "to compare patterns across groups."
        )

    if numeric:
        recs.append(
            f"Consider predictive modeling using '{numeric[0]}' or another business target "
            "if a clear prediction objective exists."
        )

    return recs


def ats_recommendations(ats):
    recs = []

    if ats.get("ats_score", 0) < 65:
        recs.append("Improve ATS compatibility by aligning the resume more closely with the job description.")
    else:
        recs.append("The resume has a reasonable ATS base; focus on improving role-specific relevance.")

    missing_skills = ats.get("missing_skills", [])
    if missing_skills:
        recs.append(
            "Where truthful, add evidence for these missing skills in Skills, Projects, or Experience: "
            + ", ".join(missing_skills[:8]) + "."
        )

    if ats.get("keyword_match_score", 100) < 70:
        missing_kw = ats.get("missing_keywords", [])
        if missing_kw:
            recs.append(
                "Increase job-description keyword alignment using relevant terms such as: "
                + ", ".join(missing_kw[:8]) + "."
            )

    issues = ats.get("issues", [])
    recs.extend(issues[:4])

    if not ats.get("sections", {}).get("projects"):
        recs.append("Add a clearly labeled Projects section with technologies, responsibilities, and measurable outcomes.")

    if not ats.get("sections", {}).get("summary"):
        recs.append("Add a short professional summary tailored to the target role.")

    return recs
