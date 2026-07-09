from pathlib import Path

from app import config


def test_load_environment_reads_api_keys_from_dotenv_file(tmp_path: Path) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text(
        "OPENAI_API_KEY=abc123\nANTHROPIC_API_KEY=xyz789\nDATABASE_URL=postgresql://example\n",
        encoding="utf-8",
    )

    settings = config.load_environment(env_path=env_path)

    assert settings["OPENAI_API_KEY"] == "abc123"
    assert settings["ANTHROPIC_API_KEY"] == "xyz789"
    assert settings["DATABASE_URL"] == "postgresql://example"
