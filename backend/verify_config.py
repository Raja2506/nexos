from pathlib import Path
import tempfile
from app import config

with tempfile.TemporaryDirectory() as tmpdir:
    env_path = Path(tmpdir) / '.env'
    env_path.write_text(
        'OPENAI_API_KEY=abc123\nANTHROPIC_API_KEY=xyz789\nDATABASE_URL=postgresql://example\n',
        encoding='utf-8',
    )
    settings = config.load_environment(env_path=env_path)
    assert settings['OPENAI_API_KEY'] == 'abc123'
    assert settings['ANTHROPIC_API_KEY'] == 'xyz789'
    assert settings['DATABASE_URL'] == 'postgresql://example'
    print('config-ok')
