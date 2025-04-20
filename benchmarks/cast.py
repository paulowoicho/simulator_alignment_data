import json
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore[import-untyped]

from .base import BaseBenchMark


class CAsT2022(BaseBenchMark):
    """Represents the CAsT2022 Benchmark.

    Data can be found here: https://github.com/daltonj/treccastweb/blob/master/2022.

    Note that the collection is indexed by document (in trecweb format), but the task is
    passage retrieval. As such, we have to override ._get_passage_text so that we first
    get the document that holds the passage, then find the passage within it.
    """

    @staticmethod
    def _build_query_lookup(queries_path: Path | str) -> dict[str | int, str]:
        lookup: dict[str | int, str] = {}
        with open(queries_path, "r", encoding="utf‑8") as f:
            conversations = json.load(f)

        for conv in conversations:
            for turn in conv["turn"]:
                query_id = f"{conv['number']}_{turn['number']}"
                query = turn["manual_rewritten_utterance"]
                lookup[query_id] = query

        return lookup

    def _get_passage_text(self, passage_id: str | int) -> str:
        passage_id = str(passage_id)
        doc_id, passage_id = passage_id.rsplit("-", 1)
        doc = self.search_engine.doc(doc_id).raw()
        doc = BeautifulSoup(doc, "lxml")
        passage = doc.find("passage", {"id": passage_id})
        return passage.text if passage else ""
