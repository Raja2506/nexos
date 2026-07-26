# backend/tests/test_code_generator_agent.py
from app.agents.code_generator_agent import CodeGeneratorAgent
from app.agents.bug_fix_agent import BugFixAgent


async def test_code_generator_agent_sum_of_squares():
    gen = CodeGeneratorAgent()
    result = await gen.run({"task": "Calculate the sum of squares from 1 to 10"})

    assert result is not None
    assert "code" in result

    fixer = BugFixAgent()
    final = await fixer.run({"code": result["code"]})

    assert final is not None
    assert "output" in final
    assert "attempts" in final
