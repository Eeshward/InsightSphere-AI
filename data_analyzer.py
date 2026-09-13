import streamlit as st
import pandas as pd
import numpy as np
from recommendation_engine import data_recommendations

def _datetime_columns(df):
    cols = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            cols.append(col)
        elif df[col].dtype == "object":
            sample = df[col].dropna().astype(str).head(20)
            if len(sample) >= 5:
                parsed = pd.to_datetime(sample, errors="coerce")
                if parsed.notna().mean() >= 0.8:
                    cols.append(col)
    return cols

def _overview(df):
    rows, cols = df.shape
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    numeric_count = len(df.select_dtypes(include=np.number).columns)

    a, b, c, d, e = st.columns(5)
    a.metric("Rows", f"{rows:,}")
    b.metric("Columns", cols)
    c.metric("Numeric", numeric_count)
    d.metric("Missing", f"{missing:,}")
    e.metric("Duplicates", f"{duplicates:,}")

    st.subheader("Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

def _quality(df):
    q = pd.DataFrame({
        "Column": df.columns,
        "Type": [str(df[c].dtype) for c in df.columns],
        "Missing": [int(df[c].isna().sum()) for c in df.columns],
        "Missing %": [round(df[c].isna().mean()*100, 2) for c in df.columns],
        "Unique": [int(df[c].nunique(dropna=True)) for c in df.columns]
    })
    st.dataframe(q, use_container_width=True)

    miss = q[q["Missing"] > 0]
    if not miss.empty:
        st.subheader("Missing Values Dashboard")
        st.bar_chart(miss.set_index("Column")["Missing"])

def _numeric_dashboard(df):
    num = df.select_dtypes(include=np.number)
    if num.empty:
        st.info("No numeric columns available.")
        return

    st.subheader("Numeric Summary")
    st.dataframe(num.describe().T, use_container_width=True)

    selected = st.selectbox("Select numeric column", num.columns, key="num_select")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribution")
        series = num[selected].dropna()
        bins = min(20, max(5, int(np.sqrt(max(len(series), 1)))))
        counts, edges = np.histogram(series, bins=bins)
        hist_df = pd.DataFrame({
            "Range": [f"{edges[i]:.1f}-{edges[i+1]:.1f}" for i in range(len(counts))],
            "Count": counts
        })
        st.bar_chart(hist_df.set_index("Range")["Count"])

    with col2:
        st.markdown("#### Running Trend")
        trend = series.reset_index(drop=True)
        st.line_chart(trend)

def _categorical_dashboard(df):
    cats = df.select_dtypes(include=["object", "category", "bool"])
    if cats.empty:
        st.info("No categorical columns available.")
        return

    selected = st.selectbox("Select categorical column", cats.columns, key="cat_select")
    counts = df[selected].astype(str).value_counts().head(15)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Category Frequency")
        st.bar_chart(counts)
    with col2:
        st.markdown("#### Category Share")
        st.dataframe(
            pd.DataFrame({
                "Category": counts.index,
                "Count": counts.values,
                "Share %": (counts.values / counts.values.sum() * 100).round(2)
            }),
            use_container_width=True,
            hide_index=True
        )

def _correlation(df):
    num = df.select_dtypes(include=np.number)
    if num.shape[1] < 2:
        st.info("At least two numeric columns are required.")
        return

    corr = num.corr(numeric_only=True)
    st.subheader("Correlation Matrix")
    st.dataframe(corr.round(2), use_container_width=True)

    pairs = []
    for i, c1 in enumerate(corr.columns):
        for j, c2 in enumerate(corr.columns):
            if i < j and pd.notna(corr.loc[c1, c2]):
                pairs.append((c1, c2, float(corr.loc[c1, c2])))

    pairs = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)
    if pairs:
        top = pd.DataFrame(pairs[:10], columns=["Variable 1", "Variable 2", "Correlation"])
        st.markdown("#### Strongest Relationships")
        st.dataframe(top, use_container_width=True, hide_index=True)
        chart_df = top.copy()
        chart_df["Pair"] = chart_df["Variable 1"] + " × " + chart_df["Variable 2"]
        st.bar_chart(chart_df.set_index("Pair")["Correlation"])

def _trend(df):
    dates = _datetime_columns(df)
    nums = list(df.select_dtypes(include=np.number).columns)
    if not dates or not nums:
        st.info("Need at least one date column and one numeric column.")
        return

    date_col = st.selectbox("Date column", dates, key="trend_date")
    value_col = st.selectbox("Value column", nums, key="trend_value")

    temp = df[[date_col, value_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp = temp.dropna().sort_values(date_col)
    if temp.empty:
        st.info("No valid trend data.")
        return

    st.line_chart(temp.set_index(date_col)[value_col])

def analyze_dataframe(df, filename):
    st.success(f"Dataset loaded: {filename}")

    tabs = st.tabs([
        "🏠 Overview",
        "🧹 Data Quality",
        "📊 Numeric Dashboard",
        "🗂 Category Dashboard",
        "🔗 Correlation",
        "📈 Trend Analysis",
        "💡 Recommendations"
    ])

    with tabs[0]:
        _overview(df)

    with tabs[1]:
        _quality(df)

    with tabs[2]:
        _numeric_dashboard(df)

    with tabs[3]:
        _categorical_dashboard(df)

    with tabs[4]:
        _correlation(df)

    with tabs[5]:
        _trend(df)

    with tabs[6]:
        st.subheader("Recommended Next Actions")
        for i, rec in enumerate(data_recommendations(df), 1):
            st.markdown(f"**{i}.** {rec}")

    st.download_button(
        "⬇️ Download analyzed CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="analyzed_data.csv",
        mime="text/csv"
    )
