from bs4 import BeautifulSoup
import requests
import time
import json
import random
from pandas import DataFrame

def crawPageSearch(url):
    data = []
    page = '1'
    urlInput = url + '&page='
    baseUrl = url.split('/search')[0] 
    if len(url) == 0 : 
        return print(" Link is not found")
    pagingRes = requests.get(url, headers={'User-Agent': getUserAgent()}, proxies={'http':getProxy()})
    soupPage = BeautifulSoup(pagingRes.content, "html.parser")
    if type(soupPage.find('div',class_="pagination__nav")) == str : 
        paging = soupPage.find('div',class_="pagination__nav").findChildren('a', recursive=False)[2].text
        page = paging
    numPage = int(page)
    for i in range(1,numPage+1):
        response = requests.get(urlInput + str(i), headers={'User-Agent': getUserAgent()}, proxies={'http':getProxy()})
        soup = BeautifulSoup(response.content, "html.parser")
        productList = soup.find('div', class_='product-list')
        for product in productList:
            Title = product.find("a", class_="product-item__title").text
            Link = baseUrl + product.find("a", class_="product-item__title").attrs["href"]
            Link = Link[ :Link.index("?")]
            obj = {
                    'Title' :Title,
                    'Link_Image1': '',
                    'Link_Image2': '',
                    'Link_Image3': '',
                    'Link_Image4': '',
                    'SKU': '',
                    'Link':Link,
                    'mmolazi_type': '',
                    'tags': '',
                    'category': ''
                }
            productDetailRes = requests.get(Link, headers={'User-Agent': getUserAgent()}, proxies={'http':getProxy()})
            soupPD = BeautifulSoup(productDetailRes.content, "html.parser")
            Link_Image1 = 'http:' + soupPD.find('div', class_='product-gallery__thumbnail-list').findChildren("a", recursive=False)[0].attrs["href"]
            if len(list(soupPD.find('div', class_='product-gallery__thumbnail-list').children)) > 1:
                Link_Image2 = 'http:' + soupPD.find('div', class_='product-gallery__thumbnail-list').findChildren("a", recursive=False)[1].attrs["href"]
                if len(list(soupPD.find('div', class_='product-gallery__thumbnail-list').children)) > 2:
                    Link_Image3 = 'http:' + soupPD.find('div', class_='product-gallery__thumbnail-list').findChildren("a", recursive=False)[2].attrs["href"]
                    if len(list(soupPD.find('div', class_='product-gallery__thumbnail-list').children)) > 3:
                        Link_Image4 = 'http:' + soupPD.find('div', class_='product-gallery__thumbnail-list').findChildren("a", recursive=False)[3].attrs["href"]
                        obj['Link_Image1'] = Link_Image1
                        obj['Link_Image2'] = Link_Image2
                        obj['Link_Image3'] = Link_Image3
                        obj['Link_Image4'] = Link_Image4
                    else : 
                        obj['Link_Image1'] = Link_Image1
                        obj['Link_Image2'] = Link_Image2
                        obj['Link_Image3'] = Link_Image3
                else :
                    obj['Link_Image1'] = Link_Image1
                    obj['Link_Image2'] = Link_Image2
            else :
                obj['Link_Image1'] = Link_Image1
            data.append(obj)
        print("crawling page: "+ urlInput+str(i))
    print("Have " + str(len(data)) + "products crawled from: "+  url)
    return data

