"""
This module implements Adaptor functions for partitioning algorithms.

The functions accept a partitioning algorithm as an argument.

They allow you to call the partitioning algorithm with convenient input types,
such as: a list of values, or a dict that maps an item to its value.

Author: Erel Segal-Halevi
Since: 2022-07
"""

import numpy as np

import prtpy
from prtpy import outputtypes as out, objectives as obj, Bins
from typing import Callable, List, Any

def partition(
    algorithm: Callable,
    numbins: int,
    items: Any,
    valueof: Callable[[Any], float] = None,
    outputtype: out.OutputType = out.Partition,
    **kwargs
) -> List[List[int]]:
    """
    An adaptor partition function.

    :param algorithm: a specific number-partitioning algorithm. Should accept (at least) the following parameters: 
        numbins (int), 
        items (list), 
        valueof (callable), 
        outputtype (OutputType).

    :param numbins: int - how many parts should be in the partition?

    :param items: can be one of the following:
       * A list of values  (so that each item is equal to its value);
       * A dict where the keys are the items and the vals are the item values;
       * A list of strings (in this case, valueof should also be defined, and map each item name to its value);

    :param valueof: optional; required only if `items` is a list of item-names.

    :param outputtype: defines the output format. See `outputtypes.py'.

    :param kwargs: any other arguments expected by `algorithm`.

    :return: a partition, or a list of sums - depending on outputtype.

    >>> dp = prtpy.partitioning.dynamic_programming
    >>> import numpy as np
    >>> partition(algorithm=dp, numbins=2, items=[1,2,3,3,5,9,9])
    [[2, 5, 9], [1, 3, 3, 9]]
    >>> partition(algorithm=dp, numbins=3, items=[1,2,3,3,5,9,9])
    [[2, 9], [1, 9], [3, 3, 5]]
    >>> partition(algorithm=dp, numbins=2, items=np.array([1,2,3,3,5,9,9]), outputtype=out.Sums)
    [16.0, 16.0]
    >>> int(partition(algorithm=dp, numbins=3, items=[1,2,3,3,5,9,9], outputtype=out.LargestSum))
    11
    >>> partition(algorithm=dp, numbins=2, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['b', 'e', 'f'], ['a', 'c', 'd', 'g']]
    >>> partition(algorithm=dp, numbins=3, items={"a":1, "b":2, "c":3, "d":3, "e":5, "f":9, "g":9})
    [['b', 'g'], ['a', 'f'], ['c', 'd', 'e']]

    >>> traversc_example = [18, 12, 22, 22]
    >>> prtpy.partition(algorithm=prtpy.partitioning.integer_programming, numbins=2, items=traversc_example, outputtype=prtpy.out.PartitionAndSums)
    Bin #0: [12, 22], sum=34.0
    Bin #1: [18, 22], sum=40.0
    """
    if isinstance(items, dict):  # items is a dict mapping an item to its value.
        item_names = items.keys()
        if valueof is None:
            valueof = items.__getitem__
    else:  # items is a list
        item_names = items
        if valueof is None:
            valueof = lambda item: item
    bins = outputtype.create_empty_bins(numbins, valueof)
    bins = algorithm(bins, item_names, valueof, **kwargs)

    if isinstance(bins, Bins):
        return outputtype.extract_output_from_bins(bins)
    else:
        return outputtype.extract_output_from_binsarray(bins)

def partition_random_items(numitems: int, bitsperitem: int, **kwargs):
    """
    Generates a uniformly-random list of items and partitions them using the given algorithm.

    :param numitems: how many items to generate.
    :param bitsperitem: how many bits in each item.
    :param kwargs: keyword arguments delegated to `partition`.
    """
    items = np.random.randint(1, 2**bitsperitem-1, numitems, dtype=np.int64)
    return partition(items=items, **kwargs)


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    print(partition_random_items(10, 16, algorithm=prtpy.partitioning.greedy, numbins=2, outputtype=out.PartitionAndSums))