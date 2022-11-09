# Load assign and generate materials (PBR/BSDF)

###############################Dependcies######################################################################################3

import bpy
import math
import numpy as np
import bmesh
import os
import shutil
import random
import json
import sys
import colorsys
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
#sys.path.append("/home/breakeroftime/Desktop/Simulations/ModularVesselContent")
sys.path.append(directory)
os.chdir(directory)

#####################################################################################3

# Random multiply

#####################################################################################################################
def RandPow(n):
    r=1
    for i in range(int(n)):
        r*=np.random.rand()
    return r


#############################################################################################################################################

#                       Assign  bsdf Material for object and set random properties (assume material already exist in the blend file)

#############################################################################################################################################
def AssignMaterialBSDFtoObject(ObjectName, MaterialName):  
    
    

    print("================= Assign bsdf material to object "+ObjectName+" Material "+MaterialName+"=========================================================")
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects[ObjectName].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[ObjectName] 
     # Basically pick existing node and assign it to the material and set random properties (this will not work if the node doesnt already exist)          

#-------------------------------Add BSDF material to object============================================
  
    print(bpy.data.objects[ObjectName].data.materials)
    if len(bpy.data.objects[ObjectName].data.materials)==0:
         bpy.data.objects[ObjectName].data.materials.append(bpy.data.materials[MaterialName])
    else: # if object already have material replace them
         for i in range(len(bpy.data.objects[ObjectName].data.materials)):
                bpy.data.objects[ObjectName].data.materials[i]=bpy.data.materials[MaterialName]
           
        

# ----------------------------------Select random property for material --------------------------------------------------------------------------------------      
      
    if np.random.rand()<0.9:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[17].default_value = np.random.rand() # Transmission
    else:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1 #Transmission
    if np.random.rand()<0.8:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[9].default_value = np.random.rand()*np.random.rand()# Roughness
    else: 
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0# Roughness

    if np.random.rand()<0.9: # color
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (np.random.rand(), np.random.rand(),np.random.rand(), 1) # random color hsv
    else:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1,1, 1) # white color
    if np.random.rand()<0.4:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[6].default_value = np.random.rand() # metalic
    elif np.random.rand()<0.7:
      bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[6].default_value =0# metalic
    else:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[6].default_value =1# metalic
    if np.random.rand()<0.12: # specular
       bpy.data.materials['Glass'].node_tree.nodes["Principled BSDF"].inputs[7].default_value = np.random.rand()# specular
    elif np.random.rand()<0.6:
      bpy.data.materials['Glass'].node_tree.nodes["Principled BSDF"].inputs[7].default_value =0.5# specular
    else:
      ior=bpy.data.materials['Glass'].node_tree.nodes["Principled BSDF"].inputs[16].default_value# specular
      specular=((ior-1)/(ior+1))**2/0.08
      bpy.data.materials['Glass'].node_tree.nodes["Principled BSDF"].inputs[7].default_value=specular
      
    if np.random.rand()<0.12: # specular tint
       bpy.data.materials['Glass'].node_tree.nodes["Principled BSDF"].inputs[8].default_value = np.random.rand()# tint specular
    else:
      bpy.data.materials['Glass'].node_tree.nodes["Principled BSDF"].inputs[8].default_value =0.0# specular tint

    if np.random.rand()<0.4:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[10].default_value = np.random.rand()# unisotropic
    else:
        bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[10].default_value = 0# unisotropic
    if np.random.rand()<0.4:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[11].default_value = np.random.rand()# unisotropic rotation
    else: 
        bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[11].default_value = 0# unisotropic rotation
    if np.random.rand()<0.4:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[12].default_value = np.random.rand()# sheen
    else: 
        bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[12].default_value = 0# sheen
    if np.random.rand()<0.4:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[13].default_value = np.random.rand()# sheen tint
    else: 
        bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[13].default_value = 0.5# sheen tint
    bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[14].default_value =0 #Clear Coat
    bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0.03# Clear coat
 
  
    bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[16].default_value = 1+np.random.rand()*2.5 #ior index of reflection for transparen objects  
    #https://pixelandpoly.com/ior.html
    
    
    if np.random.rand()<0.2:
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[18].default_value = np.random.rand()**2*0.4# transmission rouighness
    else: 
        bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0 # transmission rouighness
    
    if np.random.rand()<0.02: # Emission
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[19].default_value = (np.random.rand(), np.random.rand(),np.random.rand(), 1)# Emission
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[20].default_value = (np.random.rand()**2)*100 # emission strengh
    else: 
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[19].default_value = (0, 0,0, 1)## transmission rouighness
       bpy.data.materials[MaterialName].node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0# Transmission strengh
      
    bpy.context.object.active_material.use_screen_refraction = True
