import itertools
import json
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from convex_hull import compute_hull_dvcq
from generate import generate_random_points

from byu_pytest_utils import (
    measure_runtime,
    compute_average_runtimes,
    print_markdown_table,
)


def preprocessing(size):
    return generate_random_points("gaussian", size, 312)


def _dvcq_convex_hull(*points):
    compute_hull_dvcq(points)


def main(input, runtime_scalar):
    measure_runtime(
        _dvcq_convex_hull,
        input,
        runtime_scalar=runtime_scalar,
        preprocessing=preprocessing,
    )
    with open("_dvcq_convex_hull_runtimes.json", "r") as f:
        runtimes = json.load(f)

    ave_runtimes = compute_average_runtimes(runtimes)

    print_markdown_table(ave_runtimes, [" Size ", "Time (ms)"])


if __name__ == "__main__":
    sizes = [10, 100, 1000, 10000, 20000, 40000, 50000]
    runtime_scalar = 1000

    iterations = 10
    input_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes) for _ in range(iterations)
    )
    input_tuples = sorted(list(input_tuples_iterator))

    main(input_tuples, runtime_scalar)
