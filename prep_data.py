from dataclasses import asdict
from pathlib import Path

from benchmarks.base import BaseBenchMark
from benchmarks.cast import CAsT2022
from benchmarks.ikat import iKAT2023
import jsonlines  # type: ignore[import-not-found]
import tqdm  # type: ignore[import-untyped]

NUM_SAMPLES_TO_CREATE = 7500

if __name__ == "__main__":
    # Replace with actual paths.
    benchmarks: list[BaseBenchMark] = [
        CAsT2022(
            queries_path="../../data/cast/queries/annotated_topics.json",
            qrels_path="../../data/cast/queries/cast2022.qrel",
            index_path="../../data/cast/trecweb_index/",
        ),
        iKAT2023(
            queries_path="../../data/ikat/data/queries/2023_test_topics.json",
            qrels_path="../../data/ikat/data/queries/2023-qrels.all-turns.txt",
            index_path="../../data/ikat/data/indexes/sparse/",
        ),
    ]

    for benchmark in benchmarks:
        output_dir = Path("data") / benchmark.name
        output_dir.mkdir(parents=True, exist_ok=True)

        with jsonlines.open(output_dir / "alignment_data.jsonl", "w") as f:
            for qrel in tqdm.tqdm(
                benchmark.get_sampled_data(num_samples=NUM_SAMPLES_TO_CREATE),
                total=NUM_SAMPLES_TO_CREATE,
                desc=f"Preparing data for {benchmark.name} benchmark.",
            ):
                f.write(asdict(qrel))
