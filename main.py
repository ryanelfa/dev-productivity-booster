import pandas  as pd
from tabulate import tabulate
from pathlib import Path

DATA_PATH = Path("data") / "Productivity.csv"

def calculate_score(row: pd.Series) -> float:
    """
    Weighted score:
      - commits: 40%
      - tests_passed: 30%
      - bugs_fixed: 20%
      - lines_added: 10% (scaled)
    """
    return (
        0.4 * float(row["commits"])
        + 0.3 * float(row["tests_passed"])
        + 0.2 * float(row["bugs_fixed"])
        + 0.1 * (float(row["lines_added"]) / 100.0)
    )
    
def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path, sep=",", encoding="utf-8")
    expected_cols = {"developer","commits","tests_passed","bugs_fixed","lines_added"}
    if set(df.columns) != expected_cols:
       raise ValueError(f"Unexpected columns {list(df.columns)}; expected {sorted(expected_cols)}")
    return df
    
def add_scores (df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["score"] = df.apply(calculate_score, axis=1)
    return df

def add_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["score"] = df.apply(calculate_score, axis=1)
    return df

def sort_by_score(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values("score", ascending=False).reset_index(drop=True)

def ai_comment(score: float) -> str:
    # Dummy “AI-like” comment for the demo (no external API)
    if score >= 85:
        return "Excellent momentum — keep leading by example."
    if score >= 75:
        return "Great performance — maintain consistency."
    if score >= 65:
        return "Solid — consider increasing test coverage."
    return "Opportunity to improve — focus on smaller, frequent commits."
    
def display_table(df: pd.DataFrame) -> None:
    print(
        tabulate(
            df[["developer","commits","tests_passed","bugs_fixed","lines_added","score"]],
            headers="keys",
            tablefmt="fancy_grid",
            showindex=False,
            floatfmt=".1f"
        )
    )
    print()  # blank line
    for _, row in df.iterrows():
        print(f"{row['developer']} → {ai_comment(row['score'])}")
    
def main() -> None:
    df = load_dataset(DATA_PATH)
    df = add_scores(df)
    df = sort_by_score(df)
    display_table(df)
    
if __name__ == "__main__":
    main()