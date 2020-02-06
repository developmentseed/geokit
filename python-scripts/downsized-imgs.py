# encoding=utf8
#!/usr/bin/python
import sys
import sys
import lycon
import glob
import os
import time
import numpy as np
import multiprocessing
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding('utf8')

inputDir = sys.argv[1]
outputDir = sys.argv[1].replace("\/", "") + "-downsized"
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


def downsized(file):
    basename = os.path.basename(file)
    img = lycon.load(file)
    resized = lycon.resize(img, width=512, height=512,
                           interpolation=lycon.Interpolation.CUBIC)
    lycon.save(outputDir + "/" + basename, resized)
    return outputDir + "/" + basename


def bashImages(chunk):
    for file in chunk:
        downsized(file)
    time.sleep(1)
    return len(glob.glob(outputDir+"/*.jpg"))


chunks = np.array_split(glob.glob(sys.argv[1]+"/*.jpg"), 200)
pool = Pool(processes=multiprocessing.cpu_count())
pool.map(bashImages, chunks)
print("Downsized: %s:%d,%s:%d" % (inputDir, len(
    glob.glob(inputDir+"/*.jpg")), outputDir, len(glob.glob(outputDir+"/*.jpg"))))
