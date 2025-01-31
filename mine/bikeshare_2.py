import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
			  'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months=('january','february','march','april','may','june')
days=('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')
def getMonth():
	month=[]
	i=0
	ch=''
	ch=input('whould you like to filter by all months? enter "y" for yes and "n" for no ')
	if ch.lower()=='y':
		month.append('all')
	else:
		while(i<6 and ch!='e'):
			ch=input('whould you like to filter by the month: {}? enter "y" for yes and "n" for no and "e" for escape '.format(months[i]))
			ch= ch.lower()
			match ch:
				case 'y':
					month.append(months[i])
					i+=1
				case 'n':
					i+=1
				case 'e':
					continue
				case _:
					print('INVALID CHOICE!\n')
	if not month:
		month.append('all')
	return month
def getDay():
	day=[]
	i=0
	ch=''
	ch=input('whould you like to filter by all days? enter "y" for yes and "n" for no ')
	if ch.lower()=='y':
		day.append('all')
	else:
		while(i<7 and ch!='e'):#filter by more than one day
			ch=input('whould you like to filter by the day: {}? enter "y" for yes and "n" for no and "e" for escape '.format(days[i]))
			ch= ch.lower()
			match ch:
				case 'y':
					day.append(days[i])
					i+=1
				case 'n':
					i+=1
				case 'e':
					continue
				case _:
					print('INVALID CHOICE!\n')
	if not day:
		day.append('all')
	return day
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
	city=''
	day=[]
	month=[]
	while(city not in CITY_DATA):
		city=input('would you like to see data for Chicago, New York,or Washington? ').lower()
	month=getMonth()
    # get user input for month (all, january, february, ... , june)
	day=getDay()
    # get user input for day of week (all, monday, tuesday, ... sunday)
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
	
	df=pd.read_csv(CITY_DATA.get(city))
	df['Start Time']=pd.to_datetime(df['Start Time'])
	df['month']=df['Start Time'].dt.month#ok
	df['day_of_week']=df['Start Time'].dt.day_name()
	if month[0]!='all' :
		for i in range(len(month)):
			month[i]=months.index(month[i]) + 1
		df=df[df['month'].isin(month)]
	if day[0]!='all':
		df=df[df['day_of_week'].isin(day)]#if the day is in the days of the week add it to the day_of_week column
	return df


def time_stats(df):
	"""Displays statistics on the most frequent times of travel."""

	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()

    # display the most common month
	common_month=df['month'].mode()[0]
	print('The most common month is ',months[common_month-1],'\n')
	
    # display the most common day of week
	common_day=df['day_of_week'].mode()[0]
	print('The most common day is ',common_day,'\n')

    # display the most common start hour
	df['hour']=df['Start Time'].dt.hour
	common_start_hour=df['hour'].mode()[0]
	print('The most common start hour is ',common_start_hour,'\n')

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""

	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()

    # display most commonly used start station
	CSstation=df['Start Station'].mode()[0]
	print('The most commonly used start station is ',CSstation,'\n')

    # display most commonly used end station
	ESstation=df['End Station'].mode()[0]
	print('The most commonly used end station is ',ESstation,'\n')

    # display most frequent combination of start station and end station trip
	popular_combination='From '+(df['Start Station']+ ' To '+df['End Station']).mode()[0]
	print('The most popular combination of start station and end station trip is ',popular_combination,'\n')
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""

	print('\nCalculating Trip Duration...\n')
	start_time = time.time()

    # display total travel time
	total=df['Trip Duration'].sum()
	print('The total trip duration is ',total,'seconds\n')


    # display mean travel time
	avg=df['Trip Duration'].mean()
	print('The average trip duration is ',avg,'seconds\n')


	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def user_stats(df):
	"""Displays statistics on bikeshare users."""

	print('\nCalculating User Stats...\n')
	start_time = time.time()

    # Display counts of user types
	print('***Counts of user types***\n')
	user_types = df['User Type'].value_counts()
	print(user_types,'\n')

    # Display counts of gender
	if 'Gender' in df.columns:
		print('***Counts of gender***\n')
		cgen=df['Gender'].value_counts()
		print(cgen)
		earliest=df['Birth Year'].min()
		Mrecent=df['Birth Year'].max()
		Mcommon=df['Birth Year'].mode()[0]
		print(' The earliest year of birth is: ',earliest,'\nThe most recent year of birth is: ',Mrecent,'\nThe most common year of birth is: ',Mcommon,'\n')

    # Display earliest, most recent, and most common year of birth


	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)
def display_data(df):
	c=input('Would you like to see the raw data? please enter yes or no ').lower()
	if c=='no':
		return
	else:
		i=0	
		while(c!='no' and i<len(df)):
			print(df.iloc[i:i+5])
			i+=5
			c=input('Would you like to see more data? please enter yes or no ').lower()

def main():
	while True:
		city, month, day = get_filters()
		df = load_data(city, month, day)
		if df.empty:
			print ('empty3')
		time_stats(df)
		station_stats(df)
		trip_duration_stats(df)
		user_stats(df)
		display_data(df)
		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break


if __name__ == "__main__":
	main()
