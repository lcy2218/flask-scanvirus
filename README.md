# 基于flask框架的在先扫描平台
在线恶意软件检测，调用www.virustotal.com提供的接口进行在线扫描

# 使用方式
python app.py  
依赖库请看requirement.txt  
pip install -r requirements.txt

# 具体功能
app.py用于启动服务器  
learning.py用于训练数据集  
checkpe.py用于检测文件是否安全  
uploadfile.py用于上传文件  

# 关于uploadfile.py
有时出现scan的error  
使用小飞机多试几次即可

# 数据库建表
create table user_info{
    id integer PRIMARY KEY AUTO_INCREMENT,
    u_ip varchar(20),
    u_md5 varchar(30),
    u_count integer,
    u_date date
};