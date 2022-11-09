import os
import shutil
type="2K"
#intr="//AmbientCG_"
mainOutDir="/media/breakeroftime/SP PHD U3/Textures/UnifiedTextures/"
if not os.path.exists(mainOutDir): os.mkdir(mainOutDir)
mainFolder="/media/breakeroftime/SP PHD U3/Textures/UnifiedTextures/"


for f1 in os.listdir(mainFolder):
    p1=mainFolder+"/"+f1+"/"
    if os.path.isdir(p1):
           for f2 in os.listdir(p1):
               p2 = p1 + "/" + f2 + "/"
               if os.path.isdir(p2):
                   os.rename(p2, mainOutDir +  f1 +"_"+ f2)
                   print(p2, "-->", mainOutDir +  f1+"_"+f2)


                     #   print("--------------------------------------")