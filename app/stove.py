import requests
from bs4 import BeautifulSoup
import json
import re

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

        equip = soup.select('.profile-equipment__slot')

        #범위는 0~11까지
        #머리
        for i in range(len(equip[0].select('.profile-item'))):
            equip_data['00'+str(i)] = equip[0].select('.profile-item')[i].attrs.get('data-item',None)
            equip_img['00'+str(i)] = script_data['Equip'][equip_data['00'+str(i)]]['Element_001']['value']['slotData']['iconPath']
            equip_data['00'+str(i)] = re.sub('<.+?>', '', script_data['Equip'][equip_data['00'+str(i)]]['Element_000']['value'], 0, re.I|re.S)

        #각인
        
        c_info2 = soup.select('.profile-tab');
        temp = c_info2[0].select('.profile-ability-engrave')
        temp2 = temp[0].select('li')
        ablity= []
        for i in range(len(temp2)):
            ablity.append(temp2[i].select('span')[0].get_text())
        
        data['script']=script_data
        data['equip']=equip_data
        data['equip_img']=equip_img
        data['ablity']=ablity
        
    except Exception as e :
        data['code']='error'
        data['e']=e
    finally:
        return data
