import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City, or Washington?\n")
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        city = input("No data for {}. Please choose from (Chicago, New York City, Washington).\n".format(city))

    # Get what filter(s) users want to use
    # Set default option as no filter
    month = 'all'
    day = 'all'

    # Get user input
    filter_flag = input("Would you like to filter the data by (1)month; (2)day; (3)both; (4)not at all? "
                        "Please enter the option number.\n")
    while filter_flag not in ['1', '2', '3', '4']:
        filter_flag = input("Wrong option! Please select from (1, 2, 3, 4).\n")

    if filter_flag in ['1', '3']:
        # TO DO: get user input for month (all, january, february, ... , june)
        month = input("Which month you would like to check, January, February, ... , June OR all?\n")
        while month.lower() not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            month = input("No data for {}. Please choose from (January, February, ... , June, all).\n".format(month))

    if filter_flag in ['2', '3']:
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day of week you would like to check, Monday, Tuesday, ... Sunday OR all?\n")
        while day.lower() not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input("No data for {}. Please choose from (Monday, Tuesday, ... Sunday, all).\n".format(day))

    print('You are going to check the data for: ')
    print('CITY: {}'.format(city))
    print('MONTH: {}'.format(month))
    print('DAY_OF_WEEK: {}'.format(day))
    print('-' * 40)
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

    # Preprocess the input
    city = city.lower()
    month = month.lower()
    day = day.title()

    # load data file into a dataframe
    data_file_name = CITY_DATA.get(city.lower(), None)
    # Return None if no data found.
    if data_file_name is None:
        print("No data for {}.".format(city))
        return None

    bike_data_df = pd.read_csv(data_file_name)

    # convert the Start Time column to datetime
    bike_data_df['Start Time'] = pd.to_datetime(bike_data_df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    bike_data_df['month'] = bike_data_df['Start Time'].dt.month
    bike_data_df['day_of_week'] = bike_data_df['Start Time'].dt.day_name()
    bike_data_df['hour'] = bike_data_df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months_name_lst = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months_name_lst.index(month) + 1

        # filter by month to create the new dataframe
        bike_data_df = bike_data_df.loc[bike_data_df['month'] == month_index]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        bike_data_df = bike_data_df.loc[bike_data_df['day_of_week'] == day]

    # Export filtered data for debug
    # bike_data_df.to_csv("temp.csv")

    return bike_data_df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_cnt = df['month'].value_counts()[popular_month]
    total_month_cnt = df['month'].count()
    popular_month_pct = popular_month_cnt / total_month_cnt * 100
    print("Most Common Month: {0}. COUNTS: {1}/{2}. That is {3:.2f}% of all records.\n".format(popular_month,
                                                                                               popular_month_cnt,
                                                                                               total_month_cnt,
                                                                                               popular_month_pct))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day_cnt = df['day_of_week'].value_counts()[popular_day]
    total_day_cnt = df['day_of_week'].count()
    popular_day_pct = popular_day_cnt / total_day_cnt * 100
    print("Most Common Day of Week: {0}. COUNTS: {1}/{2}. That is {3:.2f}% of all records.\n".format(popular_day,
                                                                                                     popular_day_cnt,
                                                                                                     total_day_cnt,
                                                                                                     popular_day_pct))

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_cnt = df['hour'].value_counts()[popular_hour]
    total_hour_cnt = df['hour'].count()
    popular_hour_pct = popular_hour_cnt / total_hour_cnt * 100
    print("Most Common Hour: {0}. COUNTS: {1}/{2}. That is {3:.1f}% of all records.\n".format(popular_hour,
                                                                                              popular_hour_cnt,
                                                                                              total_hour_cnt,
                                                                                              popular_hour_pct))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_cnt = df['Start Station'].value_counts()[popular_start_station]
    total_start_station_cnt = df['Start Station'].count()
    popular_start_station_pct = popular_start_station_cnt / total_start_station_cnt * 100
    print("Most commonly used start station: {0}. COUNTS: {1}/{2}. "
          "That is {3:.2f}% of all records.\n".format(popular_start_station,
                                                      popular_start_station_cnt,
                                                      total_start_station_cnt,
                                                      popular_start_station_pct))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_cnt = df['End Station'].value_counts()[popular_end_station]
    total_end_station_cnt = df['End Station'].count()
    popular_end_station_pct = popular_end_station_cnt / total_end_station_cnt * 100
    print("Most commonly used end station: {0}. COUNTS: {1}/{2}. "
          "That is {3:.2f}% of all records.\n".format(popular_end_station,
                                                      popular_end_station_cnt,
                                                      total_end_station_cnt,
                                                      popular_end_station_pct))

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip_cnt_df = df.groupby(['Start Station', 'End Station'])['Trip Duration'].count()
    popular_trip = popular_trip_cnt_df.idxmax()
    popular_trip_cnt = popular_trip_cnt_df.max()
    total_popular_trip_cnt = popular_trip_cnt_df.sum()
    popular_trip_pct = popular_trip_cnt / total_popular_trip_cnt * 100
    print("Most popular trip is:")
    print("FROM...{0}...TO...{1}.    \nCOUNTS: {2}/{3}. That is {4:.2f}% of all records.".format(popular_trip[0],
                                                                                                 popular_trip[1],
                                                                                                 popular_trip_cnt,
                                                                                                 total_popular_trip_cnt,
                                                                                                 popular_trip_pct))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print("Total travel time is {}".format(total_trip_duration))

    # TO DO: display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print("Mean travel time is {}".format(mean_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    df['User Type'].fillna('Unknown', inplace=True)  # Fill NaN with 'Unknown'
    print("User Type Counts:")
    user_type_ser = df['User Type'].value_counts()
    for user_type_str in user_type_ser.index:
        print("{}:\t\t{}".format(user_type_str, user_type_ser[user_type_str]))

    # User statistics only available for NYC and Chicago
    if city.lower() != 'washington':
        # TO DO: Display counts of gender
        df['Gender'].fillna('Unknown', inplace=True)  # Fill NaN with 'Unknown'
        print("\nUser Gender Counts:")
        user_gender_ser = df['Gender'].value_counts()
        for user_gender_str in user_gender_ser.index:
            print("{}:\t\t{}".format(user_gender_str, user_gender_ser[user_gender_str]))

        # TO DO: Display earliest, most recent, and most common year of birth
        user_yob_min = int(df['Birth Year'].min())
        user_yob_max = int(df['Birth Year'].max())
        user_yob_common = int(df['Birth Year'].mode()[0])
        print("\nUser Birth Year Info:")
        print("Earliest:\t\t{}".format(user_yob_min))
        print("Most Recent:\t\t{}".format(user_yob_max))
        print("Most Common:\t\t{}".format(user_yob_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data_display(df):

    # Get user's answer whether they would like to see the raw data
    ans = input("Would you like to see the raw data (filtered)? (yes/no)")
    while ans not in ['yes', 'no']:
        ans = input("Invalid answer! Please enter 'yes' or 'no'.")

    # Init print status
    total_row_num = df.shape[0]
    display_cnt = 0
    display_step = 5

    # Print only when user want to and it doesn't reach the end of the data
    while 'yes' == ans:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df.iloc[display_cnt * display_step:(display_cnt + 1) * display_step])

        # Update display count
        display_cnt += 1

        # Check if reach the end of the data
        if (display_cnt * display_step) >= total_row_num:
            print("End of the data.")
            break

        # Check if they would like to see 5 more rows
        ans = input("would like to see 5 more rows of the data? (yes/no)")
        while ans not in ['yes', 'no']:
            ans = input("Invalid answer! Please enter 'yes' or 'no'.")

    print("Data Display Stopped.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df is not None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            raw_data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
