import requests
import json
import file_result.result

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

    url1 = 'https://www.virustotal.com/vtapi/v2/file/scan'
    url2 = "https://www.virustotal.com/vtapi/v2/file/report"
    # #需要提供密钥，否者会出现403错误
    apikey = "968e3bc6d33c79c2b957696cf53b3f7c9c607411ee623e67dd3b57d52f8986e4"

    # #获得文件scan_id
    # scan_id = getFileScanId(url1,apikey,a,b)
    # #获得返回的json结果并写入result文件
    # #getFieReportResult(url2, apikey, scan_id)
    # json = getFieReportResult(url2,apikey,scan_id)

    json = file_result.result.pick_file(file_name)
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





