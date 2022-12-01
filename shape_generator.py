import math
import pyperclip


class Vector3D:
    x = 0;
    y = 0;
    z = 0;
    relative = True;
    def __init__(self, x: float, y: float, z: float, relative=False):
        self.x = x;
        self.y = y;
        self.z = z;
        self.relative = relative;

    def toString(self):
        if self.relative:
            return f"^{round(self.x, 8) if self.x != 0 else ''} ^{round(self.y, 8) if self.y != 0 else ''} ^{round(self.z, 8) if self.z != 0 else ''}";
        return f"{round(self.x, 8)} {round(self.y, 8)} {round(self.z, 8)}";
    
    def addVector(self, v2):
        if not self.relative:
            return ValueError(f'This Vector3D Object is not a relative vector.');
        if not v2.relative:
            return ValueError(f'Parameter is not a relative vector.');
        x = self.x + v2.x;
        y = self.y + v2.y;
        z = self.z + v2.z;
        return Vector3D(x, y, z, True);

    def getSqrDistance(self, v2):
        if self.relative != v2.relative:
            return ValueError(f'Both vectors must be relative or fixed in order for getSqrDistance() to run.');
        dx = self.x - v2.x;
        dy = self.y - v2.y;
        dz = self.z - v2.z;
        return dx ** 2 + dy ** 2 + dz ** 2;

# CONSTANTS
ZERO_RVECTOR = Vector3D(0,0,0, True)
ZERO_VECTOR = Vector3D(0,0,0, False)


class Polar2D:
    r = 1;
    theta = 0;
    z_offset = 0;

    def __init__(self, r, theta, z_offset = 0.0):
        self.r = r;
        self.theta = theta;
        self.z_offset = z_offset;
    
    def toVector3D(self):
        return Vector3D(self.r * math.cos(self.theta), self.r * math.sin(self.theta), self.z_offset, True);

    def RotateRadians(self, radians):
        self.theta += radians;
        return self

    def RotateDegrees(self, degrees):
        self.theta += degrees * math.pi / 180;
        return self

    def setRadians(self, radians):
        self.theta = radians;
        return self

    def setDegrees(self, degrees):
        self.theta = degrees * math.pi / 180;
        return self


class Particle:
    particle_type = "";
    origin = Vector3D(0,0,0,1);
    size = Vector3D(0,0,0,0);
    speed = 0.0;
    count = 1;
    mode = "normal";
    player = "@a";

    disabled = False

    def __init__(self, particle_type: str, origin: Vector3D, size: Vector3D, speed: float, count: int, mode="normal", player="@a"):
        if count <= 0:
            return ValueError(f'Particle Error: Particle count is less than 1 (expected positive input, but received {count}');
        if speed < 0:
            return ValueError(f'Particle Error: Particle speed is negative (expected positive input, but received {speed}');
        self.particle_type = particle_type
        self.origin = origin
        self.size = size
        self.speed = speed
        self.count = count
        self.mode = mode
        self.player = player

    def getCommand(self):
        return f"particle {self.particle_type} {self.origin.toString()} {self.size.toString()} {self.speed} {self.count}";





