# Marge the folders of PBRS downloaded from the texture BOX website to a standard structure
import os
import shutil
type="2K"
intr="//TextureBox2_"
mainOutDir="/media/breakeroftime/SP PHD U3/Textures/UnifiedTextures/"
if not os.path.exists(mainOutDir): os.mkdir(mainOutDir)
mainFolder="/media/breakeroftime/SP PHD U3/Textures/TextureBOx/2/"

for f1 in os.listdir(mainFolder):
    p1=mainFolder+"/"+f1+"/"
    if os.path.isdir(p1):
           for f2 in os.listdir(p1):
               p2 = p1 + "/" + f2 + "/"
               if os.path.isdir(p2):
              #     print(p2)
                  if not os.path.exists(mainOutDir + intr + f2):
                        os.rename(p2,mainOutDir+intr+f2)
                        print(p2, "-->", mainOutDir + intr + f2)
                   # for f3 in os.listdir(p2):
                   #     p3 = p2 + "/" + f3 + "/"
                   #     if os.path.isdir(p3) and type in p3:
                   #         if not os.path.exists(mainOutDir+intr+f3):
                   #            os.rename(p3,mainOutDir+intr+f3)
                   #            print(p3,"-->",mainOutDir+intr+f3)

                     #   print("--------------------------------------")
