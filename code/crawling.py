import urllib.request
from bs4 import BeautifulSoup
import re

def crawling_cloth(clothes):
    '''find the data for clothes review and return the dictionary
    
    :param clothes: the list of clothes that wanted information to review
    :type clothes : a list of strings
    :return: dictionary of returned 
    :rtype: dictionary 
    
    '''

    clothesReviews = dict()
    for searchWord in clothes:
        percentEncodingWord = urllib.parse.quote(searchWord)
        url = 'https://search.shopping.naver.com/search/all?query=' +  percentEncodingWord +'&frm=NVSHATC&prevQuery=' + percentEncodingWord

        html = urllib.request.urlopen(url)
        crw = BeautifulSoup(html,'html.parser')

        html = crw.find('div',{'class':'basicList_title__3P9Q7'})
        url = html.find('a')['href']
        
        html = urllib.request.urlopen(url)
        crw = BeautifulSoup(html,'html.parser')
        
        nReviews = crw.find('span',{'class':'totalArea_num2__29zT5'}).text
        stars = crw.find_all('span',{'class':'reviewItems_average__16Ya-'})
        etc = crw.find_all('span',{'class':'reviewItems_etc__1YqVF'})
        reviews = crw.find_all('p',{'class':'reviewItems_text__XIsTc'})
        
        k = 0
        allReviews = dict()
        for i in range(0,int(nReviews)):
            star = {"star":stars[i].text}
            review = {"review":reviews[i].text}
            shoppingMall = {"shoppingMall":etc[k].text}
            date = {'date':etc[k+2].text}
            user = etc[k+1].text
            etcInfo = [shoppingMall,star,date,review]
            allReviews[user] = etcInfo
            if i != int(nReviews)-1:
                check = etc[k+4].text
                if check[3] == '*':
                    k += 3
                else: k += 4

            
        clothesReviews[searchWord] = allReviews
    return clothesReviews



def sites(clothesReviews):
    '''count the site information to using Review database

    :param clothesReviews: dictionary to saving the review data
    :type clothesReviews: dictionary
    :return: return the dictionary to company data
    :rtype: dictionary

    '''
    shoppingMall = dict()
    for i in clothesReviews.values():
        for j in i.values():
            name = j[0].values()
            if name in shoppingMall:
                shoppingMall[name] += 1
            else: shoppingMall[name] = 1
    return shoppingMall




def main():
    cloths = ['파에니 포켓 반팔 자켓']
    reviews = dict()
    clothReviews = crawling_cloth(cloths)
    shoppingMall = sites(clothReviews)
    print(shoppingMall)


if __name__=="__main__":
    main()
