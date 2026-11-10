def md_table(df, index=True) -> str:
    """DataFrame -> GitHub markdown table (replaces DataFrame.to_markdown, which needs the optional tabulate package)"""
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    rows = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in d.itertuples(index=False):
        rows.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(rows)
