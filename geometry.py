from generators.shape_generator import *

geometry = Pattern("minecraft:dust 1 0 0 0.8");
geometry.generateCircle(12, ZERO_RVECTOR, 5);

geometry.generatePolygon(
    centre = ZERO_RVECTOR,
    sides = 7,
    radius = 12,
    density = 4.5,
    offset_rot = 0,
    particle_type = "",
    vertex_decoration = [
        lambda: geometry.generateCircle(3, Vector3D(0,0,0,True), 5, "", "", True, erase=True),
        lambda: geometry.generatePolygon(
                    centre = ZERO_RVECTOR,
                    sides = 5,
                    radius = 3,
                    density = 4.5,
                    offset_rot = 0,
                    particle_type = "",
                    vertex_decoration = [
                        lambda: geometry.generateCircle(0.5, Vector3D(0,0,0,True), 3, "", "", True, erase=True),
                    ]
                )
    ]
)

output = geometry.getOutput(True);
    
pyperclip.copy(output)
