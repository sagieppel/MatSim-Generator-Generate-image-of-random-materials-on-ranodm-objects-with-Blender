# Merge PBR materials to create new materials by taking the average of the maps

import os
import cv2
import numpy as np
ListDir=[]

indir="/media/breakeroftime/2T/AmbientCG_2K_PBR//"
mergdir="/media/breakeroftime/2T/AmbientCG_2K_PBR_MERGED//"
proplist=["Displacement","Color","Roughness","Normal","AmbientOcclusion","Metallness","Metalness","Opacity","Emission"]
#==================Create material list==========================================================
for fld in os.listdir(indir):
    ky = {}
    ky["name"] = fld
    fld=indir+"/"+fld+"/"
    if os.path.isdir(fld):
        for nm in os.listdir(fld):
            fl=fld+"//"+nm
            print(nm)
            if (".jpg" in nm) or (".png" in nm) or (".PNG" in nm) or (".JPG" in nm):

               for l in proplist:
                      if l in nm: ky[l.replace("Metallness.","Metalness.")]=fl
        ListDir.append(ky)

#======================Merge materials========================================================"
if not os.path.exists(mergdir): os.mkdir(mergdir)

for i in range(50000):
    k1=np.random.randint(len(ListDir))
    k2 = np.random.randint(len(ListDir))
    if k1==k2: continue
    drs=[ListDir[k1],ListDir[k2]]
    mergename="Merge_"+drs[0]["name"]+"_"+drs[1]["name"]
    outdir=mergdir+"//"+mergename+"//"
    if os.path.exists(outdir): continue
    os.mkdir(outdir)
    for p in proplist:
         if p=="name": continue
         im=[]
         for d in drs:
              if p in d:
                  im.append(cv2.imread(d[p]))

         if len(im)==0: continue
         if len(im) == 1:
             im=im[0]
         if len(im) == 2:
                 if im[0].shape[0]!=im[1].shape[0] or im[0].shape[1]!=im[1].shape[1]:
                     im[1]=cv2.resize(im[1],(im[0].shape[1],im[0].shape[0]))
                 im = (im[0]).astype(np.float32)/2 + (im[1]/2).astype(np.float32)/2
         cv2.imwrite(outdir+"/"+mergename+"_"+p+".jpg",im.astype(np.uint8))
         print(outdir+"/"+mergename+"_"+p+".jpg")
    t=open(outdir+"/Finished.txt","w")
    t.close


