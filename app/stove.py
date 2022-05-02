import requests
from urllib import parse
from bs4 import BeautifulSoup
import json
import re

def mari_info():
    data = {}
    try:
        req = requests.get('https://m-lostark.game.onstove.com/Shop#mari')
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        c_info = soup.select('#shopMari')
        c_info2 = c_info[0].select('.for-mari')
        T3 = c_info2[0].select('.list-items--mari')
        T2 = c_info2[1].select('.list-items--mari')
        
        T3_list = T3[0].select('li')
        T2_list = T2[0].select('li')
        
        T3_data = []
        T2_data = []
        
        for i in range(len(T3_list)):
            T3_data.append({'name':T3_list[i].select('.item-name')[0].get_text(),'price':T3_list[i].select('em')[0].get_text()})
        for i in range(len(T2_list)):
            T2_data.append({'name':T2_list[i].select('.item-name')[0].get_text(),'price':T2_list[i].select('em')[0].get_text()})
        data['T3']=T3_data
        data['T2']=T2_data
        data['code']='ok'
    except Exception as e :
        data['code']='error'
        data['e']='not found item'
        #data['e']=e
    finally:
        return data
        #pass

def item_info(item_name):
    data = {}
    try:
        url = 'https://m-lostark.game.onstove.com/Market/GetMarketItemList'
        url_param = parse.urlparse('https://m-lostark.game.onstove.com/Market/GetMarketItemList?itemName='+item_name)
        url_query = parse.parse_qs(url_param.query)
        url_query2 = parse.urlencode(url_query, doseq=False)
        #print(url+'?'+url_query2)
        #req = requests.get(url+'?'+url_query2+'&isInit=false')
        req = requests.get('https://m-lostark.game.onstove.com/Market/GetMarketItemList?itemName='+item_name+'&isInit=false')
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        c_info = soup.select('li')
        data_arr = []
        for i in range(len(c_info)):
            temp_arr = {}
            temp_arr['item_name']=c_info[i].select('.name')[0].get_text()
            temp_arr['current_price']=c_info[i].select('.list__detail')[0].select('tr')[0].select('em')[0].get_text()
            temp_arr['avg_price']=c_info[i].select('.list__detail')[0].select('tr')[1].select('em')[0].get_text()
            temp_arr['last_price']=c_info[i].select('.list__detail')[0].select('tr')[2].select('em')[0].get_text()
            if(len(c_info[i].select('.count'))>0):
                temp_arr['count']=c_info[i].select('.count')[0].get_text()
            else:
                temp_arr['count']=''
            data_arr.append(temp_arr)
        data['data']=data_arr
        #return c_info
    except Exception as e :
        data['code']='error'
        data['e']='not found item'
        #data['e']=e
    finally:
        return data
        #pass

def character_info(user_name):
    data = {}
    try:
        req = requests.get('https://m-lostark.game.onstove.com/Profile/Character/'+user_name)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        data['user_name']=user_name

        c_info = soup.select('.myinfo__contents-character')

        if(len(c_info)==0):
            data['code']='error'
            return data

        data['code']='ok'

        data['c_level']=c_info[0].select('.myinfo__character--button2 span')[0].get_text()

        c_info = c_info[0].select('.wrapper-define')

        #서버
        data['server']=c_info[0].get_text('|',strip=True).split('|')[1].replace('@','')
        #직업
        data['class']=c_info[0].get_text('|',strip=True).split('|')[3].replace('@','')

        #원정대 레벨
        data['w_level']=c_info[1].get_text('|',strip=True).split('|')[1].replace('@','')
        #칭호
        data['title']=c_info[1].get_text('|',strip=True).split('|')[3].replace('@','')

        #레벨
        data['level']=c_info[2].select('.item dd')[0].get_text()

        #길드명
        data['guild']=c_info[3].select('.guild-name')[0].get_text()

        #영지
        data['area']=c_info[4].select('dd')[0].get_text()

        script_data = {}

        script = soup.select('script')
        script = script[2].string.replace('\t','').replace('\r\n','').replace('$.Profile = ','').replace('\\','').replace(';','')

        script_data = json.loads(script)
        '''
        #카드
        script_data['Card']
        #카드셋
        script_data['CardSet']
        #장비
        script_data['Equip']
        #스킬
        script_data['Skill']
        '''
        equip_data = {}
        equip_img = {}
        equip_quality = {}

        equip = soup.select('.profile-equipment__slot')

        #범위는 0~11까지
        #머리
        for i in range(len(equip[0].select('.profile-item'))):
            if(equip[0].select('.profile-item')[i].attrs.get('data-item',None)[:1]=="E"):
                equip_data['00'+str(i)] = equip[0].select('.profile-item')[i].attrs.get('data-item',None)
                equip_img['00'+str(i)] = script_data['Equip'][equip_data['00'+str(i)]]['Element_001']['value']['slotData']['iconPath']
                equip_quality['00'+str(i)] = script_data['Equip'][equip_data['00'+str(i)]]['Element_001']['value']['qualityValue']
                equip_data['00'+str(i)] = re.sub('<.+?>', '', script_data['Equip'][equip_data['00'+str(i)]]['Element_000']['value'], 0, re.I|re.S)

        #각인
        c_info2 = soup.select('.profile-tab');
        temp = c_info2[0].select('.profile-ability-engrave')
        temp2 = temp[0].select('li')
        ablity= []
        for i in range(len(temp2)):
            ablity.append(temp2[i].select('span')[0].get_text())
        
        #data['script']=script_data
        data['equip']=equip_data
        data['equip_img']=equip_img
        data['equip_quality']=equip_quality
        data['ablity']=ablity
        
        #스텟
        c_info3 = soup.select('.profile-ability-basic')
        
        data['attack']= c_info3[0].select('li')[0].select('span')[1].get_text()
        data['hp']= c_info3[0].select('li')[4].select('span')[1].get_text()
        
        data['stat1']=c_info3[1].select('span')[1].get_text() #치
        data['stat2']=c_info3[1].select('span')[3].get_text() #특
        data['stat3']=c_info3[1].select('span')[5].get_text() #제
        data['stat4']=c_info3[1].select('span')[7].get_text() #신
        data['stat5']=c_info3[1].select('span')[9].get_text() #인
        data['stat6']=c_info3[1].select('span')[11].get_text() #숙
                
    except Exception as e :
        data['code']='error'
        data['e']=e
    finally:
        return data
