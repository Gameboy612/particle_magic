from generators.shape_generator import *



circle = Pattern("minecraft:dust 1 0 0 0.8", pattern=[])
circle.generateCircle(1.5, ZERO_RVECTOR, 3, erase=True);







geometry = Pattern("minecraft:dust 1 0 0 0.8", pattern=[], mode="force");
geometry.generateCircle(12, ZERO_RVECTOR, 3);

geometry.generateStar(
    centre = ZERO_RVECTOR,
    radius = 12,
    vertices = 7,
    step = 3,
    density = 3,
    offset_rot = 0,
    particle_type = ""
)


geometry.generatePolygon(
    centre = ZERO_RVECTOR,
    sides = 7,
    radius = 12,
    density = 3,
    offset_rot = 0,
    particle_type = "",
    vertex_decoration = [
        lambda: geometry.generateCircle(1.5, Vector3D(0,0,0,True), 3, "", "", True, erase=True),
    ]
)


output = geometry.getOutput(True);
    
pyperclip.copy(output)
