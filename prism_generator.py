import pyperclip
import math
import numpy as np

def generate_prism(particle_type, width, height, dpb=10):
    output = f"# generate_prism({particle_type}, {width},{height},{dpb})\n\n"
    output += f"particle {particle_type} ^ ^ ^ 0 0 0 0 1 force @a\n"
    output += f"particle {particle_type} ^ ^{height} ^ 0 0 0 0 1 force @a\n"
    j = -1 / dpb

    for i in np.arange(0, width / 2 + 1 - 1.5 / dpb, 1 / dpb * width / height):
        output += f"particle {particle_type} ^{i} ^{j} ^{i} 0 0 0 0 1 force @a\n"
        output += f"particle {particle_type} ^{-1 * i} ^{j} ^{i} 0 0 0 0 1 force @a\n"
        output += f"particle {particle_type} ^{i} ^{j} ^{-1 * i} 0 0 0 0 1 force @a\n"
        output += f"particle {particle_type} ^{-1 * i} ^{j} ^{-1 * i} 0 0 0 0 1 force @a\n"

        if round(height-j, 5) != round(j, 5):
            output += f"particle {particle_type} ^{i} ^{height - j} ^{i} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{-1 * i} ^{height - j} ^{i} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{i} ^{height - j} ^{-1 * i} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{-1 * i} ^{height - j} ^{-1 * i} 0 0 0 0 1 force @a\n"
        for k in np.arange(0, i, 1/dpb):
            output += f"particle {particle_type} ^{k} ^{j} ^{i} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{-1 * k} ^{j} ^{i} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{i} ^{j} ^{k} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{i} ^{j} ^{-1 * k} 0 0 0 0 1 force @a\n"
            
            output += f"particle {particle_type} ^{k} ^{j} ^{-1 * i} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{-1 * k} ^{j} ^{-1 * i} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{-1 * i} ^{j} ^{k} 0 0 0 0 1 force @a\n"
            output += f"particle {particle_type} ^{-1 * i} ^{j} ^{-1 * k} 0 0 0 0 1 force @a\n"

            if round(height-j, 5) != round(j, 5):
                output += f"particle {particle_type} ^{k} ^{height - j} ^{i} 0 0 0 0 1 force @a\n"
                output += f"particle {particle_type} ^{-1 * k} ^{height - j} ^{i} 0 0 0 0 1 force @a\n"
                output += f"particle {particle_type} ^{i} ^{height - j} ^{k} 0 0 0 0 1 force @a\n"
                output += f"particle {particle_type} ^{i} ^{height - j} ^{-1 * k} 0 0 0 0 1 force @a\n"
                
                output += f"particle {particle_type} ^{k} ^{height - j} ^{-1 * i} 0 0 0 0 1 force @a\n"
                output += f"particle {particle_type} ^{-1 * k} ^{height - j} ^{-1 * i} 0 0 0 0 1 force @a\n"
                output += f"particle {particle_type} ^{-1 * i} ^{height - j} ^{k} 0 0 0 0 1 force @a\n"
                output += f"particle {particle_type} ^{-1 * i} ^{height - j} ^{-1 * k} 0 0 0 0 1 force @a\n"
            else:
                for k in np.arange(0, i, 1/dpb):
                    output += f"particle {particle_type} ^{k} ^{height / 2} ^{i} 0 0 0 0 1 force @a\n"
                    output += f"particle {particle_type} ^{-1 * k} ^{height / 2} ^{i} 0 0 0 0 1 force @a\n"
                    output += f"particle {particle_type} ^{i} ^{height / 2} ^{k} 0 0 0 0 1 force @a\n"
                    output += f"particle {particle_type} ^{i} ^{height / 2} ^{-1 * k} 0 0 0 0 1 force @a\n"
                    
                    output += f"particle {particle_type} ^{k} ^{height / 2} ^{-1 * i} 0 0 0 0 1 force @a\n"
                    output += f"particle {particle_type} ^{-1 * k} ^{height / 2} ^{-1 * i} 0 0 0 0 1 force @a\n"
                    output += f"particle {particle_type} ^{-1 * i} ^{height / 2} ^{k} 0 0 0 0 1 force @a\n"
                    output += f"particle {particle_type} ^{-1 * i} ^{height / 2} ^{-1 * k} 0 0 0 0 1 force @a\n"
                    
                output += f"particle {particle_type} ^ ^{height} ^ 0 0 0 0 1 force @a\n"
                return output

        j += 1 / dpb



    
    output += f"particle {particle_type} ^ ^{height} ^ 0 0 0 0 1 force @a\n"

    return output
pyperclip.copy(generate_prism("minecraft:dust 0.1 0.1 0.1 1", 1,4,2))