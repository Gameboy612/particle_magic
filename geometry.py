from generators.shape_generator import *



pentagon = Pattern("minecraft:dust 0 0 0 0.8", pattern=[])
# pentagon.generateCircle(12, ZERO_RVECTOR, 5);


pentagon.generatePolygon(
    centre = ZERO_RVECTOR,
    sides = 5,
    radius = 3,
    density = 4,
    offset_rot = 0,
    particle_type = "",
    vertex_decoration = [
        lambda: pentagon.generateCircle(0.5, Vector3D(0,0,0,True), 3, "", "", True, erase=True)
    ]
)





geometry = Pattern("minecraft:dust 1 0 0 0.8", pattern=[]);
geometry.generateCircle(12, ZERO_RVECTOR, 4);

geometry.generatePolygon(
    centre = ZERO_RVECTOR,
    sides = 7,
    radius = 12,
    density = 4,
    offset_rot = 0,
    particle_type = "",
    vertex_decoration = [
        lambda: geometry.generateCircle(3, Vector3D(0,0,0,True), 4, "", "", True, erase=True),
        pentagon
    ]
)


output = geometry.getOutput(True);
    
pyperclip.copy(output)
