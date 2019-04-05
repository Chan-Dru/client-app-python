import os
import sys
import time
import configparser
import logging
import logging.handlers
import codecs

logger = logging.getLogger('client_program')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



config = configparser.ConfigParser()
config.read('server-configuration.properties', encoding='utf-8')
# config.readfp(codecs.open("server-configuration.properties", "r", "utf8"))


def server(time_string):
    # fileName = str(sys.argv[1]+time_string)
    fileName = "server_log"
    handler = logging.handlers.TimedRotatingFileHandler(fileName,'midnight',1)
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    namespace = str(config["Project"]["Name"])
    initialPodCount = int(config["Pod"]["InitialCount"])
    maxPodCount = int(config["Pod"]["FinalCount"])
    podStepCount = int(config["Pod"]["StepCount"])
    stepDuration = int(config["Pod"]["StepDurationSeconds"])
    commandFlag = str(config["Command"]["Flag"])
    command = str(config["Command"][commandFlag])
    s3_bucket = str(config["Storage"]["s3_bucket"])
    print(type(initialPodCount))
    
    if(initialPodCount<maxPodCount):
        PodsList = range(initialPodCount,maxPodCount+1,podStepCount)[1:]     
    else:
        PodsList = range(maxPodCount,initialPodCount+1,podStepCount)[::-1][1:]
    
    logger.info("program scale up in the range"+str(PodsList))
    logger.info("Initial Pod Count "+str(initialPodCount))
    command = command.replace("NAMESPACE",namespace)
        
    for i in PodsList:
        time.sleep(stepDuration)
        logger.info("Scale Pod to "+str(i))
        os.system(command.replace("REPLICAS",str(i)))
        #time.sleep(stepDuration)
    # logger.info("Scaling is done")
    # os.system("aws s3 cp "+fileName+" "+s3_bucket)

        
if __name__=="__main__":
    print(sys.argv)
    if (len(sys.argv)==2):
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%m_%d_%Y_%H_%M", named_tuple)
        server(time_string)
    else:
        print("Please provide the file name")