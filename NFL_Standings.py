# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Ask user what year they would like to analyze
user_response = input("""This program is used to web scrape information
regarding the regular season standings of NFL Teams between the years of
2000 - 2022 an converts that information into a 'csv' file. Please type a
year you would like to analyze and press enter: """)

# Make sure they enter a valid year
acceptable_responses = ['2000', '2001', '2002', '2003', '2004', '2005', '2006',
'2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
'2017', '2018', '2019', '2020', '2021', '2022']

if user_response not in acceptable_responses:
    print('')
    user_response = input("""Sorry that was not a valid year. Please try again: """)

# Ask user where they would like to save the 'csv' file
print('')
file_location = input(r"""Now enter a valid file location you would like to store
the 'csv' file on your computer (Ex: C:\My Folder\NFL_Standings.csv). Feel
free to name the file what ever you want: """)

# Make initial page request & create 'soup' variable
url = f'https://www.nfl.com/standings/league/{user_response}/REG'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# Create dataframe template
df = pd.DataFrame(columns = ['Regular Season', 'NFL Team', 'Total Wins',
'Total Losses', 'Total Ties', 'Total Record Percentage', 'Home Wins',
'Home Losses', 'Home Ties', 'Away Wins', 'Away Losses', 'Away Ties',
'Conference Wins', 'Conference Losses', 'Conference Ties',
'Conference Record Percentage'])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Creating and cleaning up a list of all the team names
team_list = []
team_list_v2 = []
team_list_v3 = []
team_list_final = []
all_teams = soup.find_all('div', class_ = 'd3-o-club-fullname')
for i in all_teams:
    team_list.append(i.text)

for i in team_list:
    team_names_v1 = i.replace('xyz','')
    team_list_v2.append(team_names_v1)

for i in team_list_v2:
    team_names_v2 = i.replace('xy', '')
    team_list_v3.append(team_names_v2)

for i in team_list_v3:
    team_names_v3 = i.replace('xz', '')
    team_list_final.append(team_names_v3.strip())
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Putting the rest of the data that we want into lists
# There is more data on the table/website than we care about...so have to do
# some slicing.
# Everything is printed as text, so need to convert to numbers
# This part will deal with the columns that are just a single number.
data = []
table = soup.find_all('td')
for i in table:
    data.append(i.text)

def convert_to_int(list_1, list_2, start):
    global data
    list_1.append(data[start::17])
    for i in list_1:
        try:
            for x in i:
                list_2.append(int(x))
        except:
            for x in i:
                list_2.append(float(x))
    return list_2

total_wins = []
total_wins_v2 = [] # add to dataframe
total_losses = []
total_losses_v2 = [] # add to dataframe
total_ties = []
total_ties_v2 = [] # add to dataframe
total_pct = []
total_pct_v2 = [] # add to dataframe
conference_pct = []
conference_pct_v2 = [] # add to dataframe
convert_to_int(total_wins, total_wins_v2, 1)
convert_to_int(total_losses, total_losses_v2, 2)
convert_to_int(total_ties, total_ties_v2, 3)
convert_to_int(total_pct, total_pct_v2, 4)
convert_to_int(conference_pct, conference_pct_v2, 13)

# This part will deal with the columns that display the team records as a whole
# Ex: '5-3-0'...5 wins, 3 losses, 0 ties
home_record = data[8::17]
home_record_v2 = []
home_wins = [] # add to dataframe
home_losses = [] # add to dataframe
home_ties = [] # add to dataframe

away_record = data[9::17]
away_record_v2 = []
away_wins = [] # add to dataframe
away_losses = [] # add to dataframe
away_ties = [] # add to dataframe

conference_record = data[12::17]
conference_record_v2 = []
conference_wins = [] # add to dataframe
conference_losses = [] # add to dataframe
conference_ties = [] # add to dataframe

def records(list_1, list_2, list_3, list_4, list_5):
    for i in list_1:
        list_2.append(i.split('-'))
    for i in list_2:
        list_3.append(int(i[0]))
        list_4.append(int(i[1]))
        list_5.append(int(i[2]))
    return list_3, list_4, list_5

records(home_record, home_record_v2, home_wins, home_losses, home_ties)
records(away_record, away_record_v2, away_wins, away_losses, away_ties)
records(conference_record, conference_record_v2, conference_wins,
conference_losses, conference_ties)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Make a column to indicate the season the user has chosen. Can come in handy if
# user decides to analyze multiple seasons by merging multiple csv file
# together.
regular_season = []
for i in range(32):
    i = int(user_response)
    regular_season.append(i)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Assign lists to their appropriate columns.

df['NFL Team'] = team_list_final
df['Regular Season'] = regular_season
df['Total Wins'] = total_wins_v2
df['Total Losses'] = total_losses_v2
df['Total Ties'] = total_ties_v2
df['Total Record Percentage'] = total_pct_v2
df['Home Wins'] = home_wins
df['Home Losses'] = home_losses
df['Home Ties'] = home_ties
df['Away Wins'] = away_wins
df['Away Losses'] = away_losses
df['Away Ties'] = away_ties
df['Conference Wins'] = conference_wins
df['Conference Losses'] = conference_losses
df['Conference Ties'] = conference_ties
df['Conference Record Percentage'] = conference_pct_v2

# Convert dataframe to csv file and save in location the user specified.
df.to_csv(rf'{file_location}')
