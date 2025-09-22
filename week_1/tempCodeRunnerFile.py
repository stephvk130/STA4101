import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Read the Polars DataFrame from a Parquet file
df = pl.read_parquet("cleaned_shelter_usage.parquet")