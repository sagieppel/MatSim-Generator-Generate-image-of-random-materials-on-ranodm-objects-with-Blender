# Create new PBR materials by mixing texuture maps of exisiting materials
# Merge PBR materials to create new materials by taking the average of the maps

import os
import cv2
import numpy as np
ListDir=[]
#------------Input parameters-------------------------------------------------------------------------------------------------
indir="/scratch/a/aspuru/seppel/assets/NormalizedPBR/" # input folder of PBR to mix
mergdir="/scratch/a/aspuru/seppel/assets/Merged_NormalizedPBR//" # output folder where generated PBRs will be saved 
proplist=["OriginColor.","Roughness.","Normal.","Height.","Metallic.","Specular.","AmbientColor."] # properties to mix
#==================Create material list==========================================================
print("Making file list")
for fld in os.listdir(indir):
    ky = {}
    ky["name"] = fld
    fld=indir+"/"+fld+"/"
    if os.path.isdir(fld):
        for nm in os.listdir(fld):
            fl=fld+"//"+nm
            if os.path.isfile(fl):
                for l in proplist:
                             if l in nm: ky[l]=fl
        ListDir.append(ky)

#======================Merge materials========================================================"
if not os.path.exists(mergdir): os.mkdir(mergdir)

for i in range(500000):
    numMat=np.random.randint(2,5)
    drs=[]
    mergename = "Merge_"
    for iii in range(numMat): # Select folders to merge
       drs.append(ListDir[np.random.randint(len(ListDir))]) # Dirs to merge
       mergename +=drs[len(drs)-1]["name"]+"_"
    outdir=mergdir+"//"+mergename+"//"
    if os.path.exists(outdir): continue
    os.mkdir(outdir)
    for p in proplist:
         if p=="name": continue
         im=[]
         for d in drs:
              if ("AmbientColor." in d): # use either color or ambient but not both
                  if (not "OriginColor." in d) or (np.random.rand()<0.5):
                      d["OriginColor."]=d["AmbientColor."]
                  del d["AmbientColor."]


              if p in d:
                  im.append(cv2.imread(d[p]).astype(np.float32))

         if len(im)==0: continue
         for ff in  range(len(im)):
             if ff==0:
                 MainImage=im[0]/len(im)
             else:
                 if im[0].shape[0]!=im[ff].shape[0] or im[0].shape[1]!=im[ff].shape[1]:
                        im[ff]=cv2.resize(im[ff],(im[0].shape[1],im[0].shape[0]))
                 MainImage += im[ff]/len(im)
                 # cv2.imshow(p+str(ff),im)
                 # cv2.waitKey()
                 # cv2.destroyWindow()
         cv2.imwrite(outdir+"/"+p+"jpg",MainImage.astype(np.uint8))
    print(outdir+"/"+mergename+"Created")
    t=open(outdir+"/Finished.txt","w")
    t.close()
    t.close