def crawPageCollection(url):
    data = []
    productsCount = 0
    urlInput = url + '/products.json?limit=250&page='
    page = 1
    if len(url) == 0:
        return print("Url is not found")
    paging = requests.get(url + '.json')
    soupPage = BeautifulSoup(paging.content, "html.parser")
    productsCount = json.loads(str(soupPage))["collection"]["products_count"]
    if int(productsCount) == 0 : 
        print("This page not have data")
    page += int(productsCount)//250
    for i in range(1, page+1):
        response = requests.get(urlInput+ str(i), headers={'User-Agent': getUserAgent()}, proxies={'http':getProxy()})
        soup = BeautifulSoup(response.content, "html.parser")
        for product in json.loads(str(soup))["products"] :
            obj = {
                    "Title": '',
                    "Link_Image1": '',
                    "Link_Image2": '',
                    "Link_Image3": '',
                    "Link_Image4": '',
                    "SKU": '',
                    "Link": '',
                    "mmolazi_type": '',
                    "tags": '',
                    "category": ''
                }
            obj["Title"] = product["title"]
            if len(product["images"]) > 0 :  
               obj["Link_Image1"] =  product["images"][0]["src"] 
            else :  obj["Link_Image1"] =  ''
            if len(product["images"]) > 1 :  
               obj["Link_Image2"] =  product["images"][1]["src"] 
            else :  obj["Link_Image2"] =  ''
            if len(product["images"]) > 2 :  
               obj["Link_Image3"] =  product["images"][2]["src"] 
            else :  obj["Link_Image3"] =  ''
            if len(product["images"]) > 3 :  
               obj["Link_Image4"] =  product["images"][3]["src"] 
            else :  obj["Link_Image4"] =  ''
            obj["Link"] = url + "/products/" + product["handle"]
            obj["tags"] = ''.join(product["tags"]) 
            data.append(obj)
        print("Crawling page:" + urlInput+ str(i))
    print("Have " + str(len(data)) + "products crawled from: " +  url)
    return data

def crawPageProduct(url):
    data = []
    urlInput = url + '.json'
    if len(url) ==0 :
        return print("Url is not found")
    response = requests.get(urlInput, headers={'User-Agent': getUserAgent()}, proxies={'http':getProxy()})
    soup = BeautifulSoup(response.content, "html.parser")
    product = json.loads(str(soup))["product"]
    obj = {
            "Title": '',
            "Link_Image1": '',
            "Link_Image2": '',
            "Link_Image3": '',
            "Link_Image4": '',
            "SKU": '',
            "Link": '',
            "mmolazi_type": '',
            "tags": '',
            "category": ''
        }
    obj["Title"] = product["title"]
    if len(product["images"]) > 0 :  
        obj["Link_Image1"] =  product["images"][0]["src"] 
    else :  obj["Link_Image1"] =  ''
    if len(product["images"]) > 1 :  
        obj["Link_Image2"] =  product["images"][1]["src"] 
    else :  obj["Link_Image2"] =  ''
    if len(product["images"]) > 2 :  
        obj["Link_Image3"] =  product["images"][2]["src"] 
    else :  obj["Link_Image3"] =  ''
    if len(product["images"]) > 3 :  
        obj["Link_Image4"] =  product["images"][3]["src"] 
    else :  obj["Link_Image4"] =  ''
    obj["Link"] = url + "/products/" + product["handle"]
    obj["tags"] = ''.join(product["tags"]) 
    data.append(obj)
    print("Crawling page:"+ url)
    print("Have 1 product crawled from: "+  url)
    return data

def writeFile(data, suffix):
    df = DataFrame(data, columns=["Title","Link_Image1","Link_Image2","Link_Image3","Link_Image4","SKU","Link","mmolazi_type","tags","category"])
    export_csv = df.to_csv('newmoon_import_template_'+ str(suffix )+ '.csv',index = None, header=True)

def readFile(path):
    f = open(path, 'r')
    data = f.read().split('\n')
    f.close()
    return data

def getProxy():
    data = readFile('proxies.txt')
    return data[random.randrange(0,len(data))]

def getUserAgent():
    data = readFile('useragents.txt')
    return data[random.randrange(0,len(data))]

if __name__ == "__main__":
    suffix = time.time()
    dataAll = []
    data = readFile('input.txt')
    for url in data :
        arr = url.split('/')
        for i in range(len(arr)-1, 1, -1) :
            if  arr[i] == 'products' :
                dataPro = crawPageProduct(url)
                dataAll += dataPro
                break   
            elif arr[i] == 'collections' :
                dataColl = crawPageCollection(url)
                dataAll += dataColl
                break
            elif arr[i].split('?')[0] == 'search' : 
                dataSearch = crawPageSearch(url)
                dataAll += dataSearch
                break
    writeFile(dataAll, suffix)