###    return BSDFMaterialToDictionary(bpy.data.materials[MaterialName])


###########################################################################

# Randomize mapping for pbr  (assume existing mapping node in stem and randomize it, stem is a node graph)

###########################################################################
def Randomize_PBR_MaterialMapping(stem):
    # random translation 
    stem["Mapping"].inputs[1].default_value[0] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[1] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[2] = random.uniform(0, 30)
    # random rotation
    stem["Mapping"].inputs[2].default_value[0] = random.uniform(0, 6.28318530718)
    stem["Mapping"].inputs[2].default_value[1] = random.uniform(0, 6.28318530718)
    stem["Mapping"].inputs[2].default_value[2] = random.uniform(0, 6.28318530718)
    # random scalling
    r=10**random.uniform(-2, 0.6)
    stem["Mapping"].inputs[3].default_value[0] = r
    stem["Mapping"].inputs[3].default_value[1] = r
    stem["Mapping"].inputs[3].default_value[2] = r
    if random.random()<0.4:
        stem["Mapping"].inputs[3].default_value[0] = 10**random.uniform(-2, 0.6)
        stem["Mapping"].inputs[3].default_value[1] = 10**random.uniform(-2, 0.6)
        stem["Mapping"].inputs[3].default_value[2] = 10**random.uniform(-2, 0.6)
#    else:  
#        stem["Mapping"].inputs[3].default_value[0] = 1
#        stem["Mapping"].inputs[3].default_value[1] = 1
#        stem["Mapping"].inputs[3].default_value[2] = 1
###########################################################################

# Randomize mapping for pbr (assume existing mapping node in stem and randomize it, stem is a node graph)


###########################################################################
def Randomize_RotateTranslate_PBR_MaterialMapping(stem,RotateMaterial):
    # Random translation
    stem["Mapping"].inputs[1].default_value[0] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[1] = random.uniform(0, 30)
    stem["Mapping"].inputs[1].default_value[2] = random.uniform(0, 30)
    if RotateMaterial: # Random rotation
        stem["Mapping"].inputs[2].default_value[0] = random.uniform(0, 6.28318530718)
        stem["Mapping"].inputs[2].default_value[1] = random.uniform(0, 6.28318530718)
        stem["Mapping"].inputs[2].default_value[2] = random.uniform(0, 6.28318530718)        
######################################################################################

# Translate and rotate randomly the PBR texture map on an object to increase variability

###########################################################################
def Randomize_RotateTranslate_TwoPBR_MaterialMapping(stem1,stem2,RotateMaterial):
    # Random translation
    mat1=stem1["Mapping"].inputs
    mat2=stem1["Mapping"].inputs
    mat1[1].default_value[0] = mat2[2].default_value[0] = random.uniform(0, 30)
    mat1[1].default_value[1] = mat2[2].default_value[0] = random.uniform(0, 30)
    mat1[1].default_value[2] = mat2[2].default_value[0] = random.uniform(0, 30)
    if RotateMaterial: # Random rotation
        mat1[2].default_value[0] = mat2[2].default_value[0] = random.uniform(0, 6.28318530718)
        mat1[2].default_value[1] = mat2[2].default_value[0] = random.uniform(0, 6.28318530718)
        mat1[2].default_value[2] = mat2[2].default_value[0] = random.uniform(0, 6.28318530718)  

#####################################################################################################

# load random PBR material
        
