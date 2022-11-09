# MatSim dataset generation script: Generate images of random material on random objects in random environments with a gradual transition between materials
This script will procedurally generate images of random materials on a random object with a gradual transition between the materials for material similarity recognition dataset generation. See the paper (One-shot recognition of any material anywhere using contrastive learning with
physics-based rendering)[] for more details. 

## What does this generate?

Generate the MatSim Dataset for material similarity: Random materials on random objects in random environments with a gradual transition between materials 
![](/Figure1.jpg)
![](/Figure2.jpg)




## How it works:
The general work on the script is loading. Objects background and two materials. Assigning one material to the object and then gradually transitioning the object to the second material while generating images of the transition states. See (paper)[] for more details 

# What you need
## Hardware + Software
The script was run with Blender 3.1 with no add-ons, it can run with GPU or CPU but run much faster with a strong GPU.

## CGI Assets  
Objects Folder, HDRI background folder, and a folder of PBR materials. Example folders are supplied as: “HDRI_BackGround”, “PBRMaterials”, and “Objects”. 
The script should run as is with these folders.
However, if you want to create truly diverse data, you need a large number of backgrounds, objects, and PBR materials. This can be downloaded for free at:
[PolyHaven](https://polyhaven.com/), [AmbientCg](https://ambientcg.com/), [Shapenet](https://shapenet.org/). Note that the PBR folder should be in standard format for texture file names, for more details, see section ###PBR files format. 

# How to use.
There are two ways to use this code one from within Blender and one from the command line.
To run from the command line, use the line:
blender DatasetGeneration.blend --background -noaudio -P  main.py
Or sh Run.sh
In this case, all the run parameters will be in main.py
To run from within blender, open DatasetGeneration.blend and run from main.py from within blender. Note for Blender3  the main.py you run from within Blender is stored inside the .blend file and is different from the main.py file in the code folder if you change one, the other will not change. This can be very confusing. Blender python is very confusing in general.

Note that while running, Blender will be paralyzed and will not respond.
*** Note all paths are set to the example folder supplied, running Run.sh or the main.py from the blender file should allow the script to run out of the box
## Main run parameters 
The main running parameters are in the main.py in the Input parameters section.
This include:
HDRI_BackGroundFolder = path to the HDRI background folder 
ObjectFolder = Path to the folder containing the object files (for example, shape net folder) 
OutFolder = path to output folder where generated dataset will be saved
pbr_folders  = path to a folder containing the PBRs textures subfolders

Sample folders to all of these assets folder are supplied with the code and could be used as reference. In general, the code should run as is from the command line and from within Blender GUI.
For other parameters, see the documentation within the code.

 
# Input folder structure:
See sample folders for example:

## Object Folder structure.
The object folder should contain the object in .obj or .gtlf format in the main folder or subfolder  of the .Obj  just using the Shapenet dataset as is should work. There are, in some cases, advantages in first converting the object to GTLF  format since its blender have some issue with obj materials. But this is not essential.

## HDRI folder
This should just contain HDRI images for the background.

### PBR format
The PBR folder should contain subfolders, each containing PBR texture maps. Blender read texture maps by their name. Therefore untypical map names will be ignored. The texture maps names should contains one of the following: "OriginColor.","Roughness.","Normal.","Height.","Metallic.","AmbientOcclusion"r,"Specular.","Reflection","Glosinees".
The script: PBR_handling\StandartizePBR.py will automatically convert a set of PBR folders to standard PBR folders (mainly rename texture maps files to standard names)

# Combining existing PBR texture maps to generate new PBRS
To increase the number of PBRs materials is possible to combine existing PBR materials. This is done by randomly mixing and combining existing PBR texture maps to generate new texture maps.
The script: PBR_Handling/CombinePBRMaterials.py. Take input pbr folders and mix them to generate new PBRS materials.


# Additional parameters 
In the “Input parameters” of "Main" DatasetGeneration  script (last section of the script)
"NumSimulationsToRun" determines how many different environments to render into images (How many different images will be created).



# Dealling with blender slowing done memory  issues and crashes
Given Blender’s tendency to crash, running this script alone can be problematic for large dataset creation. To avoid the need to restart the program every time Blender crashes, use the shell script Run.sh. This script will run the blender file in a loop, so it will restart every time Blender crashes (and continue from the last set). This can be run from shell/cmd/terminal: using: sh Run.sh. 
Also, in some case blender doesn't crash but  can start getting slower and slower, one way to solve it is to exit the blender once in  a while. Setting the parameter: use_priodical_exits
In the main.py to True, will cause Blender to exist every 10 sets. If this is run inside Run.sh blender will be immediately restarted and will start working cleanly. 



# Notes:
1) Running this script should paralyze Blender until the script is done, which can take a while.
2) The script refers to materials nodes and will only run as part of the blender file



# Sources for objects/HDRI/PBR materials
1) Objects were taken from [Shapenet](https://shapenet.org/). Blender has some issue with reading the  shapenet ".obj" files directly, so it might be easier (but not essential) to convert to GTLF format using the AddionalScripts\ConvertShapeNet.py script supplied. See [https://github.com/CesiumGS/obj2gltf](https://github.com/CesiumGS/obj2gltf).

3) HDRI backgrounds were downloaded from [PolyHaven](https://polyhaven.com/)
4) PBR materials textures were downloaded from [AmbientCg](https://ambientcg.com/) and [FreePBR](https://freepbr.com/) and https://www.cgbookcase.com/.



