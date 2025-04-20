import json
from pathlib import Path

from .base import BaseBenchMark


class iKAT2023(BaseBenchMark):
    """Represents the iKAT 2023 Benchmark.

    Since the shape of the queries hasn't changed from Year 1 to Year 2,
    this could possibly be resused for the 2024 query set.
    """

    @staticmethod
    def _build_query_lookup(queries_path: Path | str) -> dict[str | int, str]:
        lookup: dict[str | int, str] = {}
        with open(queries_path, "r", encoding="utf‑8") as f:
            conversations = json.load(f)

        for conv in conversations:
            for turn in conv["turns"]:
                query_id = f"{conv['number']}_{turn['turn_id']}"
                query = turn["resolved_utterance"]
                lookup[query_id] = query

        return lookup
