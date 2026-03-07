from byu_pytest_utils import compute_coefficient
import math


def main():

    filename = "_dvcq_convex_hull_runtimes.json"

    def theoretical_big_o(n):
        # FILL THIS IN with your theoretical time complexity
        return n

    # Changing these values takes a slice of your runtimes corresponding with the indices

    start = None
    end = None

    compute_coefficient(filename, theoretical_big_o, start, end)


if __name__ == "__main__":
    main()
