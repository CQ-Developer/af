from pathlib import Path

import pytest

from af.agent.tools.read_file import ReadFileTool
from af.core import ToolExecuteException


@pytest.fixture(scope="module")
def tool() -> ReadFileTool:
    return ReadFileTool()


async def test_file_does_not_exist(tmp_path: Path, tool: ReadFileTool) -> None:
    missing = tmp_path / "missing.txt"

    with pytest.raises(ToolExecuteException, match="does not exist"):
        await tool.execute({"file_path": str(missing)})


async def test_not_a_regular_file(tmp_path: Path, tool: ReadFileTool) -> None:
    with pytest.raises(ToolExecuteException, match="is not a regular file"):
        await tool.execute({"file_path": str(tmp_path)})


async def test_more_than_1000_lines(tmp_path: Path, tool: ReadFileTool) -> None:
    path = tmp_path / "long.txt"
    path.write_text("".join(f"{i}\n" for i in range(1, 1002)), encoding="utf-8")

    result = await tool.execute({"file_path": str(path), "end_line": 1001})

    assert len(result["lines"]) == 1000
    assert result["lines"][-1]["line_number"] == 1000
    assert result.get("remark") == "Output truncated at 1000 lines. Call again with start_line=1001 to read more."


async def test_more_than_64_kib(tmp_path: Path, tool: ReadFileTool) -> None:
    path = tmp_path / "large.txt"
    line = "x" * 1023 + "\n"  # 1024 bytes
    path.write_text(line * 65, encoding="utf-8")

    result = await tool.execute({"file_path": str(path)})

    assert len(result["lines"]) == 64
    assert sum(len(item["content"].encode("utf-8")) for item in result["lines"]) == 64 * 1024
    assert result.get("remark") == "Output truncated at 65536 bytes. Call again with start_line=65 to read more."
