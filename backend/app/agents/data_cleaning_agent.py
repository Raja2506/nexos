import pandas as pd
from app.agents.base_agent import BaseAgent


class DataCleaningAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="DataCleaningAgent")

    async def run(self, input_data: dict) -> dict:
        rows = input_data["rows"]
        self.log(f"Cleaning {len(rows)} rows")

        if not rows:
            return {"cleaned_rows": [], "report": "No data to clean"}

        df = pd.DataFrame(rows)

        original_count = len(df)
        df = df.drop_duplicates()
        duplicates_removed = original_count - len(df)

        missing_before = df.isnull().sum().sum()
        for col in df.columns:
            if df[col].dtype in ["float64", "int64"]:
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna("unknown")

        report = (
            f"Removed {duplicates_removed} duplicate rows. "
            f"Filled {missing_before} missing values."
        )
        self.log(report)

        return {"cleaned_rows": df.to_dict(orient="records"), "report": report}