import requests
import json
from bs4 import BeautifulSoup

base_cwd = "C:/Users/sskor/Documents/real_estate_crawler"
data = {}
data['bazos'] = []
base_url = "https://reality.bazos.sk"
locations = {"Latky": "98545", "Malinec": "98526"}
distance = ""

def GetBSPlain(url):
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    return s
# print(s.prettify())
def page_loop(url):
    s = GetBSPlain(url)
    for nadpis in s.findAll("div", {'class':'inzeratynadpis'}):
        if nadpis.find("h2", {'class': 'nadpis'}) is not None:
            podnadpis = nadpis.find("h2", {'class': 'nadpis'})

            for nadpis_a in podnadpis.findAll("a"):
                # added if statement to avoid first occurance of "inzeraty popis" 
                # which as a website header

                    text = nadpis_a.get_text()
                    sublink = nadpis_a.get('href')
                    id = (sublink.split('/')[2])
                    # include try and valuerror
                    data['bazos'].append({'id': id, 'header': text, 'url': f"{base_url}{sublink}"})

    try: 
        next_page_link = (
            s
            .find('p', attrs = {"class":'strankovani'})
            .find('a', text = 'Ďalšia')
            .get('href')
        )
    except: 
        next_page_link = None
    
    if (next_page_link is not None) :
        page_loop(url=f"{base_url}{next_page_link}")

    return(data)

for location in locations.values(): 
    url_init = f"{base_url}/predam/pozemok/?hledat=&hlokalita={location}&humkreis={distance}&cenaod=&cenado="
    data = page_loop(url=url_init)

for idx, post in enumerate(data['bazos']):
    # print(f"{base_url}{post['url']}")
    s_detail = GetBSPlain(post['url'])
    detail_text = s_detail.find('div', {'class':'popisdetail'}).get_text()
    # print(s_detail.find('td', {'class':'listadvlevo'}))
    table_body = s_detail.find('td', {'class':'listadvlevo'}).find('table')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if cols[0].get_text() == 'Videlo:':
            seen = cols[1].get_text()
        if cols[0].get_text() == 'Meno:':
            name = cols[1].get_text()
        if cols[0].get_text() == 'Cena:':
            price = cols[1].get_text()
    if(~((detail_text is None) & (seen is None) & (name is None) & (price is None))):
        detail_data = {
            'price':price,
            'name':name,
            'seen':seen,
            'text_detail':detail_text
        }
        data['bazos'][idx]['detail'] = detail_data
    
with open(f'{base_cwd}/data/new/bazos.json', 'w') as f:
  json.dump(data, f)