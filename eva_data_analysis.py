import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva-data.csv', 'w', encoding='utf-8')
graph_file = './cumulative_eva_graph.png'

def read_json_to_dataframe(input_file):
    """
    Read the data from a JSON file into a pandas dataframe
    Clean the data by removing any rows where the duration is missing

    Args:
        input_file (file or stre): The file object or the path to the JSON file

    Returns:
        eva_df (pd.DataFrame): The cleaned data as a dataframe structure.
    """
    print(f"Reading JSON file {input_file}")

    # Read the data from JSON file into a pandas dataframe
    #eva stands for extra vehicular activity
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')

    # Convert integers to float in the eva column
    eva_df['eva'] = eva_df['eva'].astype(np.float32)

    # Drop any nan values in the duration and date columns, focusing on the row (axis=0)
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)

    return eva_df

def  write_dataframe_to_csv(df, output_file):
    """Write the pandas data frame df to a csv file

    Args:
        df (dataframe): The dataframe structure to be saved as a CSV
        output_file (csv): A .csv file
    """
    print(f"Saving the CSV file {output_file}")

    # save the dataframe to CSV file for data analysis
    df.to_csv(output_file, index=False, encoding='utf-8')



def plot_cumulative_time_in_space(df, graph_file):
    """
    Plot the cumulative time in space over years
    Convert the duration column from strings to number of hours
    Calculate cumulative sum of durations
    Generate a plot of cummulative

    Args:
        df (dataframe): The dateframe data
        graph_file (file or stre): The path where the final plot should be saved
    """
    # Sort the dates from old - new dates. inplace=True to override the exisiting eva_df
    df.sort_values('date', inplace=True)

    # convert the duration  column to minutes:hours
    df['duration_hours'] = df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)

    # A cumulative sum of all the duration hours
    df['cumulative_time'] = df['duration_hours'].cumsum()

    # Plot date and the cumulative_time
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file}')
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    # label xaxis
    plt.xlabel('Year')
    # label yaxis
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()



print("--START--")

# Read the data from JSON file
eva_data = read_json_to_dataframe(input_file)

# Convert and export data to the CSV file
write_dataframe_to_csv(eva_data, output_file)

plot_cumulative_time_in_space(eva_data, graph_file)

print("--END--")