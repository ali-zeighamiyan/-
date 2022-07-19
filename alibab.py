
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import lxml
import html5lib
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from pymongo import MongoClient
import dns

class alibab:
    def __init__(self,search_txt):
        country_of_company_list=[]
        company_name_list=[]
        company_link_list=[]
        establish_year=[]

        
        # self.soup1=soup1
        self.country_of_company_list=country_of_company_list
        self.company_name_list=company_name_list
        self.company_link_list=company_link_list
        self.establish_year=establish_year

        self.search_txt=search_txt

        overview=[]
        self.overview=overview
        prices_of_all_product=[]
        self.prices_of_all_product=prices_of_all_product

        os.environ['PATH']="C:/Users/abc/Desktop/sel driver"
        path='C:/Users/abc/Desktop/sel driver'
        driver=webdriver.Chrome()
        url=f'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&tab=all&SearchText={self.search_txt}'
        driver.get(url)
        # driver.implicitly_wait(4)
        try:
            advertise=driver.find_element(By.CLASS_NAME,'gdpr-close')
            advertise.click()
        except:
            pass
        self.driver=driver
    
        self.link_title_of_all_product()



    def link_title_of_all_product(self):
        product_links=self.driver.find_elements(By.CLASS_NAME, 'elements-title-normal')
        self.product_links=product_links
        links_of_all_product=[]
        title_of_all_product=[]
        self.links_of_all_product=links_of_all_product
        self.title_of_all_product=title_of_all_product
        for link in self.product_links:
            self.links_of_all_product.append(link.get_attribute('href'))
            self.title_of_all_product.append(link.text)

    
    def loop(self):
    
        
        for i,link in enumerate(self.links_of_all_product):
            print(i)
            self.i=i
            self.link=link
            
            

            source=requests.get(link)
            soup=BeautifulSoup(source.text,"lxml")
            self.soup=soup
            self.get_prices()
            self.get_overview()
            self.get_company_details()

            if i==10:
                break
        return [self.price_normalizer(),self.overview,self.name_func_feature(),self.links_of_all_product,self.company_link_list,self.company_name_list,self.establish_year,self.country_of_company_list]
    


    def get_prices(self):
        
        self.driver.get(self.link)
        source1=self.driver.page_source
        self.source1=source1


        try:
            price=self.driver.find_element(By.ID,'buy-sample').find_element(By.CLASS_NAME,'sample-item')

            self.prices_of_all_product.append(price.text)

        except:
            try:
                #price=driver.find_element(By.CLASS_NAME,'price-item').text
                price=WebDriverWait.until(EC.presence_of_element_located(By.CLASS_NAME,'price-item').text)
                self.prices_of_all_product.append(price)
            
            except:
                try:
                    soup1=BeautifulSoup(self.source1,"lxml")
                    container=soup1.find('div',id='container')
                    price=container.find('div',class_='promotion-price').text
                    self.prices_of_all_product.append(price)
                except:
                    try:
                        price=self.driver.find_element(By.CLASS_NAME,'product-price')
                        self.prices_of_all_product.append(price.text)
                    except:
                        self.prices_of_all_product.append('not found')
    
    def get_overview(self):
        
        detail_type_list=[]
        detail_list=[]
    

        soup1=BeautifulSoup(self.source1,"lxml")
        detail_types=soup1.findAll('span',class_='attr-name')
        
        detail=soup1.findAll('div',class_='text-ellipsis')
        
        for det_type,det in zip(detail_types,detail):
    

            detail_type_list.append(det_type.text)
            detail_list.append(det.text)
        
        

        new_dict = {detail_type_list[m]: detail_list[m] for m in range(len(detail_type_list))}
        self.overview.append(new_dict)
        self.new_dict=new_dict
        return self.overview



    def get_company_details(self):
        soup1=BeautifulSoup(self.source1,"lxml")
     
        company_name=soup1.find('div',class_='company-name-container')
        if company_name==None:
            company_name=soup1.find('div',class_='company-item')
        self.company_name_list.append(company_name.text)

        self.company_link_list.append(company_name.find('a').get('href'))


        source2=requests.get(self.company_link_list[self.i])
        soup2=BeautifulSoup(source2.text,'lxml')
        year=soup2.find_all('td',class_='field-title')
        try:
            for y in year:
                if y.text=='Year Established':
                    break
            year_es=y.findNext('div',class_='content-value').text
            year_es=int(year_es)
            self.establish_year.append(year_es)
        except:
            pass

        self.country_of_company_list.append(self.new_dict['Place of Origin:'])


    def price_normalizer(self):
                ########### normalize prices and convert to float
        for i1,price in enumerate(self.prices_of_all_product):
            # print(price.split())
            for i2,p in enumerate(price):
                if p=="$":
                    self.prices_of_all_product[i1]=price[i2+1:]
        for iteration in range(3):

            for i1,price in enumerate(self.prices_of_all_product):
                for i3,p1 in enumerate(price[0:]):
                    if p1=="/":
                        self.prices_of_all_product[i1]=price[0:i3]

        for k,kp in enumerate(self.prices_of_all_product):
            self.prices_of_all_product[k]=self.prices_of_all_product[k].replace(',','')
            if self.prices_of_all_product[k]!='not found':
                self.prices_of_all_product[k]=float(self.prices_of_all_product[k])
        return self.prices_of_all_product
        #############

    def name_func_feature(self):
        All_names=[]
        self.All_names=All_names

        for d1,dic in enumerate(self.overview):
            m=0
            for t1,type in enumerate(dic):
                if type=='Product name:':
                    self.All_names.append(self.overview[d1]['Product name:'])
                    m=1
                
                elif type=='Product Name::':
                    self.All_names.append(self.overview[d1]['Product Name::'])
                    m=1
                elif type=='Product Name:':
                    self.All_names.append(self.overview[d1]['Product Name:'])
                    m=1
            if m==0:
                self.All_names.append(self.title_of_all_product[d1])
                
        #######
        All_funcs=[]
        self.All_funcs=All_funcs

        for d2,dic2 in enumerate(self.overview):
            n=0
            for t2,type2 in enumerate(dic2):
                if type2=='Function:':
                    self.All_funcs.append(self.overview[d2]['Function:'])
                    n=1
                
                elif type2=='Function::':
                    self.All_funcs.append(self.overview[d2]['Function::'])
                    n=1

            if n==0:
                self.All_funcs.append(None)
        ###############

        All_feature=[]
        self.All_feature=All_feature
        for d3,dic3 in enumerate(self.overview):
            s=0
            for t3,type3 in enumerate(dic3):
                if type3=='Feature:':
                    self.All_feature.append(self.overview[d3]['Feature:'])
                    s=1
                
                elif type3=='Feature::':
                    self.All_feature.append(self.overview[d3]['Feature::'])
                    s=1

            if s==0:
                self.All_feature.append(None)

        return self.All_names,self.All_funcs,self.All_feature
        
    def save_to_db(self):
        cluster = MongoClient("mongodb+srv://ali3515:35154174@cluster0.h3tum.mongodb.net/?retryWrites=true&w=majority")
        db=cluster["alibaba"]
        collection=db['products']
        collection.delete_many({})
        for i in range(len(self.All_names)):
            print(i)
            dict1={"_id":i,"Name":self.All_names[i],"Function":self.All_funcs[i],"Feature":self.All_feature[i],"Country":self.overview[i]['Place of Origin:'],"Link":self.links_of_all_product[i],"Price":self.prices_of_all_product[i],"Overview":self.overview[i]}
            collection.insert_one(dict1)

        collection2=db['company']
        collection2.delete_many({})
        for j in range(len(self.All_names)):

            dict2={"id":j,"Name":self.company_name_list[j],"Link":self.company_link_list[j],"Country":self.country_of_company_list[j],"Established Year":self.establish_year[j]}
            collection2.insert_one(dict2)
        








search_text=input('Please Enter your desired product')
c1=alibab(search_text)
a=c1.loop()
c1.save_to_db()


