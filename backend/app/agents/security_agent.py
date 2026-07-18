import re
from app.agents.base_agent import BaseAgent

SECRET_PATTERNS = [
    r"sk-ant-api\d*-[A-Za-z0-9_-]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"AIza[A-Za-z0-9_-]{35}",
    r"postgresql://[^:]+:[^@]+@",
    r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----",
]

DANGEROUS_CODE_PATTERNS = [
    r"\bos\.system\(",
    r"\bsubprocess\.(run|call|Popen)\(",
    r"\beval\(",
    r"\bexec\(",
    r"rm\s+-rf",
    r"DROP\s+TABLE",
    r"DELETE\s+FROM\s+\w+\s*(?!WHERE)",
]


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SecurityAgent")

    async def run(self, input_data: dict) -> dict:
        content = input_data["content"]
        self.log(f"Scanning {len(content)} characters")

        secrets_found = self._scan_patterns(content, SECRET_PATTERNS)
        dangerous_found = self._scan_patterns(content, DANGEROUS_CODE_PATTERNS)

        is_safe = not secrets_found and not dangerous_found

        if not is_safe:
            self.log(f"BLOCKED: {len(secrets_found)} secrets, {len(dangerous_found)} dangerous patterns")
        else:
            self.log("Content passed security scan")

        return {
            "is_safe": is_safe,
            "secrets_found": secrets_found,
            "dangerous_patterns_found": dangerous_found,
        }

    def _scan_patterns(self, content: str, patterns: list) -> list:
        matches = []
        for pattern in patterns:
            if re.search(pattern, content):
                matches.append(pattern)
        return matches