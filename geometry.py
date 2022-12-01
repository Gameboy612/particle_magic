from generators.shape_generator import *

my_pattern = Pattern("minecraft:dust 1 0 0 0.8");
my_pattern.generateCircle(8, ZERO_RVECTOR, 5);

my_pattern.generatePolygon(
    centre = ZERO_RVECTOR,
    sides = 7,
    radius = 8,
    density = 4.5,
    offset_rot = 0,
    particle_type = "",
    vertex_decoration = [
        lambda: my_pattern.generateCircle(1.3, Vector3D(0,0,0,True), 5, "", "", True, erase=True),
        lambda: my_pattern.generateCircle(0.9, Vector3D(0,0,0,True), 5, "", "", True, erase=True),
    ]
)

output = my_pattern.getOutput(True);
    
pyperclip.copy(output)