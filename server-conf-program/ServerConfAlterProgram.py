import os
import time
import configparser
import logging
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

initialPodCount = int(config["Pod"]["InitialCount"])
maxPodCount = int(config["Pod"]["MaxCount"])
podStepCount = int(config["Pod"]["StepCount"])
stepDuration = int(config["Pod"]["StepDurationSeconds"])
commandFlag = str(config["Command"]["Flag"])
command = str(config["Command"][commandFlag])
print(type(initialPodCount))

logger.info("program scale up in the range"+str(range(initialPodCount,maxPodCount,podStepCount)))
logger.info("Initial Pod Count "+initialPodCount)
for i in range(initialPodCount,maxPodCount+1,podStepCount):
    time.sleep(stepDuration)
    logger.info("Scale Pod to "+str(i))
    os.system(command.replace("##",str(i)))
    