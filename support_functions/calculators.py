from typing import List

from statistics import mean


def calculate_moving_average(value_list: List[float], n: int) -> List[float]:
    moving_average = []

    data_length = len(value_list)
    if n > data_length:
        raise ValueError(
            'N cannot be greater than the length'
            f' of the data! Maximum is {data_length}'
        )

    for i, elem in enumerate(value_list):
        if i < n - 1:
            continue

        matched_sublist = value_list[i - (n - 1): i + 1]
        moving_average.append(mean(matched_sublist))

    return moving_average
