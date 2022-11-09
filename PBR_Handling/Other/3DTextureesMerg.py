import os
import shutil
type="2K"
intr="//AmbientCG_"
mainOutDir="/media/breakeroftime/SP PHD U3/Textures/UnifiedTextures/"
if not os.path.exists(mainOutDir): os.mkdir(mainOutDir)
mainFolder="//media/breakeroftime/SP PHD U3/Textures/AmbientCG_2K_PBR/"

for f1 in os.listdir(mainFolder):
    p1=mainFolder+"/"+f1+"/"
    if os.path.isdir(p1):
                  if not os.path.exists(mainOutDir + intr + f1):
                        os.rename(p1,mainOutDir+intr+f1)
                        print(p1, "-->", mainOutDir + intr + f1)
                   # for f3 in os.listdir(p2):
                   #     p3 = p2 + "/" + f3 + "/"
                   #     if os.path.isdir(p3) and type in p3:
                   #         if not os.path.exists(mainOutDir+intr+f3):
                   #            os.rename(p3,mainOutDir+intr+f3)
                   #            print(p3,"-->",mainOutDir+intr+f3)

                     #   print("--------------------------------------")