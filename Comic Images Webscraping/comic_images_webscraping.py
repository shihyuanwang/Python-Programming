# HW7 - Comic Images Web Scraping- SHIH-YUAN WANG

# Write a python program that will download the latest 10 comic images from https://www.gocomics.com/pearlsbeforeswine/

#----------------------------------------------------------------------------------------------

import os
import requests
from bs4 import BeautifulSoup

# change current working directory
# os.chdir('/Users/ginawang/Desktop/Python Programming I/homework-7-shihyuanwang')
# print(os.getcwd())

url = 'https://www.gocomics.com/pearlsbeforeswine/'

# Download website URL
res = requests.get(url)
res.raise_for_status()  # check for errors

# Pass it into the BeautifulSoup to parse the webpage
soup = BeautifulSoup(res.text, "lxml")
# print(soup.prettify())

# Navigate to the latest pearlsbeforeswine page through tag
comic_link = soup.select('a[data-link="comics"]')[0]
# print(comic_link)  # <a class="nav-link" data-link="comics" href="/pearlsbeforeswine/2019/08/20">Comics</a>
# print(comic_link.get('href')) # /pearlsbeforeswine/2019/08/20
comic_url = 'https://www.gocomics.com' + comic_link.get('href')
# print(comic_url)  # https://www.gocomics.com/pearlsbeforeswine/2019/08/20


for i in range(10):
    # Download the comic webpage
    comic_res = requests.get(comic_url)
    comic_res.raise_for_status()  # check for errors

    # Pass it into the BeautifulSoup to parse the webpage
    comic_soup = BeautifulSoup(comic_res.text, "lxml")
    # print(latest_soup.prettify())

    # Find the image url of the current day
    image = comic_soup.select('a[itemprop="image"]')
    image_url = image[0].img.attrs['src'] + '.png'
    # print(image_url)

    # Download this image
    print('Downloading image %s...' % (image_url))
    image_res = requests.get(image_url)
    image_res.raise_for_status()
    
    # Save this image
    image_file = open(os.path.basename(image_url), 'wb')
    for chunk in image_res.iter_content(100000):
        if chunk:
            image_file.write(chunk)
    image_file.close()

    print("Image downloaded! Time: " + str(i+1))

    #-------------------------------------

    # Extract the link to the previous image
    prev_link = comic_soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-left sm js-previous-comic"]')[0]
    # print(prev_link)

    # Get the previous image url and assign to comic_url variable for next loop
    comic_url = 'https://www.gocomics.com' + prev_link.get('href')
    # print(comic_url)  # https://www.gocomics.com/pearlsbeforeswine/2019/08/19






