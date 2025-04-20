from dataclasses import asdict
from pathlib import Path

import jsonlines  # type: ignore[import-not-found]
import tqdm  # type: ignore[import-untyped]

from base import BaseBenchMark  # type: ignore[import-not-found]
from cast import CAsT2022  # type: ignore[import-not-found]
from ikat import iKAT2023  # type: ignore[import-not-found]

NUM_SAMPLES_TO_CREATE = 7500

if __name__ == "__main__":
    # Replace with actual paths.
    benchmarks: list[BaseBenchMark] = [
        CAsT2022(
            queries_path="path/to/queries",
            qrels_path="path/to/qrels",
            index_path="path/to/index",
        ),
        iKAT2023(
            queries_path="path/to/queries",
            qrels_path="path/to/qrels",
            index_path="path/to/index",
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
