import asyncio
from pathlib import Path
from typing import Any, NotRequired, TypedDict, override

from af.core import Tool, ToolExecuteException


class LineContent(TypedDict):
    line_number: int
    content: str


class ReadFileResult(TypedDict):
    lines: list[LineContent]
    remark: NotRequired[str]


class ReadFileTool(Tool[ReadFileResult]):
    @property
    @override
    def name(self) -> str:
        return "read_file"

    @property
    @override
    def description(self) -> str:
        return "Reads a range of lines from a file and returns them with line numbers, up to 1000 lines per call."

    @property
    @override
    def parameter_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The relative or absolute path.",
                },
                "start_line": {
                    "type": "integer",
                    "description": "1-based line number, inclusive, default 1.",
                },
                "end_line": {
                    "type": "integer",
                    "description": "1-based line number, inclusive, default EOF.",
                },
            },
            "required": ["file_path"],
        }

    @override
    async def execute(self, p: dict[str, Any]) -> ReadFileResult:
        file_path = self._check_file_path(p.get("file_path"))
        start_line = self._check_start_line(p.get("start_line"))
        end_line = self._check_end_line(start_line, p.get("end_line"))
        return await asyncio.to_thread(self._execute_read_file, file_path, start_line, end_line)

    def _check_file_path(self, file_path: Any) -> Path:
        if not file_path:
            raise ToolExecuteException("Error: file_path cannot be null or empty.")
        if not isinstance(file_path, str):
            raise ToolExecuteException("Error: file_path must be string.")
        p = Path(file_path)
        if not p.exists():
            raise ToolExecuteException(f"Error: `{file_path}` does not exist.")
        if not p.is_file():
            raise ToolExecuteException(f"Error: `{file_path}` is not a regular file.")
        return p

    def _check_start_line(self, start_line: Any) -> int:
        if start_line is None:
            return 1
        if not isinstance(start_line, int):
            raise ToolExecuteException("Error: start_line must be an integer.")
        if start_line < 1:
            raise ToolExecuteException(f"Error: start_line must be 1-based, got `{start_line}`.")
        return start_line

    def _check_end_line(self, start_line: int, end_line: Any) -> int:
        if end_line is None:
            return start_line + 999
        if not isinstance(end_line, int):
            raise ToolExecuteException("Error: end_line must be an integer.")
        if end_line < 1:
            raise ToolExecuteException(f"Error: end_line must be 1-based, got `{end_line}`.")
        if end_line < start_line:
            raise ToolExecuteException(f"Error: end_line must be less than start_line, got `{end_line}`.")
        return end_line

    def _execute_read_file(self, file_path: Path, start_line: int, end_line: int) -> ReadFileResult:
        result: ReadFileResult = {"lines": []}
        with file_path.open("r", encoding="utf-8", errors="replace") as f:
            cnt = 0
            for i, s in enumerate(f):
                if i < start_line - 1:
                    continue
                if i >= end_line:
                    break
                cnt += 1
                if cnt > 1000:
                    result["remark"] = (
                        f"Output truncated: only {cnt - 1} lines are shown. "
                        f"To read more, call again with `start_line={start_line + cnt - 1}`."
                    )
                    break
                result["lines"].append({"line_number": i + 1, "content": s})
        if not len(result["lines"]):
            result["remark"] = (
                f"No content from line {start_line} "
                f"to {end_line if end_line is not None else 'EOF'}. "
                f"Check the file line count."
            )
        return result
