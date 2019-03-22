import requests
import time
from multiprocessing import Process
import os
import logging
import logging.handlers

logger = logging.getLogger('client_program')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

handler = logging.handlers.TimedRotatingFileHandler("/home/centos/logs/client_log",'midnight',1)
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger.addHandler(handler)

processes = []
thread = int(os.environ.get('THREAD',3))
domain_name = os.environ.get('DOMAIN_NAME','http://os-sample-python-python-flask.okdexperimentation.gtrrt.click')
sleep_time = int(os.environ.get('SLEEP_TIME',3))

def query_server(domainname):
    start = time.time()
    r = requests.get(domainname)
    roundtrip = time.time() - start
    #print(r.status_code,roundtrip,os.getppid(),os.getpid(),r.headers['Date'])
    logger.info("%s - %s - %s - %s - %s",r.status_code,roundtrip,os.getppid(),os.getpid(),r.headers['Date'])

def f(domainname,delay):
    while(True):
        query_server(domainname)
        time.sleep(delay)

if __name__ == '__main__':
   # print("STATUS CODE,ROUND TRIP TIME,PARENT PROCESS ID,CHILD PROCESS ID,DATE")
    logger.info("STATUS CODE - ROUND TRIP TIME - PARENT PROCESS ID - CHILD PROCESS ID - DATE")
    for i in range(thread):
        p = Process(target=f, args=(domain_name,sleep_time,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
