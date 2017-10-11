#-*-coding : utf-8 -*-

import urllib

import os

from urllib.request import urlopen

from bs4 import BeautifulSoup

import re

from selenium import webdriver


#제목 크롤링 함수
def get_title(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    title = ''
    for item in soup.find_all('h1', class_='headline mg'):
        #print (item)
        #title = title + str(item.find_all(title=True))
        title = title + str(item.text)
    return title

#날짜 크롤링 함수
def get_date(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    date = ''
    date_num = ''
    for item in soup.find_all('div', class_='byline'):
        #print (item)
        #text = text + str(item.find_all(text=True))

        date = date + str(item.text)
        date_num = re.sub(r'[^0-9\.]+', ' ', date)
        date_num = date_num[:11]

    return date_num

#요약 크롤링 함수
def get_summary(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    summary = ''
    for item in soup.find_all('meta', attrs={"name":"description"}):
        #print (item)
        #text = text + str(item.find_all(text=True))
        s = re.sub(r'[^가-힣0-9]', " ", str(item))
        #s = re.sub(r'[!@#$&*():;="./|<>a-zA-Z]', repl, text)
        #summary = summary.replace('\n', ' ')
        #s = "\n".join(s.splitlines())
        summary = s.replace("\n", ' ')

        #delete !@#$&*():;="./|<>a-zA-Z
        #print(summary)
    return summary

#본문 크롤링 함수
def get_bodytext(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    newText = ''
    for item in soup.find_all('div', id='article_body'):
        #print (item)
        #text = text + str(item.find_all(text=True))
        text = text + str(item.text)
        newText = re.sub(r'[^가-힣0-9]+', " ", text)
    return newText

# 메인함수
def main(URL, OUTPUT_FILE_NAME):
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_title = get_title(URL)
    result_date = get_date(URL)
    result_summary = str(get_summary(URL))
    result_text = get_bodytext(URL)

    #print(result_title)
    #print(result_date)
    #print(result_summary)
    #print(result_text)

    #open_output_file.write('제목:' + result_title)
    open_output_file.write(result_title)
    open_output_file.write(';')
    #open_output_file.write('날짜:' + result_date)
    open_output_file.write(result_date)
    open_output_file.write(';')
    #open_output_file.write('요약:' + result_date)
    open_output_file.write(result_summary)
    open_output_file.write(';')
    #open_output_file.write('본문:' + result_text)
    open_output_file.write(result_text)
    open_output_file.write(';')
    open_output_file.close()

#if __name__ == '__main__':
#    main(URL, OUTPUT_FILE_NAME)


for page in range(1,10):
    #출력파일명
    OUTPUT_FILE_NAME='/home/pirl/BS/JoongAng_new'+str(page)+'.txt'
    #크롤링할 URL
    URL='http://news.joins.com/article/'+str(page)
    if get_title(URL) != "":
        main(URL, OUTPUT_FILE_NAME)
    else:
        pass
