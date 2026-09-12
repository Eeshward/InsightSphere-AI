def build_text_report(filename, summary, important_points, keywords, stats):
    lines = []
    lines.append("PDF & DATA INTELLIGENCE DASHBOARD")
    lines.append("=" * 50)
    lines.append(f"File: {filename}")
    lines.append("")

    lines.append("DOCUMENT STATISTICS")
    lines.append("-" * 50)
    for key, value in stats.items():
        lines.append(f"{key}: {value}")

    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 50)
    lines.append(summary)

    lines.append("")
    lines.append("IMPORTANT POINTS")
    lines.append("-" * 50)
    for i, point in enumerate(important_points, 1):
        lines.append(f"{i}. {point}")

    lines.append("")
    lines.append("TOP KEYWORDS")
    lines.append("-" * 50)
    lines.append(", ".join(keywords))

    return "\n".join(lines)
