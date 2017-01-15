__author__ = "Zoe ZHU"
__copyright__ = "Copyright 2017, Pitt"


## The method following in comments does not work, I don't know why, maybe the website can detect this crawl using this technology
# import scrapy
#
# class MoiveSpider(scrapy.Spider):
#     name="doubanmoive"
#     allowed_domains=["movie.douban.com"]
#     start_urls=["https://movie.douban.com/subject/6982558/"]
#
#     def parse(self,response):
#         print(response.css('h1 span').extract())

from bs4 import BeautifulSoup
import urllib.request
import csv

def each_movie(url, fileName, attrs):
    res_data = {'类型': []}
    key = ''
    with urllib.request.urlopen(url) as response:
       html = response.read()
    soup = BeautifulSoup(html)

    # crawl the name of movie
    for h1 in soup.find_all('h1'):
        for span in h1.find_all('span'):
            if span.get('property') == "v:itemreviewed":
                res_data["片名"] = [span.string]
            else:
                res_data["年份"] = [span.string[1:-1]]
                break
    # crawl "director", "scenarist", "actor" and "genre"
    for div in soup.find_all('div'):
        if div.get('id') == "info":
            for each in div.find_all('span'):
                for e in each.find_all('span'):
                    if key == '':
                        key = e.string
                        res_data[key] = []
                    else:
                        for all in e.find_all('a'):
                            res_data[key].append(all.string)
                        key = ''
                # crawl "genre"
                if each.get('property') == "v:genre":
                    res_data['类型'].append(each.string)
    # crawl score
    for strong in soup.find_all('strong'):
        res_data['评分'] = [strong.string]

    # write the data to file
    with open(fileName,'a') as file:

        for element in attrs:
            if element in res_data:
                try:
                    for i in res_data[element]:
                        file.write(i+' ')
                except:
                    file.write(' ')
            else:
                file.write(' ')
            file.write('\t')
        file.write('\n')
        # file.close()
    # print(res_data)


def everyPage(url, fileName, attrs):
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html)
    # get the content of the movie
    for table in soup.find_all('table'):
        for div in table.find_all('div'):
            if div.get('class') == ['pl2']:
                each_movie(div.a.get('href'), fileName, attrs)

    # next page
    for div in soup.find_all('div'):
        if div.get('class') == ['article']:
            for child in div.find_all('div', recursive=False):
                if child.get('class') == ['paginator']:
                    for span in child.find_all('span'):
                        if span.get('class') == ['next']:
                            everyPage(span.a.get('href'), fileName, attrs)


# main function
# url = 'https://movie.douban.com/tag/%E4%B8%AD%E5%9B%BD'
url = 'https://movie.douban.com/tag/%E4%B8%AD%E5%9B%BD?start=4540&type=T'
fileName = '/Users/zz/Desktop/doubanData.txt'
attrs = ['片名','年份','评分','主演','导演','类型','编剧']
# write header into file
# with open(fileName,'w') as file:
#     for i in attrs:
#         file.write(i + '\t')
#     file.write('\n')
everyPage(url, fileName, attrs)



# Rewrite the txt into csv
with open(fileName,'r') as old:
    with open('/Users/zz/Desktop/doubanData.csv','w', encoding='utf-8') as new:
        fieldnames = old.readline().split()
        writer = csv.DictWriter(new, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        line = old.readline()
        while line:
            row = line.split('\t')
            dic = {}
            for i in range(len(fieldnames)):
                dic[fieldnames[i]] = row[i]
            # print(dic)
            writer.writerow(dic)
            line = old.readline()