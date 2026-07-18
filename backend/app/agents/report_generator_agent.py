from datetime import datetime
from app.agents.base_agent import BaseAgent


class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ReportGeneratorAgent")

    async def run(self, input_data: dict) -> dict:
        title = input_data["title"]
        sections = input_data["sections"]

        self.log(f"Generating report: {title} ({len(sections)} sections)")

        report_lines = [
            f"# {title}",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
        ]

        for section in sections:
            report_lines.append(f"## {section['heading']}")
            report_lines.append(section["content"])
            report_lines.append("")

        report_text = "\n".join(report_lines)
        self.log(f"Report generated: {len(report_text)} characters")

        return {"report": report_text}