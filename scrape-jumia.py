import time
from bs4 import BeautifulSoup
import requests
import json
from alive_progress import alive_bar

base_pages = [
  'https://www.jumia.ug/groceries/',
  'https://www.jumia.ug/phones-tablets/',
  'https://www.jumia.ug/home-office/',
  'https://www.jumia.ug/electronics/',
  'https://www.jumia.ug/health-beauty/',
  'https://www.jumia.ug/category-fashion-by-jumia/',
  'https://www.jumia.ug/computing/',
  'https://www.jumia.ug/sporting-goods/',
  'https://www.jumia.ug/baby-products/',
  'https://www.jumia.ug/video-games/',
  'https://www.jumia.ug/patio-lawn-garden/',
]

phones_dic = []

def get_links():
  url = 'https://www.jumia.ug'
  
  # get links container
  links_container_selector = '#jm > main > div.row.-pvm > div.col16.-df.-j-bet.-pbs > div.flyout-w.-fsh0.-fs0 > div > div:nth-child(2) > div > div:nth-child(1) > div'
  
  
  req = requests.get(url)
  
  soup = BeautifulSoup(req.text, 'lxml')
  
  
  return [i.text for i in  soup.select_one(links_container_selector).find_all('a')]
  # return [i.a for i in soup.select(links_container_selector)]

def parse(link):

  page = 1
  # samsung phones from 500k t0 1M

  products_selector = '#jm > main > div.aim.row.-pbm > div.-pvs.col12 > section > div.-paxs.row._no-g._4cl-3cm-shs > article'

  
  # loop through pages
  while(True):
    
    items_in_prev = len(phones_dic)

    # link = f'https://www.jumia.ug/catalog/?q=samsung+phones&price=500000-1000000'
    # link = 'https://www.jumia.ug/groceries/'
    
    # collect html
    # print(f'fetching page {page} >> {link}...')
    
    final_link = link + f'?page={page}'
    
    r = requests.get(final_link)
    
    # print(f'status >> {r.status_code}')
    
    if r.status_code == 404:
      break
    
    # print(f'page {page} fetching success')

    # print('parsing...')

    soup = BeautifulSoup(r.text, 'html.parser')


    for product in soup.select(products_selector):
      phone_name = product.a.select_one('h3.name').text
      phone_price = product.a.select_one('div.prc').text
      phone_link = product.a.get('href')

      
      # is fridge
      if phone_name == 'Changhong CH-120':
        print('##################################')
        print('##################################')
        
        print(f'link >> https://jumia.ug{phone_link}')
        
        print('##################################')
        print('##################################')
        break
      
      if not phone_name == '': # remove false positives
        phones_dic.append({
          'name': phone_name,
          'price': phone_price,
          'link': f'https://jumia.ug{phone_link}',
        })
        
    # did we get anything we probably on error page
    diff = len(phones_dic) - items_in_prev
    print(final_link, diff)
    if diff == 0:
      break
        
    page += 1
    
    yield
  

# print(get_links())


# looping through pages
print('')
for link in base_pages:
  print(f'fetching products... >> {link} \n')  
  with alive_bar(0) as bar:
    for i in parse(link=link):
      time.sleep(.001)
      bar()
    
# print(json.dumps(phones_dic))
print('\n')
print(len(phones_dic), 'phones collected')
