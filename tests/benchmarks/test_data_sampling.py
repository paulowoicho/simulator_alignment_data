# tests/benchmarks/test_data_sampling.py

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from benchmarks.base import BaseBenchMark
import pytest  # type: ignore[import-not-found]


class DummyBenchmark(BaseBenchMark):
    @staticmethod
    def _build_query_lookup(queries_path: str | Path) -> dict[str | int, str]:
        return {"1": "query one", "2": "query two", "3": "query three"}


@pytest.fixture
def mock_qrel_data() -> str:
    # three lines of TREC‐style qrels: query_id, unused, doc_id, relevance
    return "1 0 DOC1 2\n2 0 DOC2 1\n3 0 DOC3 0\n"


@pytest.fixture
def mock_searcher() -> MagicMock:
    # A fake LuceneSearcher.doc() that returns a stub with .contents()
    searcher = MagicMock()
    doc1, doc2, doc3 = [MagicMock() for _ in range(3)]
    doc1.contents.return_value = "passage one"
    doc2.contents.return_value = "passage two"
    doc3.contents.return_value = "passage three"
    searcher.doc.side_effect = lambda pid: {
        "DOC1": doc1,
        "DOC2": doc2,
        "DOC3": doc3,
    }.get(pid)
    return searcher


@patch("benchmarks.base.LuceneSearcher")
def test_get_sampled_data(mock_lucene_cls, mock_qrel_data, mock_searcher):
    mock_lucene_cls.return_value = mock_searcher

    m = mock_open(read_data=mock_qrel_data)
    with patch("builtins.open", m):
        benchmark = DummyBenchmark("queries.txt", "qrels.txt", "index_path")
        sampled = list(benchmark.get_sampled_data(num_samples=2, seed=42))

    assert len(sampled) == 2, (
        "Reservoir sampling with seed=42 over 3 items and num_samples=2 should yield exactly 2 items"
    )

    seen_ids = {q.query_id for q in sampled}
    seen_queries = {q.query for q in sampled}
    seen_passages = {q.passage for q in sampled}
    seen_relevances = {q.relevance for q in sampled}

    assert seen_ids.issubset({"1", "2", "3"})
    assert seen_queries.issubset({"query one", "query two", "query three"})
    assert seen_passages.issubset({"passage one", "passage two", "passage three"})
    assert seen_relevances.issubset({0, 1, 2})
