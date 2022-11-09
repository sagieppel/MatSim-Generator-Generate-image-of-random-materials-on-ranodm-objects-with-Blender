import os
import os
import cv2
import numpy as np
import shutil

mainOutDir="/media/breakeroftime/SP PHD U3/Textures/NormalizedPBRDefect/"
if not os.path.exists(mainOutDir): os.mkdir(mainOutDir)
mainOutFix="/media/breakeroftime/SP PHD U3/Textures/NormalizedPBRFix/"
if not os.path.exists(mainOutFix): os.mkdir(mainOutFix)

mainFolder="/media/breakeroftime/SP PHD U3/Textures/NormalizedPBR/"

# d={}
# d["Color."]=["Color.","color.","olor.", "COLOR","Color","color","lbedo.","LBEDO.","diff","Diffuse.","d.tif"]
# d["Roughness."]=["ROUGHNESS.","roughnness.","oughness.","ROUGH.","roughness","ROUGHNESS","roughnness", "r.tif"]
# d["Normal."]=["normal.","NORMAL.","Normal.","ormal.","NORM.","normal","NORMAL","Normal","nrm.", "n.tif"]
# d["Height."]=["EIGHT.","eight.","DISP.","Disp.","disp.","height","isplacement", "h.tif","Bump.","Bumpiness.","BUMP.","BUMP"]
# d["Metallic."]=["etallic.","etalness.","etal.","etalic.","ETAL.","ETALLIC.","ETALIC."]
# d["AmbientOcclusion"]=["mbientOcclusion","ao.","AO.","OCC.","cclusion.","cclusion."] #Multiply by color
# d["Specular."]=["Specular","specularLevel","pecular","pecularLevel","SPECULAR"]
# d["Reflection"]=["Reflection.","eflection.","REFLECTIN."] # Innverse of specular
# d["Glosinees"]=["Glossiness","Gloss"] # opposite of roughness
#
foldList=os.listdir(mainFolder)
for numfinished,f1 in enumerate(foldList):
    print(numfinished,f1)
    if "AmbientCG" in f1: continue
    p1=mainFolder+"/"+f1+"/"
#-------------------------Create file list---------------------------------------------------------------------------------
    im={}
    if os.path.isdir(p1) and not os.path.exists(p1+"checked.txt"): # All folders
                     for fl in os.listdir(p1): # all files in folder
                        if "Color." in fl:
                          if "AmbientColor." in fl: # read image
                              nm="Ambient"
                          else:
                              nm="Color"
                          im[nm]=cv2.resize(cv2.imread(p1 + fl),(512,512))

                     if len(im)==2:
                          img=np.hstack([im["Color"],im["Ambient"]])
                     else:
                          img=im["Color"]
                     cv2.imshow(p1,img)
                     ky=cv2.waitKey()


                     cv2.destroyAllWindows()
                     if chr(ky)=="m": # Remove from folder
                         os.rename(p1,mainOutDir+f1)
                         print("Moved Folder to:",mainOutDir+f1)


                     if chr(ky)=='c':  # Crop center region of PBR
                         if not os.path.exists(mainOutFix+f1):
                             shutil.copytree(p1, mainOutFix+f1)
                         print("Backing folder in",mainOutFix)
                         for fl in os.listdir(p1):
                             im=cv2.imread(p1 + fl)
                             h,w,kk=im.shape
                             im=im[int(h/4):-int(h/4),int(w/4):-int(w/4)]
                            # cv2.imshow(p1 + fl+"Resize"+str(im.shape),im)
                             cv2.imwrite(p1 + fl,im)
                           #  cv2.waitKey()
                     if chr(ky) == 'a': # Remove ambient occlusion
                         if not os.path.exists(mainOutFix + f1):
                             shutil.copytree(p1, mainOutFix + f1)
                         for fl in os.listdir(p1):
                             if "AmbientColor." in fl:
                                   os.remove(p1+fl)
                                   print("Removed"+p1+fl)
                     if chr(ky) == 'l': # # Rmove image without ambient
                         if not os.path.exists(mainOutFix + f1):
                             shutil.copytree(p1, mainOutFix + f1)
                         for fl in os.listdir(p1):
                             if ("AmbientColor." not in fl) and  ("Color." in fl):
                                 os.remove(p1 + fl)
                                 print("Removed" + p1 + fl)
                     if os.path.exists(p1): open(p1+"checked.txt","w").close()
                     if os.path.exists(mainFolder+"/Finished.txt"):
                          fff=open(mainFolder+"/Finished.txt","a")
                     else:
                         fff=open(mainFolder+"/Finished.txt","w")


                     fff.write(f1+"\n")
                     fff.close()











