import urllib.request
from bs4 import BeautifulSoup

def crawling_cloth(clothes):
    '''find the two values to sell the clothes and return the dictionary
    
    :param clothes: the list of clothes that wanted information to review
    :type clothes : a list of strings
    :return: dictionary of returned : {shoppin mall name : links}
    :rtype: dictionary 
    
    '''
    for searchWord in clothes:
        percentEncodingWord = urllib.parse.quote(sw)
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
            links = i.find('a')['href']
            namelink[name] = links

        shoppingMall[sw] = namelink
    return shoppingMall
        
            
def crawling_



def main():
    cloths = ['파에니 포켓 반팔 자켓']
    a = crawling_cloth(cloths)
    print(a)

if __name__=="__main__":
    main()
