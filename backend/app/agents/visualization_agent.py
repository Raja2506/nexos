import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import uuid
from pathlib import Path
from app.agents.base_agent import BaseAgent

CHART_OUTPUT_DIR = Path("chart_outputs")
CHART_OUTPUT_DIR.mkdir(exist_ok=True)


class VisualizationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="VisualizationAgent")

    async def run(self, input_data: dict) -> dict:
        rows = input_data["rows"]
        x_column = input_data["x_column"]
        y_column = input_data["y_column"]
        chart_type = input_data.get("chart_type", "bar")

        self.log(f"Generating {chart_type} chart: {x_column} vs {y_column}")

        df = pd.DataFrame(rows)

        fig, ax = plt.subplots(figsize=(8, 5))
        if chart_type == "bar":
            ax.bar(df[x_column], df[y_column])
        elif chart_type == "line":
            ax.plot(df[x_column], df[y_column])
        else:
            raise ValueError(f"Unsupported chart_type: {chart_type}")

        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"{y_column} by {x_column}")

        filename = f"{uuid.uuid4().hex}.png"
        filepath = CHART_OUTPUT_DIR / filename
        fig.savefig(filepath)
        plt.close(fig)

        self.log(f"Chart saved: {filepath}")
        return {"chart_path": str(filepath)}