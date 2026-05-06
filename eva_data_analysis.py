import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva-data.csv', 'w', encoding='utf-8')
graph_file = './cumulative_eva_graph.png'


print("--START--")
print(f"Reading JSON file {input_file}")

# Read the data from JSON file into a pandas dataframe
#eva stands for extra vehicular activity
eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')

# Convert integers to float in the eva column
eva_df['eva'] = eva_df['eva'].astype(np.float32)

# Drop any nan values in the duration and date columns, focusing on the row (axis=0)
eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)

print(f"Saving the CSV file {output_file}")

# save the dataframe to CSV file for data analysis
eva_df.to_csv(output_file, index=False, encoding='utf-8')

# Sort the dates from old - new dates. inplace=True to override the exisiting eva_df
eva_df.sort_values('date', inplace=True)

# convert the duration  column to minutes:hours
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)

# A cumulative sum of all the duration hours
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

# Plot date and the cumulative_time
print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')
# label xaxis
plt.xlabel('Year')
# label yaxis
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
print("--END--")