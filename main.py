
# Generate the MatSim Dataset 
# note that this script run with the blend file and refers to some
###############################Dependcies######################################################################################

import bpy
import math
import numpy as np
import bmesh
import os
import shutil
import random
import json
import sys
filepath = bpy.data.filepath
homedir = os.path.dirname(filepath)
sys.path.append(homedir) # So the system will be able to find local imports
os.chdir(homedir)
import MaterialsHandling as Materials
import ObjectsHandling as Objects
import RenderingAndSaving as RenderSave
import SetScene
import time
########################################################################################

def ClearMaterials(KeepMaterials): # clean materials from scene
    mtlist=[]
    for nm in bpy.data.materials: 
        if nm.name not in KeepMaterials: mtlist.append(nm)
    for nm in mtlist:
        bpy.data.materials.remove(nm)

################################################################################################################################################################

#                                    Main 

###################################################################################################################################################################


#------------------------Input parameters---------------------------------------------------------------------

# Example HDRI_BackGroundFolder and PBRMaterialsFolder  and ObjectsFolder folders should be in the same folder as the script. 
# Background hdri folder
HDRI_BackGroundFolder="HDRI_BackGround/"
#HDRI_BackGroundFolder=r"/home/breakeroftime/Documents/Datasets/DataForVirtualDataSet/4k_HDRI/4k/" 
#ObjectFolder=r"/home/breakeroftime/Documents/Datasets/Shapenet/ShapeNetCoreV2/"
#Folder of objects (like shapenet) 
ObjectFolder=r"Objects/"
#ObjectFolder=r"/home/breakeroftime/Documents/Datasets/Shapenet/ObjectGTLF_NEW/" 
# folder where out put will be save
OutFolder="OutFolder/" # folder where out put will be save
pbr_folders = ['PBRMaterials/'] # folders with PBR materiall each folder will be use with equal chance
#pbr_folders = [r"/mnt/306deddd-38b0-4adc-b1ea-dcd5efc989f3/Materials_Assets/NormalizedPBR/",
#r'/mnt/306deddd-38b0-4adc-b1ea-dcd5efc989f3/Materials_Assets/NormalizedPBR_MERGED/',
#r'/mnt/306deddd-38b0-4adc-b1ea-dcd5efc989f3/Materials_Assets/NormalizedPBR_MERGED/',
#r'/mnt/306deddd-38b0-4adc-b1ea-dcd5efc989f3/Materials_Assets/NormalizedPBR_MERGED/']

NumSetsToRender=10 
use_priodical_exits = False # Exit blender once every few sets to avoid memory leaks, assuming that the script is run inside Run.sh loop that will imidiatly restart blender fresh
 


#------------------Create PBR list-------------------------------------------------------- 
materials_lst = [] # List of all pbr materials folders path
for fff,fold in enumerate(pbr_folders): # go over all super folders 
    materials_lst.append([]) 
    for sdir in  os.listdir(fold): # go over all pbrs in folder
        pbr_path=fold+"//"+sdir+"//"
        if os.path.isdir(pbr_path):
              materials_lst[fff].append(pbr_path)
#------------------------------------Create list with all hdri files in the folder-------------------------------------
hdr_list=[]
for hname in os.listdir(HDRI_BackGroundFolder): 
   if ".hdr" in hname:
         hdr_list.append(HDRI_BackGroundFolder+"//"+hname)

#################################Other parameters#########################################################



NumSimulationsToRun=100000000000              # Number of simulation to run

#==============Set Rendering engine parameters (for image creaion)==========================================

bpy.context.scene.render.engine = 'CYCLES' # 
bpy.context.scene.cycles.device = 'GPU' # If you have GPU 
bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL' # Not sure if this is really necessary but might help with sum surface textures
bpy.context.scene.cycles.samples = 120 #200, #900 # This work well for rtx 3090 for weaker hardware this can take lots of time
bpy.context.scene.cycles.preview_samples = 900 # This work well for rtx 3090 for weaker hardware this can take lots of time

bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 800

#bpy.context.scene.eevee.use_ssr = True
#bpy.context.scene.eevee.use_ssr_refraction = True
bpy.context.scene.cycles.caustics_refractive=True
bpy.context.scene.cycles.caustics_reflective=True
bpy.context.scene.cycles.use_preview_denoising = True
bpy.context.scene.cycles.use_denoising = True


# get_devices() to let Blender detects GPU device
#bpy.context.preferences.addons["cycles"].preferences.get_devices()
#print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
#for d in bpy.context.preferences.addons["cycles"].preferences.devices:
#    d["use"] = 1 # Using all devices, include GPU and CPU
#    print(d["name"], d["use"])

#---------------List of materials that are part of the blender structure and will not be deleted------------------------------------------
MaterialsList=["White","Black","PbrMaterial1","PbrMaterial2","TwoPhaseMaterial","GroundMaterial","TransparentLiquidMaterial","BSDFMaterial","BSDFMaterialLiquid","Glass","PBRReplacement"] # Materials that will be used

#-------------------------Create output folder--------------------------------------------------------------


if not os.path.exists(OutFolder): os.mkdir(OutFolder)

#----------------------------Create list of Objects that will be loaded during the simulation---------------------------------------------------------------
ObjectList={}
ObjectList=Objects.CreateObjectList(ObjectFolder)
print("object list len",len(ObjectList))

#----------------------------------------------------------------------
######################Main loop##########################################################\
# loop 1: select materials, loop 2: create scences, loop 3: set materials ratios and render
 # Set the device_type
#bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA" # or "OPENCL"


scounter=0 # Count how many scene have been made
for cnt in range(NumSetsToRender):
#---------------------------Pick materials-----------------------------------------   
    MainOutputFolder=OutFolder+"/"+str(cnt)
    if  os.path.exists(MainOutputFolder): continue # Dont over run existing folder continue from where you started
    print("scounter",scounter)
    os.mkdir(MainOutputFolder)
    scounter+=1
#==================select UV mapping mode of the material to the object==========================
   
    
    rn=random.random()
    if rn<0.37:
       uv='camera'
    elif rn<0.70: 
       uv='object' 
    else: 
        uv='uv'
#--------------------------------------------------
    # Pick material type PBR/bsdf
    if random.random()<0.815: 
           matype1='pbr'
    else:
           matype1='bsdf'
    if random.random()<0.815: 
           matype2='pbr'
    else:
           matype2='bsdf'
    Materials.ChangeUVmapping(bpy.data.node_groups['Phase1'],uvmode = uv) # set uv mapping in the material graph
    
    Materials.ChangeUVmapping(bpy.data.node_groups['Phase2'],uvmode = uv) # set uv mapping in the material graph

#-----------select random material phase 1,2-----------------------------------------------------
    MaterialDictionary={} # Where materials name and properties will be stored                      

    MaterialDictionary['material1']=Materials.ChangeMaterialMode(bpy.data.node_groups['Phase1'],matype1,materials_lst) # Change the type of material by connecting bsdf, pbr, or value 0-255 node to the output node 
    MaterialDictionary['material2']=Materials.ChangeMaterialMode(bpy.data.node_groups['Phase2'],matype2,materials_lst)
    with open(MainOutputFolder +"//MaterialsNamesAndProperties.json", "w") as outfile: json.dump(MaterialDictionary, outfile)  # save materials propeties
