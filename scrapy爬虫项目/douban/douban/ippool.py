import requests
from threading import Timer
import time

def get_proxy():
    datas = requests.get("http://piping.mogumiao.com/\
    proxy/api/get_ip_bs?appKey=09b8e2ffdc2a4fac90349d6\
    3699553ec&count=10&expiryDate=0&format=2").content.decode('utf-8')
    print(datas)
    ips = datas.split('\r\n')
    with open('proxies.txt', 'w') as f:  
        for ip in ips:  
            f.write(ip+'\n')
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        
while True:
    get_proxy()
    time.sleep(5)