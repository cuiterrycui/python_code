# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 15:16:26 2018

@author: terry
"""


import os
import requests
from lxml import html
import csv

headers = {
#    'Host': 'www.nusil.com',
#    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    # 2017.12 经网友提醒，知乎更新后启用了网页压缩，所以不能再采用该压缩头部
    # !!!注意, 请求头部里使用gzip, 响应的网页内容不一定被压缩，这得看目标网站是否压缩网页
    # 'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}


def save(text, filename='temp', path='download'):
    fpath = os.path.join(path, filename)
    with open(fpath, 'w') as  f:
        print('output:', fpath)
        f.write(text)


def save_image(image_url):
    resp = requests.get(image_url)
    page = resp.content
    filename = image_url.split('zhimg.com/')[-1]
    save(page, filename)


def crawl(url,filename):
    resp = requests.get(url)
    page = resp.content
#    f = open(filename+'.html', 'w+')
#    f.write(page)
#    f.close()



#    print(page)
    root = html.fromstring(page)
    dbproductresult =  root.find(".//div[@class='db-product-result']")        
#    print(dbproductresult)
    
    pagecontent = dbproductresult.find(".//div[@class='page-content']") 
#    print(pagecontent)
    
    propertiesrow  =  pagecontent.find(".//div[@id='properties-row']")
    
  
 #   print(propertiesrow)
    
    medium7columns   = propertiesrow.find(".//div[@class='medium-7 columns']")  
#    print(medium7columns.text_content())  
    
    propertiestable =   propertiesrow.find(".//table[@class='properties-table']")
#    print(propertiestable.text_content().strip().replace(' ','').replace('\n',':'))  
    print(propertiestable.text_content().strip().replace(' ',''))     
    

#    medium-5 columns
    medium5columns   = pagecontent.find(".//div[@class='medium-5 columns']")  
    print(medium5columns.text_content())
    
    medium7columns   = pagecontent.find(".//div[@class='medium-7 columns']")  
    print(medium7columns.text_content())  
    
    dic={"Product":filename,"Description":medium5columns.text_content(),"Applications":medium7columns.text_content(),"Properties":propertiestable.text_content().strip().replace(' ','')
}   
    csvFile3 = open('csvFile.csv','w') 
    writer2 = csv.writer(csvFile3)
    for key in dic:
        writer2.writerow([key, dic[key]])
    csvFile3.close() 
    
    
    
    
    
    
def crawlfile():
    f = open("all.xml","r")
    xmlstring = f.read(10000000)
        
    root = html.fromstring(xmlstring)
#    print(dir(root))
#    print(root)
    product_table =root.findall(".//div[@class='product-row ']")
    
#    product_table =root.findall(".//div[@class='product-row']")
#    print(len(product_table))    
#    print(product_table)
    
    for product in product_table:
        ahref =product.find(".//a") 
#        print(len(ahref))
        url = ahref.attrib     
        print(ahref.text_content())
        print(url['href'])
        crawl(url['href'],ahref.text_content().strip())

    
    
   
   
#    image_urls = root.xpath('//img[@data-original]/@data-original')
#    for image_url in image_urls:
#        save_image(image_url)


if __name__ == '__main__':
    # 注意在运行之前，先确保该文件的同路径下存在一个download的文件夹, 用于存放爬虫下载的图片
    url = 'https://nusil.com/en/productsearch#life-sciences?segment=all'  # 有一双美腿是一种怎样的体验?
#    crawl(url)
    crawlfile()
    
