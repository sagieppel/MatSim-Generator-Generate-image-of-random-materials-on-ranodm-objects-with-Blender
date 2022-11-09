# Merge PBR materials to create new materials by taking the average of the maps

import os
import cv2
import numpy as np
ListDir=[]

indir="/media/breakeroftime/SP PHD U3/Textures/NormalizedPBR/"

#==================Create material list================================f==========================
for fld in os.listdir(indir):
        fld=indir+fld+"//"
        if os.path.isdir(fld):
            for nm in os.listdir(fld):
                if ("OriginOriginColor." in nm) :
                     os.rename(fld+nm,fld+nm.replace("OriginOrigin","Origin"))




