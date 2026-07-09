from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv

with tempfile.TemporaryDirectory() as tmpdir:
    p = Path(tmpdir) / '.env'
    p.write_text('OPENAI_API_KEY=abc123\nANTHROPIC_API_KEY=xyz789\nDATABASE_URL=postgresql://example\n', encoding='utf-8')
    print('exists', p.exists())
    print('load', load_dotenv(p, override=False))
    print('openai', os.getenv('OPENAI_API_KEY'))
    print('anthropic', os.getenv('ANTHROPIC_API_KEY'))
    print('database', os.getenv('DATABASE_URL'))
