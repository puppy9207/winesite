from selenium import webdriver
from bs4 import BeautifulSoup
import threading

def dictDt(dt):
    for i, val in enumerate(dt):
        if val.string == '용 도':
            dic['용도'] = i
        if val.string == '알코올 도수':
            dic['알코올도수'] = i
        if val.string == '종 류':
            dic['종류'] = i
        if val.string == '품 종':
            dic['품종'] = i
        if val.string == '음용온도':
            dic['음용온도'] = i
        if val.string == '등 급':
            dic['등급'] = i
        if val.string == '당 도':
            dic['당도'] = i
        if val.string == '산 도':
            dic['산도'] = i
        if val.string == '바 디':
            dic['바디'] = i
        if val.string == '타 닌':
            dic['타닌'] = i
        if val.string == '가격':
            dic['가격'] = i
    return dic

def makeFactor(dd):
    try:
        sugar = int(dd[dic['당도']].find('img')['src'][-5])
    except KeyError as e:
        sugar = None
    try:
        acid = int(dd[dic['산도']].find('img')['src'][-5])
    except KeyError as e:
        acid = None
    try:
        body = int(dd[dic['바디']].find('img')['src'][-5])
    except KeyError as e:
        body = None
    try:
        tarnin = int(dd[dic['타닌']].find('img')['src'][-5])
    except KeyError as e:
        tarnin = None
    factor = [sugar,acid,body,tarnin]
    return factor

def getWineText(dd):
    pass

def sepPrice(price):
    if price == '가격정보없음':
        return None
    price = price.replace(",","")
    price = int(price.replace("원",""))
    return price
def writingCsv(wine):
    with open('./wine.csv', 'a', encoding='utf-8-sig') as f:
        csv_data = wine
        for lines in csv_data:
            for line in lines:
                f.write(str(line)+",")
            f.write('\n')


driver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
driver.implicitly_wait(3)
driver.get('https://www.wine21.com/13_search/wine_list.html')
cnt=1
while(True):
    if cnt>1630:
        break

    for a in range(1,11):
        if cnt!= 1:
            if cnt%10 == 1:
                button = driver.find_element_by_link_text('다음')
                button.click()
                driver.implicitly_wait(2)
        if cnt!= 1:
            if cnt%10!=1:
                try:
                    button = driver.find_element_by_link_text(str(cnt))
                    button.click()
                except Exception:
                    for at in range(cnt // 10):
                        awa = driver.find_element_by_link_text('다음')
                        awa.click()
        #한바퀴
        wines = []
        for i in range(1,11):
            wine = []
            name = driver.find_element_by_css_selector('li:nth-child(' + str(i) + ') > div.column_detail1 >div.cnt > div.tit > h4 > a')
            name.click()


            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            #한글이름
            wineKo = soup.select_one('div.column_detail2 > div.cnt > h4').string.replace(","," ")
            wine.append(wineKo)
            #영어이름
            wineEn = soup.select_one('div.column_detail2 > div.cnt > div.name_en').string.replace(","," ")
            wine.append(wineEn)

            dt = soup.select('div.wine_info > dl > dt')
            dd = soup.select('div.wine_info > dl > dd')
            dic = {}
            dic = dictDt(dt)
            factor = makeFactor(dd)

            try:
                winery = driver.find_element_by_css_selector('dd.winery > a').text.strip()
                winery = " ".join(winery.split())
            except Exception:
                winery = None
            try:
                wine_area = driver.find_element_by_css_selector('dd.wine_area > a').text.strip()
            except Exception:
                wine_area = None

            try:
                kind = driver.find_element_by_css_selector('dd.variety').text.strip()
            except Exception:
                kind = None

            try:
                value = dd[dic['종류']].string
                value = value.replace('\xa0','')
            except KeyError as k:
                value = None
            finally:
                wine.append(value)

            try:
                alcohol = float(dd[dic['알코올도수']].string.replace("도",""))
            except KeyError as k:
                alcohol = None
            except ValueError as v:
                alcohol = dd[dic['알코올도수']].string.replace("도","")
                a1= float(alcohol[:alcohol.find("~")])
                a2= float(alcohol[alcohol.find("~")+1:])
                alcohol = (a1+a2)/2

            finally:
                wine.append(alcohol)

            try:
                temp = dd[dic['음용온도']].string
            except KeyError as k:
                temp = None
            finally:
                wine.append(temp)

            try:
                price = dd[dic['가격']].select_one('strong').string
                price = sepPrice(price)
            except KeyError as k:
                price = None
            finally:
                wine.append(price)

            #요인들
            for i in factor:
                wine.append(i)

            wines.append(wine)
            driver.execute_script("window.history.go(-1)")
        print(wines)

        t1 = threading.Thread(target=writingCsv(wines), args=wines, )
        t1.start()
        cnt+=1
