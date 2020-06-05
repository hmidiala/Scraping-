import requests
import numpy as np
from bs4 import BeautifulSoup
import csv
import lxml
# Lists to store the scraped data in
titles = []
reviews = []
prices = []
nbrofreviews = []
unifiedprices = []

# Scraping all pages
pages_url = requests.get('https://www.amazon.fr')

pages_soup = BeautifulSoup(pages_url.text,'html.parser')

#list_nums = pages_soup.find('div').text

#print(list_nums)
name = input("Enter a name: ")
print(name)
pages = [str(i) for i in range(1,20)]

for page in pages:
    
    response = requests.get('https://www.amazon.fr/s?k='+name).text
    
    html_soup = BeautifulSoup(response, 'lxml')

    # Extract data from individual listing containers
    listing_containers = html_soup.find_all('div',class_="sg-col-inner")
    
    print(type(listing_containers))
    
    print(len(listing_containers))
    
    

    for container in listing_containers:
        title = container.h2
        if title:
            titles.append(title.text)
        else:
            titles.append(np.nan)  
              
    for container in listing_containers:
        price = container.find('span',class_="a-offscreen")
        if price:
            prices.append(price.text)
        else:
            prices.append(np.nan)   
            
    for container in listing_containers:
        review = container.find('span',class_="a-icon-alt")
        if review:
            reviews.append(review.text)
        else:
            reviews.append(np.nan)
            
    for container in listing_containers:
        unifiedprice = container.find('span',class_="a-price a-text-price")
        if unifiedprice:
            unifiedprices.append(unifiedprice.text)
        else:
            unifiedprices.append(np.nan)            
    for container in listing_containers:
        nbrofreview = container.find('span',class_="a-size-base")
        if nbrofreview:
            nbrofreviews.append(nbrofreview.text)
        else:
            nbrofreviews.append(np.nan)            
    
       
import pandas as pd
test_df = pd.DataFrame({'Title' : titles, 'Price': prices, 'Review':reviews ,'Evaluations clients': nbrofreviews ,'Unified_Price':unifiedprices ,           
})
#Determining duplicates and the quanitity
for column in test_df.columns:
   print(test_df.duplicated([column]))
   print(test_df.duplicated([column]).sum())

#Eliminating duplicates
test_df.drop_duplicates(['Title'],keep='first', inplace=True)

test_df.to_csv('products.csv', index=False, encoding='utf-8') 
print(test_df)
