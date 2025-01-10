from __future__ import annotations

import ast
import io
import re
from dataclasses import dataclass
from typing import Any, Callable, Generator

type Parser = Callable[[list[str]], Generator[CodeAnimBlock, Any, None]]


@dataclass(frozen=True)
class CodeAnimBlock:
    labels: set[str]
    code: list[str]
    prelude: bool = False

    def __contains__(self, labels: set[str]) -> bool:
        return len(labels & self.labels) > 0

    def expressions(self) -> Generator[str, Any, None]:
        module = ast.parse("\n".join(self.code))
        for node in module.body:
            start = node.lineno - 1
            end = node.end_lineno if node.end_lineno is not None else start
            yield "\n".join(self.code[start:end])


@dataclass(frozen=True)
class CodeAnimBlocks:
    blocks: list[CodeAnimBlock]

    def filter(
        self, *, labels: set[str] | None = None, start_label: str | None = None
    ) -> Generator[CodeAnimBlock, Any, None]:
        found_start_label = False
        for block in self.blocks:
            if start_label in block.labels:
                found_start_label = True
            if (
                (labels is None and start_label is None)
                or (labels is not None and labels in block)
                or block.prelude
                or found_start_label
            ):
                yield block

    @staticmethod
    def parse(buffer: io.TextIOWrapper, parser: Parser) -> CodeAnimBlocks:
        lines = buffer.read().splitlines()
        blocks = list(parser(lines))
        return CodeAnimBlocks(blocks)

    @staticmethod
    def parse_file(path: str):
        with open(path) as fp:
            if path.endswith(".md"):
                return CodeAnimBlocks.parse(fp, markdown)
            if path.endswith(".py"):
                return CodeAnimBlocks.parse(fp, python)
        raise Exception(f"Unknown script type: {path}")


def markdown(lines: list[str]) -> Generator[CodeAnimBlock, Any, None]:
    is_codeanim = False
    labels, code, prelude = set(), [], False
    for line in lines:
        if line.startswith("```python"):
            tokens = line.strip().split()
            is_codeanim = len(tokens) > 1 and tokens[1] == "codeanim"
            labels = set(tokens[2:])
            prelude = "prelude" in labels
            continue
        if line == "```":
            yield CodeAnimBlock(labels, code, prelude)
            code, prelude = [], False
            prelude = False
            is_codeanim = False
            continue
        if is_codeanim:
            code.append(line)


def python(lines: list[str]) -> Generator[CodeAnimBlock, Any, None]:
    labels, code, prelude = set(), [], True
    for line in lines:
        if match := re.match(r"^#\s*%{2,}(.*)", line):
            if len(code) > 0:
                yield CodeAnimBlock(labels, code, prelude)
            labels = set(match[1].strip().split())
            code, prelude = [], False
        else:
            code.append(line)
    if len(code) > 0:
        yield CodeAnimBlock(labels, code, prelude)
