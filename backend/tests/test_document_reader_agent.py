# backend/tests/test_document_reader_agent.py
import asyncio
import pandas as pd
from pathlib import Path
from app.agents.document_reader_agent import DocumentReaderAgent

async def main():
    # Create a sample CSV for testing
    sample_path = Path("tests/sample_data.csv")
    df = pd.DataFrame({
        "product": ["Widget A", "Widget B", "Widget C"],
        "price": [19.99, 29.99, 39.99],
        "stock": [100, 50, 25],
    })
    df.to_csv(sample_path, index=False)

    agent = DocumentReaderAgent()
    result = await agent.run({"file_path": str(sample_path)})
    print(f"File: {result['file_name']}")
    print(f"Extracted text:\n{result['text']}")

asyncio.run(main())