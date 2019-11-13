# This program will scrape the 7-day forecast of the weather for Boston
import requests
from bs4 import BeautifulSoup

# Make request to web page
page = requests.get("https://weather.com/weather/today/l/d7f5a4af529e40b0a82d339e5467e89458e5ad5e2cf0ffdd05c853ed3e98fd38")

# Create soup object to parse web page
soup = BeautifulSoup(page.content, 'html.parser')

# Find id tag on the HTML block I need
look_ahead = soup.find(id="main-LookingAhead-b39982dc-b828-42f9-9ca4-3d6686c1bb83")
# print(look_ahead)

# Need to id all elements with class = looking-ahead
forecast_items = look_ahead.find(class_="looking-ahead")
# print(forecast_items)

# Get the content from that class, and dig deeper to find where the content is hidden
# in class = looking-ahead; class = today-daypart-content,
content = forecast_items.find(class_="today-daypart-content")
print(content)

period = content.find(class_="today-daypart-title").get_text()
short_desc = content.find(class_="today-daypart-wxphrase").get_text()
hi_low = content.find(class_="today-daypart-hilo").get_text()
temp = content.find(class_="today-daypart-temp").get_text()
precip = content.find(class_="today-daypart-precip").get_text()

# print(period) # Today
# print(short_desc)
# print(hi_low)
# print(temp)
# print(precip)
#
# print(f"In Hyderabad {period}, the weather looks like this: ")
# print(f"Conditions: {short_desc}")
# print(f"High/Low: {hi_low}")
# print(f"Temp: {temp}")
# print(f"Chance of rain: {precip}")


# Pull the information for the rest of the periods
periods = forecast_items.select(".today-daypart-content .today-daypart-title")

period_names = [item.get_text() for item in periods]
short_descs = [item.get_text() for item in forecast_items.select(".today-daypart-content .today-daypart-wxphrase")]
hi_lows = [item.get_text() for item in forecast_items.select(".today-daypart-content .today-daypart-hilo")]
temps = [item.get_text() for item in forecast_items.select(".today-daypart-content .today-daypart-temp")]
precips = [item.get_text() for item in forecast_items.select(".today-daypart-content .today-daypart-precip")]

print(period_names)
print(short_descs)
print(hi_lows)
print(temps)
print(precips)

# Import into pandas DF
import pandas as pd
weather = pd.DataFrame({
    "Period": period_names,
    "Short_Desc": short_descs,
    "High/Low" : hi_lows,
    "Temp": temps,
    "Chance of rain" : precips
})

print(weather)

# Do some analysis on the data.
#
# Find the mean temp
temp_nums = weather["Temp"].str.extract("(?P<temp_num>\d+)", expand=False)
# Create a new column called "Temp num, that only has the number
weather["Temp num"] = temp_nums.astype('int')
mean_temp = weather["Temp num"].mean()

print(temp_nums)
print(weather)
print("Mean Temp: ", mean_temp)

# Find the ones that happen at night
is_night = weather["High/Low"].str.contains("Low")
weather["is_night"] = is_night
print(weather)