###################################################################################
#---------------------Create a set, each set involve transition between two materials and 6 scene each involve differentr objects and backgroubds--------------------------------------------   
    RotateMaterial= random.random()<0.7 # rotate material between frames
    for nscenes in range(6): # different scenes same materials
        MainOutputFolder
        print("Add material")

        
        #if os.path.exists(CatcheFolder): shutil.rmtree(CatcheFolder)# Delete liquid simulation folder to free space
        if NumSimulationsToRun==0: break
        OutputFolder= MainOutputFolder+"/Scene_"+str(nscenes)+"/"
        if  os.path.exists(OutputFolder): continue # Dont over run existing folder continue from where you started
        os.mkdir(OutputFolder) 
        NumSimulationsToRun-=1

        ContentMaterial={"TYPE":"NONE"}

    #    #================================Create scene load object and set material=============================================================================
        print("=========================Start====================================")
        print("Simulation number:"+str(cnt)+" Remaining:"+ str(NumSimulationsToRun))
        SetScene.CleanScene()  # Delete all objects in scence
   
      
    #    #------------------------------Load random object into scene center---------------------------------

        MainObjectName=Objects.LoadRandomObject(ObjectList,random.uniform(30,50),[0,0,0])
        bpy.ops.object.select_all(action="DESELECT")
        bpy.data.objects[MainObjectName].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[MainObjectName]
        bpy.ops.object.editmode_toggle() #edit mode
        bpy.ops.mesh.remove_doubles() #remove overlapping faces
       
        bpy.ops.uv.smart_project(island_margin=0.03)
        bpy.ops.object.editmode_toggle() #back to object mode
 
        

        ClearMaterials(KeepMaterials=MaterialsList)
        MainObject = bpy.data.objects[MainObjectName]
#***************************SMOOTH optional******************************************************************
        if np.random.rand()<0.0:
            MainObject.select_set(True)
            bpy.context.view_layer.objects.active = MainObject
            bpy.ops.object.modifier_add(type='SUBSURF') # add more polygos (kind of smothing
            bpy.context.object.modifiers["Subdivision"].levels = 2
            bpy.context.object.modifiers["Subdivision"].render_levels = 2
#*******************************************************************************************        
        Materials.ReplaceMaterial(MainObject,bpy.data.materials['TwoPhaseMaterial']) # replace material on object
        MaxZ=MaxXY=20 # Size of object
       #-------------------------------------------Create ground plane and assign materials to it----------------------------------
        if np.random.rand()<0.25:
            PlaneSx,PlaneSy= SetScene.AddGroundPlane("Ground",x0=0,y0=0,z0=0,sx=MaxXY,sy=MaxXY) # Add plane for ground
            if np.random.rand()<0.9:+
                   Materials.load_random_PBR_material(bpy.data.materials['GroundMaterial'].node_tree,materials_lst)
                   Materials.ReplaceMaterial(bpy.data.objects["Ground"],bpy.data.materials['GroundMaterial']) # Assign PBR material to ground plane (Physics based material) from PBRMaterialsFolder
            
            else: 
                Materials.AssignMaterialBSDFtoObject(ObjectName="Ground",MaterialName="BSDFMaterial") 
        else: 
            with open(OutputFolder+'/NoGroundPlane.txt', 'w'): print("No Ground Plane")
        PlaneSx,PlaneSy=MaxXY*(np.random.rand()*4+2), MaxXY*(np.random.rand()*4+2)
    #------------------------Load random background hdri---------------------------------------------------------------   
        SetScene.AddBackground(hdr_list) # Add randonm Background hdri from hdri folder

    #..............................Create load  n objects into scene as background....................................................
        if np.random.rand()<0.3:
                 Objects.LoadNObjectsToScene(ObjectList,AvoidPos=[0,0,0],AvoidRad=0,NumObjects=np.random.randint(8),MnPos=[-PlaneSx/2,-PlaneSy/2,-1],MxPos=[PlaneSx/2,PlaneSy/2,3],MnScale=(np.random.rand()*0.8+0.2)*MaxXY,MxScale=np.max([MaxXY,MaxZ])*(1+np.random.rand()*4))    
                
      
    #-----------------Save materials properties as json files------------------------------------------------------------
        if not  os.path.exists(OutputFolder): os.mkdir(OutputFolder)
        print("+++++++++++++++++++++Content material++++++++++++++++++++++++++++++")
        print(ContentMaterial)
        if ContentMaterial["TYPE"]!="NONE":
                  with open(OutputFolder+'/ContentMaterial.json', 'w') as fp: json.dump(ContentMaterial, fp)
    
        


    #...........Set Scene and camera postion..........................................................
        SetScene.RandomlySetCameraPos(name="Camera",VesWidth = MaxXY,VesHeight = MaxZ)
        with open(OutputFolder+'/CameraParameters.json', 'w') as fp: json.dump( SetScene.CameraParamtersToDictionary(), fp)
        if np.random.rand()<0.09:
            SetScene.add_random_point_light()
