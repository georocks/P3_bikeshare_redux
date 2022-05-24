import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter your city: ").lower()
        if city in cities:
            break
        else:
            print("Invalid entry. Please enter Chicago, New York City or Washington.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter a month (January to June) or 'all' to apply no month filter: ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month in months:
            break
        else:
            print("Invalid entry. Please enter a valid month (January through June) or select 'all' to apply no month filter: ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter a day of the week or 'all' to apply no day filter: ").lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        if day in days:
            break
        else:
            print("Please select a day or 'all' to apply no day filter: ")
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to to_datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new column
    df['Month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # extract day of week from Start Time to create new column
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month for travel is ", df['Month'].mode()[0], "\n")

    # display the most common day of week
    print("The most common day for travel is ", df['Day of Week'].mode()[0], "\n")

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print("Most riders start their ride at ", df['Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['paired'] = df['Start Station'] +  " and " + df['End Station']
    print("The most commonly paired start and end stations are ", df['paired'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time in hours is ", df['Trip Duration'].sum() / 3600, "\n")

    # display mean travel time
    print("The average trip time in hours is ", df['Trip Duration'].mean() / 3600, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Displaying user types:")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city != 'washington':
        print('Gender:')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
        print('Birth Year Trends: ')

        youngest_rider = df['Birth Year'].max()
        print('The most recent birth year of a rider was ', youngest_rider)

        oldest_rider = df['Birth Year'].min()
        print('The earliest birth year of a rider was ', oldest_rider)

        birth_year_mode = df['Birth Year'].mode()[0]
        print('The most common birth year is ', birth_year_mode)

    # Allow user to view raw data upon request
    origin = 0
    while(True):
        view_data = input("Do you want to view 5 lines of raw data? Please enter yes or no: ").lower()
        if view_data == 'yes':
            print(df[origin:origin+5])
            origin += 5
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
