# Use to merge all the PBR sub folder for the  CGBookCases website https://www.cgbookcase.com/
import os
import shutil
type="2K"
intr="//CGBookCases_"
mainOutDir="/media/breakeroftime/SP PHD U3/Textures/UnifiedTextures/"
if not os.path.exists(mainOutDir): os.mkdir(mainOutDir)
mainFolder="/media/breakeroftime/SP PHD U3/Textures/CGBookCases/"

for f1 in os.listdir(mainFolder):
    p1=mainFolder+"/"+f1+"/"
    if os.path.isdir(p1):
           for f2 in os.listdir(p1):
               p2 = p1 + "/" + f2 + "/"
               if os.path.isdir(p2):
                   for f3 in os.listdir(p2):
                       p3 = p2 + "/" + f3 + "/"
                       if os.path.isdir(p3) and type in p3:
                           os.rename(p3,mainOutDir+type+f3)
                           print(p3,"-->",mainOutDir+type+f3)

                           print("--------------------------------------")
