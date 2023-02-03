# Program that can be used to find local movies showtimes using your zipcode

# import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_experimental_option('detach', True)

# User prompt asking to enter zipcode
print('Would you like to see what movies are currently showing in your area?')
zipcode = input(str("Please type your zipcode & press 'enter': "))


# use your own file path where ever you have your webdriver installed
# I used chrome as you can see ('chromedriver.exe')
driver = webdriver.Chrome('C:\Program Files (x86)\Selenium\chromedriver.exe',
options = options)
# Inject user's zipcode into url
driver.get(f'https://www.fandango.com/{zipcode}_movietimes')

# Define soup variable for BeautifulSoup find functions
soup = BeautifulSoup(driver.page_source, 'lxml')

# Create dataframe to append data to
df = pd.DataFrame(columns = ['Title', 'Rating', 'Runtime',
'Genre(s)', 'Showtimes', 'Link'])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# This purpose of this part was to try and match the movies to the theater they
# were being played at, but I was unsuccessful. If anyone can figure it out,
# please let me know. I was trying to a counter, iterate through
# official_theater_list, and maybe use another for loop or if statement
# somewhere. But I'm not sure.

# all_theaters = soup.find_all('li', class_ = 'fd-theater')
# theater_list = []
# for theater in all_theaters:
#     theater_name = theater.find('a', class_ = 'light').text.strip()
#     theater_list.append(theater_name)
# official_theater_list = theater_list[1:]
# number_of_theaters = len(official_theater_list)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Find all the movie listing on the webpage
all_movies = soup.find_all('li', class_ = 'fd-movie')

# Iterate through all the info within 'all_movies' & sort them into their
# respective columns in the dataframe
for movie in all_movies:
    try:
        viewings = []
        info2 = []
        title = movie.find('h3', class_ = 'dark fd-movie__title font-sans-serif font-lg font-300 uppercase').text
        info = movie.find('p', class_ = 'fd-movie__rating-runtime').text.strip().split('\n')
        for i in info:
            x = i.strip()
            if len(x) > 2:
                info2.append(x)
        rating = info2[0][7:-1]
        if len(info2) > 2:
            runtime = info2[1][9:]
            genre = info2[2]
        else:
            runtime = ''
            genre = info2[1]
        showtimes = movie.find_all('li', class_ = 'fd-movie__btn-list-item')
        for showtime in showtimes:
            viewings.append(showtime.text.strip())
        link = movie.find('a', class_ = 'fd-movie__link').get('href')
        full_link = 'https://www.fandango.com/' + link
        df = df.append({'Title':title, 'Rating':rating,
        'Runtime':runtime, 'Genre(s)':genre, 'Showtimes':viewings,
        'Link':full_link}, ignore_index = True)
    except:
        pass

# Convert dataframe into csv file to view more easily and click on links
# You can choose your own file path/location depending on where you want to
# save the csv.
df.to_csv('D:\Data Analytics\Movies.csv')
