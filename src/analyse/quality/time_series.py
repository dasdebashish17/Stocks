"""
Time series analysis of the stocks to understand how good the stock is.
* Is it always increasing with minor fluctuations
* Is it always increasing with major fluctuations
* Is it mostly swinging with minor fluctuations
* Is it mostly swinging with major fluctuations
* Is it gradually decreasing with minor/major fluctuations

For such analysis, tsfel module is used.

Procedure:
  Load past 5 years data
  partition_steps = 1
  while partition_steps < 5:
    find [trend, seasonality, residue] from 'partition_steps' of data
    store [trend, seasonality, residue] into an array
    repeat until all the partitions are processed


"""

import tsfel
import pandas as pd

data = tsfel.datasets.load_biopluxecg()    # A single-lead ECG collected during 10 s at 100 Hz.