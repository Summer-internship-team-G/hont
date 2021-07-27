from flask import Flask, request, jsonify, redirect, make_response
import requests
from bs4 import BeautifulSoup


#사전
dic = {
    "chest": ['가슴','가슴 근육','가슴 운동'],
    "forearms" : ['팔뚝','팔','팔근육'],
    "lats":['광배근','등','등근육'],
    "middle-back":[ '엉덩이 위', '갈비뼈 아래','척추'],
    "lower-back" : ['허리','요추'],
    "quadriceps":['넙다리네갈래근', '사두근', '허벅지 앞 근육','다리'],
    "hamstrings" : ['허벅지 뒤','허벅지','다리'],
    "calves":['종아리','다리'],
    "triceps" :['삼두근' , '팔 위쪽','팔','팔근육'],
    "traps":['등','척추'],
    "abdominals": ['배','복부'],
    "glutes" :['둔근', '엉덩이'],
    "biceps" :['이두근', '팔'],
    "adductors" :['내전근', '허벅지','다리'],
    "abductors" :["외전근", "다리",'허벅지'],
    "neck": ['목','목덜미'],
    "shoulders": ['어깨','어깨 근육']
}


#밸류값으로 키값 구하기
def find_key(dic,val):
    for key in dic:
        for i in range(len(dic[key])):
            if(val==dic[key][i]):
                return key


def crawling_data(val):
    url="https://www.bodybuilding.com/exercises/muscle/"+find_key(dic,val)
    data=requests.get(url)
    soup=BeautifulSoup(data.text,'html.parser')
    result_dict=[]
    threeall = soup.select('#js-ex-category-body > div.ExCategory-results > div')
    id=0
    for each in threeall:
        
        n=each.select_one('div.ExResult-cell.ExResult-cell--nameEtc > h3 > a')
        t=each.select_one('div.ExResult-cell.ExResult-cell--nameEtc > div.ExResult-details.ExResult-equipmentType > a')
        i=each.select_one('img')
        if n is not None:
            id+=1
            seq_map = {"id": id,"name": n.get_text().replace('\n','').strip(), "tool": t.get_text().replace('\n','').strip(), "image": i["src"]}
            result_dict.append(seq_map)
    return result_dict


class Search:
    def findSearch(self):
        search_string = request.get_json()
        search_data = search_string['type']
        result=crawling_data(search_data)
        return jsonify(result)
   