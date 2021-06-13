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
        
        nReviews = crw.find('li',{'class':'filter_on__X0_Fb'}).text
        nReviews = nReviews[-2]
        stars = crw.find_all('span',{'class':'reviewItems_average__16Ya-'})
        etc = crw.find_all('span',{'class':'reviewItems_etc__1YqVF'})
        reviews = crw.find_all('p',{'class':'reviewItems_text__XIsTc'})
        
        k = 0
        allReviews = dict()
        for i in range(0,int(nReviews)):
            star = {"star":int(str(stars[i].text)[-1])}
            review = {"review":reviews[i].text}
            shoppingMall = {"shoppingMall":etc[k].text}
            date = {'date':etc[k+2].text}
            user = etc[k+1].text
            etcInfo = [shoppingMall,star,date,review]
            allReviews[user] = etcInfo
            try:
                check = etc[k+4].text
                if check[3] == '*':
                    k += 3
                else: k += 4
            except:
                break

            
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
    mallInfo = dict()
    for i in clothesReviews.values():
        for j in i.values():
            name = str(j[0].values())
            name = name[14:-3]
            star = j[1].values()
            star = int(str(star)[-3])
            if shoppingMall.get(name) != None:
                
                mallInfo = shoppingMall[name]
                meanStar = mallInfo["star"]
                n = mallInfo["nReviews"]
            
                n += 1
                meanStar = (star+meanStar)/n
            
                mallInfo = {"nReviews":n, "star":meanStar}
                del(shoppingMall[name])
                shoppingMall[name] = mallInfo
            else:
                mallInfo2 = dict()
                mallInfo2["nReviews"] = 1
                mallInfo2["star"] = star
                shoppingMall[name] = mallInfo2
    return shoppingMall



#def clothes

def main():
    cloths = ['파에니 포켓 반팔 자켓','아엘 루즈핏 자켓']
    reviews = dict()
    clothReviews = crawling_cloth(cloths)
    shoppingMall = sites(clothReviews)
    print(shoppingMall)


if __name__=="__main__":
    main()
