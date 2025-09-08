import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Read the Polars DataFrame from a Parquet file
df = pl.read_parquet("cleaned_shelter_usage.parquet")

# Convert the date column to datetime and rename it for clarity
df = df.with_columns(pl.col("date").str.strptime(pl.Date, "%Y-%m-%d").alias("date"))

# Group by "Dates" and calculate total "Capacity" and "Usage"
aggregated_df = (
    df.group_by("date")
    .agg([
        pl.col("Capacity").sum().alias("Total_Capacity"),
        pl.col("Usage").sum().alias("Total_Usage")
    ])
    .sort("date")  # Sort the results by date
)


# Ensure the 'date' column is of datetime type in Polars
df = df.with_columns([
    pl.col('date').cast(pl.Date)
])

# Select the relevant columns and reshape the DataFrame
df_melted = df.select(["date", "Total_Capacity", "Total_Usage"]).melt(
    id_vars="date",
    variable_name="Metric",
    value_name="Value"
)

# Convert Polars DataFrame to a Pandas DataFrame for Seaborn
df_melted_pd = df_melted.to_pandas()

# Ensure 'date' column is datetime in Pandas
df_melted_pd['date'] = pd.to_datetime(df_melted_pd['date'])

# Set the plotting style
sns.set_theme(style="whitegrid")

# Create the plot
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_melted_pd,
    x="date",
    y="Value",
    hue="Metric",
    linewidth=2.5
)

# Format the x-axis to show dates nicely
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add labels and title
plt.xlabel("Date")
plt.ylabel("Values")
plt.title("Total Capacity and Usage Over Time")

# Adjust layout to prevent clipping of tick-labels
plt.tight_layout()

# Display the plot
plt.show()