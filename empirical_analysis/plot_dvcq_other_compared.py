import json
import matplotlib.pyplot as plt
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from byu_pytest_utils import compute_average_runtimes


def main():

    filename = "_dvcq_convex_hull_runtimes.json"

    with open(filename, "r") as f:
        dvcq_runtimes = json.load(f)

    filename = "_other_convex_hull_runtimes.json"

    with open(filename, "r") as f:
        other_runtimes = json.load(f)

    dvcq_average = compute_average_runtimes(dvcq_runtimes)
    other_average = compute_average_runtimes(other_runtimes)

    dvcq_sizes, dvcq_times = zip(*dvcq_average)
    other_sizes, other_times = zip(*other_average)

    fig = plt.figure()

    # Update title, legend, and axis labels as needed

    plt.plot(dvcq_sizes, dvcq_times, c="k", lw=2, alpha=0.5, label="DVCQ")
    plt.plot(other_sizes, other_times, c="m", lw=2, alpha=0.5, label="[FILL ME IN]")

    plt.legend()
    plt.xlabel("n")
    plt.ylabel("Runtime (sec)")
    plt.title("Time for DVCQ Convex Hull vs. [FILL ME IN] Convex Hull")

    fig.show()
    fig.savefig("dvcq_v_other.svg")


if __name__ == "__main__":
    main()
