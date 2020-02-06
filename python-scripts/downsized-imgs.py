# encoding=utf8
#!/usr/bin/python
import sys
import sys
import lycon
import glob
import os
reload(sys)
sys.setdefaultencoding('utf8')

for file in glob.glob(sys.argv[1]+"/*.jpg"):
    basename = os.path.basename(file) 
    # Print the basename name   
    outputDir = os.path.dirname(file) + "-downsized/"
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    img = lycon.load(file)
    resized = lycon.resize(img, width=512, height=512, interpolation=lycon.Interpolation.CUBIC)
    outputFile = outputDir + basename
    lycon.save(outputDir + basename, resized)
    print("ok: %s"%(outputFile))