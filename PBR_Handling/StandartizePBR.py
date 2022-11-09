# Convert pbrs folders to standart format with standart file names
import os
import os
import cv2
import numpy as np
import shutil
type="2K"
#intr="//AmbientCG_"
mainOutDir="/media/breakeroftime/SP PHD U3/Textures/NormalizedPBR/" # outpur dir, where normalized output will be 
if not os.path.exists(mainOutDir): os.mkdir(mainOutDir)
mainFolder="/media/breakeroftime/SP PHD U3/Textures/UnifiedTextures/" # input dir, with pbrs to normalize 

# standart texture maps names dictionary, the keys are the standart names
d={}
d["OriginColor."]=["Color.","color.","olor.", "COLOR","Color","color","lbedo.","LBEDO.","diff","Diffuse.","d.tif"]
d["Roughness."]=["ROUGHNESS.","roughnness.","oughness.","ROUGH.","roughness","ROUGHNESS","roughnness", "r.tif"]
d["Normal."]=["normal.","NORMAL.","Normal.","ormal.","NORM.","normal","NORMAL","Normal","nrm.", "n.tif"]
d["Height."]=["EIGHT.","eight.","DISP.","Disp.","disp.","height","isplacement", "h.tif","Bump.","Bumpiness.","BUMP.","BUMP"]
d["Metallic."]=["etallic.","etalness.","etal.","etalic.","ETAL.","ETALLIC.","ETALIC."]
d["AmbientOcclusion"]=["mbientOcclusion","ao.","AO.","OCC.","cclusion.","cclusion."] #Multiply by color
d["Specular."]=["Specular","specularLevel","pecular","pecularLevel","SPECULAR"]
d["Reflection"]=["Reflection.","eflection.","REFLECTIN."] # Innverse of specular
d["Glosinees"]=["Glossiness","Gloss"] # opposite of roughness


exceptions=0
for numfinished,f1 in enumerate(os.listdir(mainFolder)):
   # if not "4K" in f1: continue
    print(f1)
    p1=mainFolder+"/"+f1+"/"
    outd = {}
#-------------------------Create file list---------------------------------------------------------------------------------
    if os.path.isdir(p1): # All folders
           print("excerptions",exceptions,"Of",numfinished)
           for prp in d: # All file properties
                for nm in d[prp]:  # All names for property
                     for fl in os.listdir(p1): # all files in folder
                         if prp in outd: continue
                         if nm in fl:
                             outd[prp]=fl
#---------------------------Read resize maps-----------------------------------------------------------------------------
           #if not ((not "Specular." in outd) and ("Reflection" in outd)): continue
           if not "OriginColor." in outd:
               print(p1," Missing color")
               continue
           imgs={}
           for prp in outd:
               try:
                 imgs[prp]=cv2.imread(p1+outd[prp])
                 print(p1+outd[prp])
                 h,w,depth=imgs[prp].shape
               except:
                  print("Fail reading:",p1+outd[prp])
                  del imgs[prp]
                  exceptions+=1
                  continue
               r=2048.0/max([h,w])
               if r<1:
                   h = int(h * r)
                   w = int(w  * r)
                   imgs[prp]=cv2.resize(imgs[prp],[w,h])
                   # cv2.imshow("resize", cv2.resize(imgs[prp], (1000, 1000)))
                   # cv2.waitKey()
#----------------------------------Proccess maps----------------------------------------------------------------------
           if not "OriginColor." in imgs: continue
           if "AmbientOcclusion" in imgs:
                amb=imgs["AmbientOcclusion"].astype(np.float32)
                color=imgs["OriginColor."].astype(np.float32)
                imgs["AmbientColor."]=(color*amb/amb.max()).astype(np.uint8)#
                outd["AmbientColor."]=outd["OriginColor."]
                # cv2.imshow("Ambient",cv2.resize(np.hstack([imgs["Color."],imgs["AmbientColor."]]),(1000,500)))
                # cv2.waitKey()
           if (not "Specular." in imgs) and ("Reflection" in imgs):
               imgs["Specular."]=255-imgs["Reflection"]
               outd["Specular."] = outd["Reflection"]
               # cv2.imshow("Specular.", cv2.resize(np.hstack([imgs["Specular."], imgs["Reflection"]]),(1000,500)))
               # cv2.waitKey()
           if (not "Roughness." in imgs) and ("Glosinees" in imgs):
               imgs["Roughness."]=255-imgs["Glosinees"]
               outd["Roughness."] = outd["Glosinees"]
               # cv2.imshow("Roughness.", cv2.resize(np.hstack([imgs["Roughness."], imgs["Glosinees"]]),(1000,500)))
               # cv2.waitKey()
#----------------------------Save-----------------------------------------------------------------------------------
           outDir=mainOutDir+"/"+f1+"/"
           print(outDir)
           if not os.path.exists(outDir): os.mkdir(outDir)
           for fl in imgs:
               if "." in fl:
                   if ".jpg" or ".JPG" in outd[fl]:
                       ext="jpg"
                   else:
                       ext="png"
                   cv2.imwrite(outDir+fl+ext,imgs[fl])