########################################################################################################
def load_random_PBR_material(mat,materials_lst):
    stem = mat.nodes  # node where the material will be loaded
    rnd=np.random.randint(len(materials_lst)) # pick dataset
    print("Load a random material from the computer hard drive.")
    index = random.randint(0, len(materials_lst[rnd])-1 )
    PbrDir = materials_lst[rnd][index] # pick pbr

     
    for Fname in os.listdir(PbrDir):
       if ("olor." in Fname)  or ("COLOR." in Fname) or ("ao." in Fname)  or ("AO." in Fname):
          stem["Image Texture.001"].image=bpy.data.images.load(PbrDir+"/"+Fname)          
          print("Color "+ Fname)
       if ("oughness." in Fname) or ("ROUGH." in Fname) or ("roughness" in Fname) or ("ROUGHNESS" in Fname) or ("roughnness" in Fname):
          stem["Image Texture.002"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Roughness "+ Fname)
       if ("ormal." in Fname)  or ("NORM." in Fname) or ("normal" in Fname)  or ("NORMAL" in Fname) or ("Normal" in Fname):
          stem["Image Texture.003"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Normal "+ Fname)
       if ("eight." in Fname) or ("DISP." in Fname) or ("height" in Fname) or ("displacement" in Fname):
          stem["Image Texture"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Height "+ Fname)
       if ("etallic." in Fname) or ("etalness." in Fname)  or ("etal." in Fname) or ("etalic." in Fname) :
          stem["Image Texture.004"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Metallic "+ Fname)
       if ("pecular."  in Fname):
          stem["Image Texture.005"].image=bpy.data.images.load(PbrDir+"/"+Fname)
          print("Specular "+ Fname)
        
    Randomize_PBR_MaterialMapping(stem)
    return PbrDir

###################################################################################################################################

# Transform BSDF Mateiral to dictionary (use to save materials properties)

####################################################################################################################################
def BSDFMaterialToDictionary(bsdf):
    dic={}
    dic["TYPE"]="Principled BSDF"
    dic["Base Color"]=(bsdf.inputs[0].default_value)[:]## = (0.0892693, 0.0446506, 0.137255, 1)
    dic["Subsurface"]=bsdf.inputs[1].default_value## = 0
    dic["Subsurface Radius"]=str(bsdf.inputs[2].default_value[:])
    dic["Subsurface Color"]=bsdf.inputs[3].default_value[:]# = (0.8, 0.642313, 0.521388, 1)
    dic["Metalic"]=bsdf.inputs[6].default_value# = 5
    dic["Specular"]=bsdf.inputs[7].default_value# = 0.804545
    dic["Specular Tint"]=bsdf.inputs[8].default_value# = 0.268182
    dic["Roughness"]=bsdf.inputs[9].default_value# = 0.64
    dic["Anisotropic"]=bsdf.inputs[10].default_value# = 0.15
    dic["Anisotropic Rotation"]=bsdf.inputs[11].default_value# = 0.236364
    dic["Sheen"]=bsdf.inputs[12].default_value# = 0.304545
    dic["Sheen tint"]=bsdf.inputs[13].default_value# = 0.304545
    dic["Clear Coat"]=bsdf.inputs[14].default_value# = 0.0136364
    dic["Clear Coat Roguhness"]=bsdf.inputs[15].default_value #= 0.0136364
    dic["IOR"]=bsdf.inputs[16].default_value# = 3.85
    dic["Transmission"]=bsdf.inputs[17].default_value# = 0.486364
    dic["Transmission Roguhness"]=bsdf.inputs[18].default_value# = 0.177273
    dic["Emission"]=bsdf.inputs[19].default_value[:]# = (0.170604, 0.150816, 0.220022, 1)
    dic["Emission Strengh"]=bsdf.inputs[20].default_value
    dic["Alpha"]=bsdf.inputs[21].default_value
   # dic["bsdf Blender"]=bsdf.inputs
    return dic
    
#########################################################################################################################3

# Generate random BSDF material(stem is existing BSDF node)

########################################################################################################
def load_random_BSDF_material(stem):  
    #stem = bpy.data.materials[slot].node_tree.nodes["Principled BSDF"]
    if np.random.rand()<0.9:
      stem.inputs[17].default_value = np.random.rand() # Transmission
    else:
      stem.inputs[17].default_value = 1 #Transmission
    if np.random.rand()<0.7:
      stem.inputs[9].default_value = np.random.rand()# Roughness
    else: 
      stem.inputs[9].default_value = 0# Roughness
    
    RGB=colorsys.hsv_to_rgb(np.random.rand(), np.random.rand(),np.random.rand()) # Create random HSV and convert to RGB (HSV have better distrobution)
    stem.inputs[0].default_value = (RGB[0], RGB[1],RGB[2], 1) # random color hsv

    if np.random.rand()<0.5:
      stem.inputs[6].default_value = np.random.rand() # metalic
    elif np.random.rand()<0.38:
     stem.inputs[6].default_value =0# metalic
    else:
      stem.inputs[6].default_value =1# metalic


    if np.random.rand()<0.4:
      stem.inputs[10].default_value = np.random.rand()# anisotropic
    else:
       stem.inputs[10].default_value = 0# anisotropic
    if np.random.rand()<0.4:
      stem.inputs[11].default_value = np.random.rand()# anisotropic rotation
    else: 
       stem.inputs[11].default_value = 0# anisotropic rotation
    if np.random.rand()<0.4:
      stem.inputs[12].default_value = np.random.rand()# sheen
    else: 
       stem.inputs[12].default_value = 0# sheen
    if np.random.rand()<0.4:
      stem.inputs[13].default_value = np.random.rand()# sheen tint
    else: 
       stem.inputs[13].default_value = 0.5# sheen tint
    
 
    stem.inputs[16].default_value = 1+np.random.rand()*2.5 #ior index of reflection for transparen objects  
    #https://pixelandpoly.com/ior.html
    
    
    if np.random.rand()<0.2:
      stem.inputs[18].default_value = np.random.rand()**2*0.4# transmission rouighness
    else: 
       stem.inputs[18].default_value = 0 # transmission rouighness
    
    if np.random.rand()<0.015: # Emission
      stem.inputs[19].default_value = (RGB[0], RGB[1],RGB[2], 1)# Emission
      stem.inputs[20].default_value = (np.random.rand()**2)*100 # Transmission strengh
    else: 
      stem.inputs[19].default_value = (0, 0,0, 1)## transmission rouighness
      stem.inputs[20].default_value = 1# Transmission strengh
    stem.inputs[21].default_value = 1# alpha
    
    return BSDFMaterialToDictionary(stem)
#########################################################################################################################3

# Generate random transparent BSDF material (stem is existing BSDF node)

########################################################################################################
def load_transparent_BSDF_material(stem):
#    material = bpy.data.materials['Glass'].copy() 
#    ntree=material.node_tree  
#    stem = ntree.nodes["Principled BSDF"]
    if np.random.rand()<0.25: # Color
        stem.inputs[0].default_value = (np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand())
    else:
        rnd=1-np.random.rand()*0.3
        stem.inputs[0].default_value = (rnd, rnd, rnd, rnd)

    stem.inputs[3].default_value = stem.inputs[0].default_value 


    if np.random.rand()<0.1: # Subsurface
        stem.inputs[1].default_value = np.random.rand()
    else:
        stem.inputs[1].default_value = 0
   
    if np.random.rand()<0.5: #Transmission
        stem.inputs[17].default_value = 1-0.2*RandPow(4) # Transmission
    else:
        stem.inputs[17].default_value = 1 #Transmission
       
       
    if np.random.rand()<0.5: # Roughnesss
        stem.inputs[9].default_value = 0.2*RandPow(3) # Roughness
    else: 
        stem.inputs[9].default_value = 0# Roughness
  
 
   
       
    if np.random.rand()<0.7:# ior index refraction
          stem.inputs[16].default_value = 0.7+np.random.rand()*2 #ior index of reflection for transparen objects  
    
    else:
         stem.inputs[16].default_value = 1.415+np.random.rand()*0.115 #ior index of reflection for transparen objects  
    #https://pixelandpoly.com/ior.html

     

    if np.random.rand()<0.1: # Metalic
        stem.inputs[6].default_value = 0.15*RandPow(3)# metalic
    else:
        stem.inputs[6].default_value =0# meralic
      
      
    if np.random.rand()<0.12: # specular
          stem.inputs[7].default_value = np.random.rand()# specular
    elif np.random.rand()<0.6:
          stem.inputs[7].default_value =0.5# specular
    else:
       ior=stem.inputs[16].default_value# specular
       specular=((ior-1)/(ior+1))**2/0.08
       stem.inputs[7].default_value=specular
      
    if np.random.rand()<0.12: # specular tint
        stem.inputs[8].default_value = np.random.rand()# tint specular
    else:
        stem.inputs[8].default_value =0.0# specular tint
  
    if np.random.rand()<0.12: # anisotropic
        stem.inputs[10].default_value = np.random.rand()# unisotropic
    else:
       stem.inputs[10].default_value =0.0# unisotropic
  
    if np.random.rand()<0.12: # anisotropic rotation
        stem.inputs[11].default_value = np.random.rand()# unisotropic rotation
    else:
        stem.inputs[11].default_value =0.0# unisotropic
    
    if np.random.rand()<0.6: #Transmission Roughness
           stem.inputs[18].default_value = 0.25*np.random.rand()*np.random.rand() # transmission rouighness
    else:
           stem.inputs[18].default_value = 0 # transmission rouighness
    
      
    if np.random.rand()<0.1: # Clear  coat
          stem.inputs[14].default_value = np.random.rand()
    else:
          stem.inputs[14].default_value =0# 

    if np.random.rand()<0.1: # Clear  coat
          stem.inputs[15].default_value = np.random.rand()
    else:
        stem.inputs[15].default_value =0.03# 
    stem.inputs[12].default_value = 0 # Sheen 
    stem.inputs[13].default_value = 0.5 # Sheen tint
    stem.inputs[19].default_value = (0, 0, 0, 1) # Emission
    stem.inputs[20].default_value = 0 # Emission stength


    
    return BSDFMaterialToDictionary(stem)    


#######################################################################################################

# Replace material on object, set material be the only material of object obj

##############################################################################################################3
def ReplaceMaterial(obj,material):  

#    # Pick method to wrap PBr around object
#        if random.random()<0.55: 
#               nm='Material_pbr_camera_cord'
#        elif random.random()<0.5:
#               nm='Material_pbr_generated_cord' 
#        else:
#               nm='Material_pbr_object_cord'
        if hasattr(obj,'uv_textures'):
            obj.data.uv_textures.clear() 
            uv_textures=obj.data.uv_textures
            while (len(uv_textures)>0):
                  uv_textures = obj.data.uv_textures
                  uv_textures.remove(uv_textures[0])
        
#        for i in range(len(obj.data.materials)):
#            obj.data.materials[i]=material
        obj.data.materials.clear()
       
        obj.data.materials.append(material)
     #   fdfd=sss

####################################################################################################

#   Change UV mapping (the way the material ovelayed on the object           

########################################################################################################
def ChangeUVmapping(mat,uvmode): # 
    #   'camera' 'generated' 'object'
    if uvmode == 'object':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[3],mat.nodes["Mapping"].inputs[0])
    if uvmode == 'generated':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[0],mat.nodes["Mapping"].inputs[0])
    if uvmode == 'camera':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[4],mat.nodes["Mapping"].inputs[0])
    if uvmode == 'uv':
          mat.links.new(mat.nodes["Texture Coordinate"].outputs[2],mat.nodes["Mapping"].inputs[0])
####################################################################################################

#   Change material mode  (load random material into ma         

########################################################################################################
def ChangeMaterialMode(mat,mode, materials_lst): # Change the type of material by connecting bsdf, pbr, or value 0-255 node to the output node 
    #   'bsdf' 'pbr' 'black' 'white'
    matprop={} # material properties
    if mode == 'bsdf':
          if random.random()<0.65:
             matprop=load_random_BSDF_material(mat.nodes["Principled BSDF.001"])
          else:
             matprop=load_transparent_BSDF_material(mat.nodes["Principled BSDF.001"])
            
          mat.links.new(mat.nodes["Principled BSDF.001"].outputs[0],mat.nodes["Group Output"].inputs[0])
    if mode == 'pbr':
          matprop=load_random_PBR_material(mat,materials_lst)
          mat.links.new(mat.nodes["Principled BSDF"].outputs[0],mat.nodes["Group Output"].inputs[0])
    if mode == 'white':
           mat.nodes["Value"].outputs[0].default_value = 1
           mat.links.new(mat.nodes["Value"].outputs[0],mat.nodes["Group Output"].inputs[0])
    if mode == 'black':
           mat.nodes["Value"].outputs[0].default_value = 0
           mat.links.new(mat.nodes["Value"].outputs[0],mat.nodes["Group Output"].inputs[0])
    return matprop
 #    node_groups['NodeGroupPBR_Generated'].nodes["Texture Coordinate"].outputs[1], bpy.data.node_groups['NodeGroupPBR_Generated'].nodes["Mapping"].inputs[0])
####################################################################################################