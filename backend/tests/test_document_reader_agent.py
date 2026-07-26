# backend/tests/test_document_reader_agent.py
import pandas as pd
from pathlib import Path
from app.agents.document_reader_agent import DocumentReaderAgent


async def test_document_reader_agent_reads_csv():
    sample_path = Path("tests/sample_data.csv")
    df = pd.DataFrame({
        "product": ["Widget A", "Widget B", "Widget C"],
        "price": [19.99, 29.99, 39.99],
        "stock": [100, 50, 25],
    })
    df.to_csv(sample_path, index=False)

    agent = DocumentReaderAgent()
    result = await agent.run({"file_path": str(sample_path)})

    assert result is not None
    assert "file_name" in result
    assert "text" in result
