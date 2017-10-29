import json
import os
from pprint import pprint

for jsonFilename in os.listdir('dump'):
    with open("dump\\"+jsonFilename) as json_file:
        data = json.load(json_file)
        #pprint(data["text"])
        with open("dumpText\\justText.txt", 'a+') as fp:
            json.dump(data["text"]+"\n", fp)