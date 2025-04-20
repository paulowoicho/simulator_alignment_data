from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
import random
from typing import Generator

from pyserini.search.lucene import LuceneSearcher  # type: ignore[import-not-found]


@dataclass(frozen=True)
class Qrel:
    query_id: str | int
    query: str
    passage_id: str | int
    passage: str
    relevance: int


class BaseBenchMark(ABC):
    def __init__(
        self, queries_path: str | Path, qrels_path: str | Path, index_path: str | Path
    ) -> None:
        """Creates an instance of BenchMark.

        Args:
            queries_path (str | Path): The path to the queries file.
            qrels_path (str | Path): The path to the qrels file. Note that this is expected to be in the TREC format.
            index_path (str | Path): The path to a pyserini compatible Lucene index.
        """
        self.query_lookup = self._build_query_lookup(queries_path)
        self.qrels_path = qrels_path
        self.search_engine = LuceneSearcher(index_path)

    @staticmethod
    @abstractmethod
    def _build_query_lookup(queries_path: str | Path) -> dict[str | int, str]:
        """Helper method to build a query id to query lookup table.

        As the format of queries will vary between datasets, this is up to the subclass to implement.

        Args:
            queries_path (str | Path): The path to the queries file.

        Returns:
            dict[str | int, str]: A lookup table, mapping query id to query.
        """
        ...

    def get_sampled_data(
        self, num_samples: int = 10_000, seed: int = 42
    ) -> Generator[Qrel, None, None]:
        """Uses resevoir sampling to create `num_samples` random query-passage-relevance triplets from a qrel file.

        Args:
            num_samples (int, optional): The number of triplets to create. Defaults to 10_000.
            seed (int, optional): Seed for reproducibility. Defaults to 42.

        Returns:
            Generator[Qrel, None, None]: A generator of random `num_sample` query-passage-relevance triplets as Qrel objects.
        """
        rng = random.Random(seed)
        reservoir: list[tuple[str, str, int]] = []

        with open(self.qrels_path) as f:
            for idx, line in enumerate(f):
                query_id, _, passage_id, relevance = line.split()
                int_relevance: int = int(relevance)
                if idx < num_samples:
                    reservoir.append((query_id, passage_id, int_relevance))
                else:
                    rand_idx = rng.randint(0, idx)
                    if rand_idx < num_samples:
                        reservoir[rand_idx] = (query_id, passage_id, int_relevance)

        for query_id, passage_id, int_relevance in reservoir:
            yield Qrel(
                query_id=query_id,
                query=self.query_lookup[query_id],
                passage_id=passage_id,
                passage=self._get_passage_text(passage_id),
                relevance=int_relevance,
            )

    def _get_passage_text(self, passage_id: int | str) -> str:
        """Retrieves the passage text from a search engine.

        Args:
            passage_id (int | str): The passage id of the passage to retrieve.

        Returns:
            str: The text of the passage.
        """
        passage = self.search_engine.doc(passage_id)
        return passage.contents() if passage else ""

    @property
    def name(self) -> str:
        """Gets the name of the BenchMark

        Returns:
            str: Benchmark name.
        """
        return self.__class__.__name__
