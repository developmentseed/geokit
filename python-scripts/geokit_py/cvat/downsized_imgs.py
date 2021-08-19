"""cvat.downsized_imgs: Skeleton of a function."""

import glob
import os

import lycon


def downsized_imgs(inputDir, outputDir):
    """An Awesome doc."""

    os.makedirs(outputDir, exist_ok=True)

    for file in glob.glob(f"{inputDir}/*.jpg"):
        basename = os.path.basename(file)
        img = lycon.load(file)
        resized = lycon.resize(
            img, width=512, height=512, interpolation=lycon.Interpolation.CUBIC
        )
        lycon.save(outputDir + "/" + basename, resized)
    files_input = len(glob.glob(f"{inputDir}/*.jpg"))
    files_output = len(glob.glob(f"{outputDir}/*.jpg"))

    print(f"Downsized: {inputDir}:{files_input}, {outputDir}:{files_output}")
