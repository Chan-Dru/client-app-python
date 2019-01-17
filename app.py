import requests
import time
from multiprocessing import Process
import os

processes = []
thread = int(os.environ.get('THREAD',3))
# domain_name = os.environ.get('DOMAIN_NAME','http://flaskapp.openshiftnode.gtrrt.click/')
domain_name = os.environ.get('DOMAIN_NAME','http://flask-app-chaosproject.router.default.svc.cluster.local')
sleep_time = int(os.environ.get('SLEEP_TIME',3))

def query_server(domainname):
    start = time.time()
    r = requests.get(domainname)
    roundtrip = time.time() - start
    print(r.status_code,roundtrip,os.getppid(),os.getpid(),r.headers['Date'])

def f(domainname,delay):
    while(True):
        query_server(domainname)
        time.sleep(delay)

if __name__ == '__main__':
    print("STATUS CODE,ROUND TRIP TIME,PARENT PROCESS ID,CHILD PROCESS ID,DATE")
    for i in range(thread):
        p = Process(target=f, args=(domain_name,sleep_time,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()