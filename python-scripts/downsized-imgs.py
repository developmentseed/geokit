# encoding=utf8
#!/usr/bin/python
import sys
import sys
import lycon
import glob
import os
import time

reload(sys)
sys.setdefaultencoding('utf8')

inputDir = sys.argv[1]
outputDir = sys.argv[1].replace("\/", "")  + "-downsized"
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

for file in glob.glob(sys.argv[1]+"/*.jpg"):
    basename = os.path.basename(file)
    img = lycon.load(file)
    resized = lycon.resize(img, width=512, height=512, interpolation=lycon.Interpolation.CUBIC)
    lycon.save(outputDir + "/" +basename, resized)
print("Downsized: %s:%d,%s:%d"%(inputDir,len(glob.glob(inputDir+"/*.jpg")),outputDir,len(glob.glob(outputDir+"/*.jpg"))))