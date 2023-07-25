import csv
import random

header = ['Latitude', 'Longitude']


with open('sample.csv', 'w') as f:

    writer = csv.writer(f)

    writer.writerow(header) # write the header to the file first

    for i in range(10): # generate 10 rows of data with random latitude and longitude values between 40 and 50, rounded up to 3 decimal places each time.

        lat = round(random.uniform(40,50),3) # use uniform method from random library to get a float value between 40 and 50, then roundit up to 3 decimal places.
        lon = round(random.uniform(40,50),3) # same as above for longitude

        writer.writerow([lat,lon]) # write the latitude and longitude values in each row of the file