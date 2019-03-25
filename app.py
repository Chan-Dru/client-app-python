import requests
import time
from multiprocessing import Process
import os
import logging
import logging.handlers
import datetime

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
thread = int(os.environ.get('THREAD',50))
domain_name = os.environ.get('DOMAIN_NAME','http://os-sample-python-python-flask-new.okdexperimentation.gtrrt.click')
sleep_time = int(os.environ.get('SLEEP_TIME',1))
timeout_duration = int(os.environ.get('TIMEOUT_DURATION',5))

def query_server(domainname):
    try:
      start = datetime.datetime.now()
      r = requests.get(domainname,timeout=timeout_duration)
      roundtrip = datetime.datetime.now() - start
      #print(r.status_code,roundtrip,os.getppid(),os.getpid(),r.headers['Date'])
      status_code = r.status_code
      #response = r.text
      if status_code != 200:
        response = "The Host not exists"
        print(r)
        #print(r.text)
        logger.info("%s - %s - %s - %s - %s - %s",start,r.status_code,roundtrip.total_seconds(),os.getppid(),os.getpid(),response)
      else:
        logger.info("%s - %s - %s - %s - %s - %s",start,r.status_code,roundtrip.total_seconds(),os.getppid(),os.getpid(),r.text)
    except requests.exceptions.ReadTimeout:
        roundtrip = datetime.datetime.now() - start
        logger.info("%s - %s - %s - %s - %s - %s",start,504,roundtrip.total_seconds(),os.getppid(),os.getpid(),"The Request Timeout")

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
