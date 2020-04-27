import requests
import json

def getFileScanId(url,apikey,a,b):
    # /file/scan
    # /文件/扫描
    # 上传并扫描文件
    # 限制为32MB
    params = {'apikey': apikey}
    files = {'file': (a, open(b, 'rb'))}
    response = requests.post(url, files=files, params=params)
    my_scan_id = str(response.json()['scan_id'])
    return my_scan_id

def getFieReportResult(url,apikey,my_scan_id):
    #/file/report
    # /文件/报告
    # 检索文件扫描报告
    #该resource参数可以是要获取最新的病毒报告文件的MD5，SHA-1或SHA-256。
    #还可以指定/ file / scan端点scan_id返回的值。
    #如果allinfo参数设置为true除了返回防病毒结果之外的其他信息。
    get_params = {'apikey': apikey, 'resource': my_scan_id,'allinfo': '1'}
    response2 = requests.get(url, params=get_params)
    jsondata = json.loads(response2.text)
    with open("jsonResult.json","w") as f:
        json.dump(jsondata, f, indent=4)
    return jsondata

def getResult(json):
    result = {}
    for k,v in json["scans"].items():
        result[k] = v['detected']
    print(result)
    print("一共有{0}条杀毒数据".format(len(result)))
    with open("result.txt","w") as g:
        g.write(str(result))

