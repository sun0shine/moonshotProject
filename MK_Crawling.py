#-*-coding : utf-8 -*-

import urllib

import os

from urllib.request import urlopen

from bs4 import BeautifulSoup

import re

from urllib.request import HTTPError




#제목 크롤링 함수

def get_title(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    title = ''
    for item in soup.find_all('h1', class_='top_title'):
        title = title + str(item.text)
        if title[0] == '[':
            title = title[title.index(']')+1:]
        else:
            pass
        title = re.sub(r'[…;]', '' , title)

        #print (item)
        #title = title + str(item.find_all(title=True))

    return title

#날짜 크롤링 함수
def get_date(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    date = ''
    date_num = ''
    for item in soup.find_all('li', class_='lasttime1'):
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
        #text = text + str(item.find_all(text=True))

        #s = re.sub(r'[^가-힣0-9]', " ", str(item))

        #s = re.sub(r'[!@#$&*():;="./|<>a-zA-Z]', repl, text)
        #summary = summary.replace('\n', ' ')
        #s = "\n".join(s.splitlines())
        summary = item
        #summary = s.replace("\n", ' ')

        #delete !@#$&*():;="./|<>a-zA-Z
        #print(summary)
    return summary

#본문 크롤링 함수
def get_bodytext(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('div', class_='art_txt'):
        #text = text + str(item.find_all(text=True))
        text = text + str(item.text)
        text = re.sub(';', '', text)
        if 'window.jQuery' in text:
            text = text[:text.index('window.jQuery')]
    return text

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


for page in range(1,679000):
    try:
        #출력파일명
        OUTPUT_FILE_NAME='/home/pirl/MK_2017/MK_2017_'+str(page)+'.txt'
        #크롤링할 URL
        URL='http://news.mk.co.kr/newsRead.php?sc=30000016&year=2017&no='+str(page)
        if get_title(URL) != "":
            main(URL, OUTPUT_FILE_NAME)
        else:
            pass
    except HTTPError:
        pass

# ~ 679000
# 2017년 매일경제 전부 크롤링
# 카테고리별 접속해서 번호 바꿔도 다른 기사랑 중복됨....