class Pattern:
    default_particle_type = "";
    players = "@a"
    pattern = [Particle("", Vector3D(0, 0, 0, True), Vector3D(0,0,0), 0, 1)];

    centre_offset = Vector3D(0,0,0, True);

    def __init__(self, default_particle_type="minecraft:happy_villager", players = "@a", pattern=[]):
        self.default_particle_type = default_particle_type;
        self.players = players;
        self.pattern = pattern;
    
    def getOutput(self, print_particle_count=False):
        out = "";
        count = 0;
        for i in self.pattern:
            if i.disabled:
                pass
            elif i.particle_type != "":
                out += i.getCommand() + "\n";
                count += 1;
            else:
                j = i;
                j.particle_type = self.default_particle_type;
                out += j.getCommand() + "\n";
                count += 1;

        if print_particle_count:
            print("Number of Particles:", count)
        return out;

    def addParticle(self, particle: Particle):
        self.pattern.append(particle);

    def eraseRadius(self, centre, radius, filter_particle_type=""):
        i = 0;
        while i < len(self.pattern):
            if filter_particle_type == "" or filter_particle_type != self.pattern[i].particle_type:
                if self.pattern[i].origin.getSqrDistance(centre) < radius ** 2:
                    self.pattern[i].disabled = True;
            i += 1;
            

    def generateCircle(self, radius: Vector3D, centre: Vector3D, density: float, particle_type=default_particle_type, players=players, relative=True, erase=False):
        centre = centre.addVector(self.centre_offset)

        # circumference * particle density is the number of particles required.
        particle_count = (2 * math.pi * radius) * density;
        if particle_type == "":
            particle_type = self.default_particle_type;
        if players == "":
            players = self.players;

        if erase:
            self.eraseRadius(centre, radius, "");

        for i in range(math.ceil(particle_count)):
            self.pattern.append(Particle(particle_type, centre.addVector(Polar2D(radius, i / particle_count * 2 * math.pi).toVector3D()), Vector3D(0, 0, 0, False), 0, 1, "normal", players));

    def generateLine(self, origin: Vector3D, destination: Vector3D, density: float, particle_type=default_particle_type, players=players, relative=True):
        particle_count = math.sqrt(origin.getSqrDistance(destination)) * density;
        if particle_type == "":
            particle_type = self.default_particle_type;
        if players == "":
            players = self.players;

        dx = (destination.x - origin.x) / particle_count;
        dy = (destination.y - origin.y) / particle_count;
        dz = (destination.z - origin.z) / particle_count;

        for i in range(math.ceil(particle_count)):
            self.pattern.append(
                Particle(
                    particle_type,
                    Vector3D(
                        origin.x + dx * i,
                        origin.y + dy * i,
                        origin.z + dz * i,
                        True
                    ),
                    Vector3D(0,0,0),
                    0, 1, "normal", players
                )
            );
    

    def generatePolygon(self, centre: Vector3D, radius: float, sides: int, density: float, offset_rot = 0, particle_type=default_particle_type, players=players, relative=True, vertex_decoration=[Particle("", Vector3D(0, 0, 0, True), Vector3D(0,0,0), 0, 1)]):
        if particle_type == "":
            particle_type = self.default_particle_type;
        if players == "":
            players = self.players;
        
        if sides < 3:
            return ValueError(f"Sides is expected to be larger than 2, received {sides} instead.");
        
        ext_angle = 2 * math.pi / sides;
        v = Polar2D(radius, offset_rot)
        for i in range(sides):
            self.generateLine(centre.addVector(v.toVector3D()), v.RotateRadians(ext_angle).toVector3D(), density, particle_type, players, relative);

        # add decorations in the polygon vertices
        v = Polar2D(radius, offset_rot)
        for i in range(sides):
            v.RotateRadians(ext_angle)
            for pattern in vertex_decoration:
                old_centre_offset = self.centre_offset
                self.centre_offset = v.toVector3D()
                pattern()
                self.centre_offset = old_centre_offset










if __name__ == "__main__":
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



    # my_pattern.generatePolygon(
    #     centre = ZERO_RVECTOR,
    #     sides = 3,
    #     radius = 8,
    #     density = 4.5,
    #     offset_rot = 0,
    #     particle_type = "",
    #     vertex_decoration = [
    #         lambda: my_pattern.generateCircle(1, Vector3D(0,0,0,True), 5, "", "", True, erase=True)
    #     ]
    # )
    
    # my_pattern.generatePolygon(
    #     centre = ZERO_RVECTOR,
    #     sides = 3,
    #     radius = 8,
    #     density = 4.5,
    #     offset_rot = math.pi,
    #     particle_type = "",
    #     vertex_decoration = [
    #         lambda: my_pattern.generateCircle(1, Vector3D(0,0,0,True), 5, "", "", True, erase=True)
    #     ]
    # )