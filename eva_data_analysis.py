import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import re


# Data source: https://data.nasa.gov/resource/eva.json (with modifications)


def main(input_file, output_file, graph_file):
    print("--START--")

    # Read the data from JSON file
    eva_data = read_json_to_dataframe(input_file)

    # Calculate and add crew size to data
    eva_data = add_crew_size_column(eva_data) # added this line

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Sort dataframe by date ready to be plotted (date values are on x-axis)
    eva_data.sort_values('date', inplace=True)

    # Plot cumulative time spent in space over years
    plot_cumulative_time_in_space(eva_data, graph_file)

    print("--END--")


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
    df = add_duration_hours(df)

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


def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
        duration (str): The text format duration

    Returns:
        duration_hours (float): The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60  # there is an intentional bug on this line (should divide by 60 not 6)
    return duration_hours


def add_duration_hours(df):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        df_copy (pd.DataFrame): A copy of df with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy


def calculate_crew_size(crew):
    """
    Calculate the size of the crew for a single crew entry

    Args:
        crew (str): The text entry in the crew column containing a list of crew member names

    Returns:
        (int): The crew size
    """
    if crew.split() == []:
        return None
    else:
        return len(re.split(r';', crew))-1


def add_crew_size_column(df):
    """
    Add crew_size column to the dataset containing the value of the crew size

    Args:
        df (pd.DataFrame): The input data frame.

    Returns:
        df_copy (pd.DataFrame): A copy of the dataframe df with the new crew_size variable added
    """
    print('Adding crew size variable (crew_size) to dataset')
    df_copy = df.copy()
    df_copy["crew_size"] = df_copy["crew"].apply(
        calculate_crew_size
    )
    return df_copy


if __name__ == "__main__":

    if len(sys.argv) < 3:

        input_file = open('./Data/eva-data.json', 'r', encoding='ascii')
        output_file = open('./results/eva-data.csv', 'w', encoding='utf-8')
        print('Using default input and output filenames')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print('Using custom inputand output filenames.')
    
    graph_file = './results/cumulative_eva_graph.png'
    main(input_file, output_file, graph_file)




