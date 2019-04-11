import bs4 as bs
import urllib.request
import json

'''
    scrape data from allbud.com
'''


baseurl = 'https://www.allbud.com/marijuana-strains/search?sort=alphabet&letter='
num_results = str(400)
resultsurl = '&results=' + num_results
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
allbudurl = 'https://www.allbud.com'
results_dict = {}

if __name__ == "__main__":
    for letter in alphabet:
        source = urllib.request.urlopen(baseurl + letter).read()
        soup = bs.BeautifulSoup(source,'lxml')

        mydivs = soup.findAll("article", {"class": "infocard strain"})

        for div in mydivs:
            name = div.find("h3", {"itemprop": "name"}).get_text().strip()
            try:
                rating = div.find("div", {"itemprop": "ratingValue"}).get_text().strip()
            except AttributeError:
                rating = None

            strainurl = div.find("section", {"class": "object-title"}).find("a", href=True)['href']

            strain_source = urllib.request.urlopen(allbudurl + strainurl).read()
            strain_soup = bs.BeautifulSoup(strain_source, 'lxml')

            pos_effects = strain_soup.find("section", {"id": "positive-effects"}).find_all("a", href=True)
            pos_effects_list = []
            for effect in pos_effects:
                pos_effects_list.append(effect.get_text())

            relieved_effects = strain_soup.find("section", {"id": "relieved"}).find_all("a", href=True)
            relieved_effects_list = []
            for effect in relieved_effects:
                relieved_effects_list.append(effect.get_text())

            flavor_effects = strain_soup.find("section", {"id": "flavors"}).find_all("a", href=True)
            flavor_effects_list = []
            for effect in flavor_effects:
                flavor_effects_list.append(effect.get_text())

            aroma_effects = strain_soup.find("section", {"id": "aromas"}).find_all("a", href=True)
            aroma_effects_list = []
            for effect in aroma_effects:
                aroma_effects_list.append(effect.get_text())

            description = strain_soup.find("div", {"class": "panel-body well description"}). \
                find("span", {"class": "hidden-xs"}, recursive=False).get_text().strip()

            percentages_dict = {}
            percent_wrapper = strain_soup.find("h4", {"class": "percentage"})

            percentages = percent_wrapper.text.replace(" ", "").replace("\n", "").split(',')
            if percentages != ['']:
                for percentage in percentages:
                    temp = percentage.split(':')
                    percentages_dict[temp[0]] = temp[1]


            results_dict[name] = {
                'rating': rating,
                'positive': pos_effects_list,
                'medical': relieved_effects_list,
                'flavor': flavor_effects_list,
                'aroma': aroma_effects_list,
                'percentages': percentages_dict,
                'description': description
            }
        print('done with: ' + letter)
    with open('../data/allbud_output.json', 'w') as outfile:
        json.dump(results_dict, outfile)