def uploadFile(file_name, file_src):
    #file_name = input("请输入文件名:")
    a = file_name
    #file_src  = input("请输入文件路径:")
    b = file_src

    # url1 = 'https://www.virustotal.com/vtapi/v2/file/scan'
    # url2 = "https://www.virustotal.com/vtapi/v2/file/report"
    # #需要提供密钥，否者会出现403错误
    # apikey = "968e3bc6d33c79c2b957696cf53b3f7c9c607411ee623e67dd3b57d52f8986e4"

    # #获得文件scan_id
    # scan_id = getFileScanId(url1,apikey,a,b)
    # #获得返回的json结果并写入result文件
    # #getFieReportResult(url2, apikey, scan_id)
    # json = getFieReportResult(url2,apikey,scan_id)

    #用于模拟发用数据
    json = {'scans':{'Bkav': {'detected': False, 'version': '1.3.0.9899', 'result': None, 'update': '20200415'}, 
    'DrWeb': {'detected': False, 'version': '7.0.46.3050', 'result': None, 'update': '20200416'}, 
    'MicroWorld-eScan': {'detected': False, 'version': '14.0.409.0', 'result': None, 'update': '20200416'}, 
    'VBA32': {'detected': False, 'version': '4.3.0', 'result': None, 'update': '20200415'}, 
    'CMC': {'detected': False, 'version': '1.1.0.977', 'result': None, 'update': '20190321'}, 
    'CAT-QuickHeal': {'detected': False, 'version': '14.00', 'result': None, 'update': '20200415'}, 
    'ALYac': {'detected': False, 'version': '1.1.1.5', 'result': None, 'update': '20200416'}, 
    'Cylance': {'detected': False, 'version': '2.3.1.101', 'result': None, 'update': '20200416'}, 
    'Zillya': {'detected': False, 'version': '2.0.0.4069', 'result': None, 'update': '20200415'}, 
    'SUPERAntiSpyware': {'detected': False, 'version': '5.6.0.1032', 'result': None, 'update': '20200415'}, 
    'Sangfor': {'detected': False, 'version': '1.0', 'result': None, 'update': '20200412'}, 
    'K7AntiVirus': {'detected': False, 'version': '11.102.33708', 'result': None, 'update': '20200407'}, 
    'Alibaba': {'detected': False, 'version': '0.3.0.5', 'result': None, 'update': '20190527'}, 
    'K7GW': {'detected': False, 'version': '11.103.33809', 'result': None, 'update': '20200415'}, 
    'Cybereason': {'detected': False, 'version': '1.2.449', 'result': None, 'update': '20190616'}, 
    'Arcabit': {'detected': False, 'version': '1.0.0.870', 'result': None, 'update': '20200415'}, 
    'Invincea': {'detected': False, 'version': '6.3.6.26157', 'result': None, 'update': '20200407'}, 
    'BitDefenderTheta': {'detected': False, 'version': '7.2.37796.0', 'result': None, 'update': '20200408'}, 
    'F-Prot': {'detected': False, 'version': '4.7.1.166', 'result': None, 'update': '20200416'}, 'Symantec': {'detected': False, 'version': '1.11.0.0', 'result': None, 'update': '20200415'}, 'TotalDefense': {'detected': False, 'version': '37.1.62.1', 'result': None, 'update': '20200415'}, 'Zoner': {'detected': False, 'version': '0.0.0.0', 'result': None, 'update': '20200415'}, 'TrendMicro-HouseCall': {'detected': False, 'version': '10.0.0.1040', 'result': None, 'update': '20200416'}, 'Avast': {'detected': False, 'version': '18.4.3895.0', 'result': None, 'update': '20200415'}, 'ClamAV': {'detected': False, 'version': '0.102.2.0', 'result': None, 'update': '20200415'}, 'Kaspersky': {'detected': False, 'version': '15.0.1.13', 'result': None, 'update': '20200416'}, 'BitDefender': {'detected': False, 'version': '7.2', 'result': None, 'update': '20200416'}, 'NANO-Antivirus': {'detected': False, 'version': '1.0.134.25032', 'result': None, 'update': '20200416'}, 'Paloalto': {'detected': False, 'version': '1.0', 'result': None, 'update': '20200416'}, 'AegisLab': {'detected': False, 'version': '4.2', 'result': None, 'update': '20200416'}, 'Rising': {'detected': False, 'version': '25.0.0.24', 'result': None, 'update': '20200416'}, 'Endgame': {'detected': False, 'version': '3.0.17', 'result': None, 'update': '20200226'}, 'Sophos': {'detected': False, 'version': '4.98.0', 'result': None, 'update': '20200416'}, 'Comodo': {'detected': False, 'version': '32328', 'result': None, 'update': '20200415'}, 'F-Secure': {'detected': False, 'version': '12.0.86.52', 'result': None, 'update': '20200416'}, 'Baidu': {'detected': False, 'version': '1.0.0.2', 'result': None, 'update': '20190318'}, 'VIPRE': {'detected': False, 'version': '83012', 'result': None, 
    'update': '20200416'}, 
    'TrendMicro': {'detected': False, 'version': '11.0.0.1006', 'result': None, 'update': '20200416'}, 
    'McAfee-GW-Edition': {'detected': False, 'version': 'v2017.3010', 'result': None, 'update': '20200415'}, 
    'Trapmine': {'detected': False, 'version': '3.2.22.914', 'result': None, 'update': '20200123'}, 
    'FireEye': {'detected': False, 'version': '32.31.0.0', 'result': None, 'update': '20200316'}, 
    'Emsisoft': {'detected': False, 'version': '2018.12.0.1641', 'result': None, 'update': '20200416'}, 
    'Ikarus': {'detected': False, 'version': '0.1.5.2', 'result': None, 'update': '20200415'}, 
    'Cyren': {'detected': False, 'version': '6.2.2.2', 'result': None, 'update': '20200416'}, 
    'Jiangmin': {'detected': False, 'version': '16.0.100', 'result': None, 'update': '20200415'}, 
    'eGambit': {'detected': False, 'version': None, 'result': None, 'update': '20200416'}, 
    'Avira': {'detected': False, 'version': '8.3.3.8', 'result': None, 'update': '20200415'}, 
    'MAX': {'detected': False, 'version': '2019.9.16.1', 'result': None, 'update': '20200416'}, 
    'Antiy-AVL': {'detected': False, 'version': '3.0.0.1', 'result': None, 'update': '20200416'}, 
    'Kingsoft': {'detected': False, 'version': '2013.8.14.323', 'result': None, 'update': '20200416'}, 
    'Microsoft': {'detected': False, 'version': '1.1.16900.4', 'result': None, 'update': '20200415'}, 'ViRobot': {'detected': False, 'version': '2014.3.20.0', 'result': None, 'update': '20200415'}, 'ZoneAlarm': {'detected': False, 'version': '1.0', 'result': None, 'update': '20200416'}, 'Avast-Mobile': {'detected': False, 'version': '200415-00', 'result': None, 'update': '20200415'}, 'GData': {'detected': False, 'version': 'A:25.25419B:26.18390', 'result': None, 'update': '20200416'}, 'AhnLab-V3': {'detected': False, 'version': '3.17.4.26996', 'result': None, 'update': '20200415'}, 'Acronis': {'detected': False, 'version': '1.1.1.75', 'result': None, 'update': '20200409'}, 'McAfee': {'detected': False, 'version': '6.0.6.653', 'result': None, 'update': '20200416'}, 'TACHYON': {'detected': False, 'version': '2020-04-16.01', 'result': None, 'update': '20200416'}, 'Ad-Aware': {'detected': False, 'version': '3.0.5.370', 'result': None, 'update': '20200416'},
    'Malwarebytes': {'detected': False, 'version': '3.6.4.335', 'result': None, 'update': '20200416'},
    'APEX': {'detected': False, 'version': '6.11', 'result': None, 'update': '20200413'}, 
    'ESET-NOD32': {'detected': False, 'version': 
    '21172', 'result': None, 'update': '20200416'}, 
    'Tencent': {'detected': False, 'version': '1.0.0.1', 'result': None, 'update': '20200416'}, 
    'Yandex': {'detected': False, 'version': '5.5.2.24', 'result': None, 'update': '20200415'}, 
    'SentinelOne': {'detected': False, 'version': '2.1.0.89', 'result': None, 'update': '20200406'}, 
    'MaxSecure': {'detected': False, 'version': '1.0.0.1', 'result': None, 'update': '20200415'}, 
    'Fortinet': {'detected': False, 'version': '6.2.142.0', 'result': None, 'update': '20200416'}, 
    'Webroot': {'detected': False, 'version': '1.0.0.403', 'result': None, 'update': '20200416'}, 
    'AVG': {'detected': False, 'version': '18.4.3895.0', 'result': None, 'update': '20200415'}, 
    'Panda': {'detected': False, 'version': '4.6.4.2', 'result': None, 'update': '20200415'}, 
    'CrowdStrike': {'detected': False, 'version': '1.0', 'result': None, 'update': '20190702'}, 
    'Qihoo-360': {'detected': False, 'version': '1.0.0.1120', 'result': None, 'update': '20200416'}}}
    data = json["scans"]
    mylist =[]
    mydict = {
        'name': '',
        'version' : '',
        'detected' : ''
    }
    #i = 0
    for key in data:
        mydict['name'] = key
        mydict['version'] = data[key]["version"]
        mydict['detected'] = data[key]["detected"]
        #不使用copy的话会导致列表元素完全相同
        mylist.append(mydict.copy())

    return mylist





