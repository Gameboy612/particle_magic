import os
import shutil
import numpy

from generators.shape_generator import *
from generators.math_tools import *


def clear_output():
    CURR_DIR = os.path.dirname(__file__)
    try:
        shutil.rmtree(os.path.join(CURR_DIR, "output"))
    except:
        pass
    output_dir = CURR_DIR + "/output"
    os.mkdir(output_dir)
    os.mkdir(output_dir + "/particles")
    os.mkdir(output_dir + "/search")
    return output_dir

OUTPUT_DIR = clear_output()


DENSITY = 3
file_index = 0
for t in [round(i, 2) for i in numpy.arange(0.5, 5.00, 0.05).tolist()]:

    RADIUS = 10 * t
    

    circle = Pattern("minecraft:dust 1 0 0 1.2", pattern=[], mode="force");
    circle.generateCircle(RADIUS * 0.2, ZERO_RVECTOR, DENSITY, erase=True);


    geometry = Pattern("minecraft:dust 1 0 0 1.2", pattern=[], mode="force");
    geometry.generateCircle(RADIUS, ZERO_RVECTOR, DENSITY);

    geometry.generateStar(
        centre = ZERO_RVECTOR,
        radius = RADIUS,
        vertices = 7,
        step = 2,
        density = DENSITY,
        offset_rot = 0,
        particle_type = ""
    )


    geometry.generatePolygon(
        centre = ZERO_RVECTOR,
        sides = 7,
        radius = RADIUS,
        density = DENSITY,
        offset_rot = 0,
        particle_type = "",
        vertex_decoration = [
            circle
        ]
    )


    output = geometry.getOutput(True);
    
    f = open(f"{OUTPUT_DIR}/particles/{file_index}.mcfunction", "w")
    f.write(output)
    f.close()


    file_index += 1




PARTICLE_RESOURCE_PATH = input("Where is the particle resource path located? (what is the function directory in your datapack?)\n")
if PARTICLE_RESOURCE_PATH[-1] == '/':
    PARTICLE_RESOURCE_PATH = PARTICLE_RESOURCE_PATH[:len(PARTICLE_RESOURCE_PATH) - 1]
TEMP_SCOREBOARD = input("\n\nWhat is your temporary scoreboard name?\n")


def BranchDirectories(nodes, directory):
    if len(nodes) <= 3:
        if len(nodes) == 1:
            f = open(f"{OUTPUT_DIR}/search/{directory}{nodes[0]}.mcfunction", "w")
        else:
            f = open(f"{OUTPUT_DIR}/search/{directory}{nodes[0]}-{nodes[-1]}.mcfunction", "w")
        f.write(f"execute if score #temp {TEMP_SCOREBOARD} matches {nodes[0]} run function {PARTICLE_RESOURCE_PATH}/particles/{nodes[0]}")
        if len(nodes) >= 2:
            f.write(f"\nexecute if score #temp {TEMP_SCOREBOARD} matches {nodes[1]} run function {PARTICLE_RESOURCE_PATH}/particles/{nodes[1]}")
            if len(nodes) == 3:
                f.write(f"\nexecute if score #temp {TEMP_SCOREBOARD} matches {nodes[2]} run function {PARTICLE_RESOURCE_PATH}/particles/{nodes[2]}")
        f.close()
        return
    
    f = open(f"{OUTPUT_DIR}/search/{directory}{nodes[0]}-{nodes[-1]}.mcfunction", "w")
    f.write(f"execute if score #temp {TEMP_SCOREBOARD} matches {nodes[0]}..{nodes[len(nodes) //2 - 1]} run function {PARTICLE_RESOURCE_PATH}/search/{directory}{nodes[0]}-{nodes[len(nodes) // 2 - 1]}/{nodes[0]}-{nodes[len(nodes) // 2 - 1]}\nexecute if score #temp {TEMP_SCOREBOARD} matches {nodes[len(nodes) // 2]}..{nodes[len(nodes) - 1]} run function {PARTICLE_RESOURCE_PATH}/search/{directory}{nodes[len(nodes) // 2]}-{nodes[len(nodes) - 1]}/{nodes[len(nodes) // 2]}-{nodes[len(nodes) - 1]}")
    f.close()

    
    os.mkdir(f"{OUTPUT_DIR}/search/{directory}/{nodes[0]}-{nodes[len(nodes) // 2 - 1]}")
    os.mkdir(f"{OUTPUT_DIR}/search/{directory}/{nodes[len(nodes) // 2]}-{nodes[len(nodes) - 1]}")
    BranchDirectories(nodes[:len(nodes) // 2], f"{directory}{nodes[0]}-{nodes[len(nodes) // 2 - 1]}/")
    BranchDirectories(nodes[len(nodes) // 2:], f"{directory}{nodes[len(nodes) // 2]}-{nodes[len(nodes) - 1]}/")
    pass

f = open(f"{OUTPUT_DIR}/search.mcfunction","w")
f.write(f"function {PARTICLE_RESOURCE_PATH}/search/0-{file_index - 1}")
BranchDirectories(range(0, file_index), "")
