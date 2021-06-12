import urllib.request
from bs4 import BeautifulSoup
import re

def crawling_cloth(clothes):
    '''find the two values to sell the clothes and return the dictionary
    
    :param clothes: the list of clothes that wanted information to review
    :type clothes : a list of strings
    :return: dictionary of returned : {shoppin mall name : links}
    :rtype: dictionary 
    
    '''
    for searchWord in clothes:
        percentEncodingWord = urllib.parse.quote(searchWord)
        url = 'https://search.shopping.naver.com/search/all?query=' +  percentEncodingWord +'&frm=NVSHATC&prevQuery=' + percentEncodingWord

        html = urllib.request.urlopen(url)
        crw = BeautifulSoup(html,'html.parser')

        html = crw.find('div',{'class':'basicList_title__3P9Q7'})
        url = html.find('a')['href']
        
        html = urllib.request.urlopen(url)
        crw = BeautifulSoup(html,'html.parser')

        shops = crw.find_all('div',{'class':'productByMall_text_over__1rkUg'})
        
        shoppingMall = dict()
        namelink = dict()
        for i in shops:
            name = i.find('img')['alt']
            bridgeLinks = i.find('a')['href']
    
            html = urllib.request.urlopen(bridgeLinks)
            crw = BeautifulSoup(html,'html.parser')

            text = str(crw)
            url = text.split("  ")
            for i in url:
                if 'var targetUrl' in i:
                    urls = i.split('\"')
                    for j in urls:
                        if 'http://' in j:
                           link = j
            namelink[name] = link

        shoppingMall[searchWord] = namelink
    return shoppingMall
        
            
def crawling_review_eleven(url,reviews):
    
    html = urllib.request.urlopen(url)
    crw = BeautifulSoup(html,'html.parser')

    allReviews = crw.find('dii',{'class':'area_list'})

    print(crw)
    reviews = crw.find_all('li')
    print(reviews)

    for i in reviews:
        name = i.find('dt',{'class':'name'}).text
        print(name)





def main():
    cloths = ['파에니 포켓 반팔 자켓']
    reviews = dict()
    shoppingMall = crawling_cloth(cloths)
    print(shoppingMall)

    
    for i in shoppingMall:
        for j in shoppingMall[i]:
            print(j)
            if j == '11번가':
                print(shoppingMall[i][j])
                crawling_review_eleven(shoppingMall[i][j],reviews)

    


if __name__=="__main__":
    main()
