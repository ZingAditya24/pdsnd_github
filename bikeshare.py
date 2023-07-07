import time
import pandas as pd
import numpy as np

#Create a dictioary CITY_DATA which holds path to the .csv files

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_raw_data(df):
    """
    Returns the records from the dataset if requested by user:
    """
    # Display raw data upon user request
    display_raw_data = input("\n\nWould you like to see the raw data? Enter 'yes' or 'no': ")
    display_raw_data = display_raw_data.lower()
    if display_raw_data == 'yes':
        print("\nRaw Data:")

        # Show data in batches of 5 records
        batch_size = 5
        current_index = 0
        total_records = len(df)

        while current_index < total_records:
            print("\n\nShowing {}-{} of {} records".format(current_index+1, current_index+batch_size, total_records))
            print(df.iloc[current_index:current_index+batch_size])
            current_index += batch_size

            if current_index < total_records:
                show_next_batch = input("\n\nWould you like to see the next batch? Enter 'yes' or 'no': ")
                show_next_batch = show_next_batch.lower()
                if show_next_batch != 'yes':
                    break

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nEnter the name of the city to analyze (chicago, new york city, washington): ")
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("\nInvalid input. Please enter a valid city name.")
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nEnter the month to filter by (january, february, ..., june) or 'all' for no month filter: ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("\nInvalid input. Please enter a valid month or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nEnter the day of the week to filter by (monday, tuesday, ..., sunday) or 'all' for no day filter: ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("\nInvalid input. Please enter a valid day or 'all'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'chicago':
        input_file = CITY_DATA['chicago']
    elif city == 'new york city':
        input_file = CITY_DATA['new york city']
    elif city == 'washington':
        input_file = CITY_DATA['washington']
    else:
        return None
    
    df = pd.read_csv(input_file)

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of week from the 'Start Time' column to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # Apply filters based on the month and day inputs
    if month != 'all':
        # Convert month name to month number (e.g., 'January' -> 1)
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filter by month
        df = df[df['Month'] == month]

    if day != 'all':
        # Filter by day of week
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['Start Time'].dt.month.mode()[0]
    print(f"\nMost Common Month: {common_month}")

    # Display the most common day of week
    common_day = df['Start Time'].dt.day_name().mode()[0]
    print(f"\nMost Common Day of Week: {common_day}")

    # Display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print(f"\nMost Common Start Hour: {common_hour}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print(f"\nMost commonly used start station: {common_start_station}")

    # Display the most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print(f"\nMost commonly used end station: {common_end_station}")

    # Display the most frequent combination of start station and end station trip
    start_end_combinations = df.groupby(['Start Station', 'End Station']).size()
    most_frequent_combination = start_end_combinations.idxmax()
    print(f"\nMost frequent combination of start station and end station: {most_frequent_combination[0]}, {most_frequent_combination[1]}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total travel time (in sec):", total_travel_time)

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("\nMean travel time (in sec):", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:")
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        print(gender_counts)
    else:
        print("\nGender information is not available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest Birth Year:", int(earliest_birth_year))
        print("\nMost Recent Birth Year:", int(most_recent_birth_year))
        print("\nMost Common Birth Year:", int(most_common_birth_year))
    else:
        print("\nBirth year information is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def main():
    """
    The main function of the bikeshare data analysis script.
    It serves as the entry point for the program and controls the flow of execution.

    The function repeatedly prompts the user for city, month, and day filters, and then performs the following steps:
    1. Calls the `get_filters()` function to get user input for city, month, and day.
    2. Calls the `load_data()` function to load and filter the bikeshare data based on the user's input.
    3. Calls the `get_raw_data()` function to display the raw data if requested by the user.
    4. Calls the `time_stats()`, `station_stats()`, `trip_duration_stats()`, and `user_stats()` functions to calculate and display various statistics on the bikeshare data.
    5. Asks the user if they want to restart the program or exit.

    Returns:
        None
    """
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        
        get_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
    
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