######################################################################################################################3

# Generate images of same scene with different materials ratios on the same object and render

##########################################################################################################################        
        for matsRatio in [0,0.25,0.5,0.75,1]:    # mixture ratios   
            #------------Modify scene scene----------------------------------------------------------------------------------  
                if nscenes>1: 
                    SetScene.RandomRotateBackground() # randomly rotate background for each frame  for scenes above 1
                if nscenes>3: 
                    SetScene.AddBackground(hdr_list) #   # randomly select background for each scene  for scenes above 1 
                    if np.random.rand()<0.09:
                             SetScene.add_random_point_light()
                           
                #Randomize_RotateTranslate_TwoPBR_MaterialMapping(bpy.data.node_groups["Phase1"].nodes,bpy.data.node_groups["Phase2"].nodes,RotateMaterial)
                Materials.Randomize_RotateTranslate_PBR_MaterialMapping(bpy.data.node_groups["Phase1"].nodes,RotateMaterial) # rotate translate material mapping to object    
                Materials.Randomize_RotateTranslate_PBR_MaterialMapping(bpy.data.node_groups["Phase2"].nodes,RotateMaterial)# rotate translate material mapping to object
                bpy.data.materials["TwoPhaseMaterial"].node_tree.nodes["Mix Shader"].inputs[0].default_value = bpy.data.materials["TwoPhaseMaterial"].node_tree.nodes["Mix Shader"].inputs[0].default_value = matsRatio
       
 
            #------------------------------------------------------Save Objects to file-----------------------------------------------------
            #-------------------------------------------------------Save images--------------------------------------------------------------    
                
                bpy.context.scene.render.engine = 'CYCLES'
                print("Saving Images")
                print(OutputFolder)
           #     x=sfsfsfs
                RenderSave.RenderImageAndSave(FileNamePrefix="RGB_"+str(matsRatio),OutputFolder=OutputFolder) # Render image and save
                

                   
        #-------------------Save segmentation mask for center objet---------------------------------------------------------------------    
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
             
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        RenderSave.SaveObjectVisibleMask([MainObject.name],OutputFolder +"MaskOcluded") #mask of only visible region
        RenderSave.SaveObjectFullMask([MainObject.name],OutputFolder + "MaskFull") # all object even ocluded parts
       
        
        open(OutputFolder+"/Finished.txt","w").close()
        objs=[]
        #-------------Delete all objects from scene but keep materials---------------------------
        for nm in bpy.data.objects: objs.append(nm)
        for nm in objs:  
                bpy.data.objects.remove(nm)
       
    #------------------------------Finish and clean data--------------------------------------------------
        

    print("Cleaning")

    open(MainOutputFolder+"/Finished.txt","w").close()
    
    # Clean images
    imlist=[]
    for nm in bpy.data.images: imlist.append(nm) 
    for nm in imlist:
        bpy.data.images.remove(nm)
    # Clean materials

    ClearMaterials(KeepMaterials=MaterialsList)
    print("========================Finished==================================")
    SetScene.CleanScene()  # Delete all objects in scence
    if use_priodical_exits and scounter>=20: # Break program and exit blender, allow blender to remove junk
        #  print("Resting for a minute")
        #  time.sleep(30)
          break
if use_priodical_exits:
   print("quit")
   bpy.ops.wm.quit_blender()
      #  break