from app.agents.base_agent import BaseAgent


class PresentationAgent(BaseAgent):
    """
    Converts a report (title + sections) into a simple slide structure
    - a list of slides, each with a title and bullet points.
    """

    def __init__(self):
        super().__init__(name="PresentationAgent")

    async def run(self, input_data: dict) -> dict:
        title = input_data["title"]
        sections = input_data["sections"]

        self.log(f"Building {len(sections) + 1} slides for: {title}")

        slides = [{"slide_number": 1, "title": title, "bullets": ["Overview"]}]

        for i, section in enumerate(sections, start=2):
            bullets = self._content_to_bullets(section["content"])
            slides.append({
                "slide_number": i,
                "title": section["heading"],
                "bullets": bullets,
            })

        return {"slides": slides}

    def _content_to_bullets(self, content: str) -> list:
        sentences = [s.strip() for s in content.split(".") if s.strip()]
        return sentences[:5]