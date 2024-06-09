import numpy as np
import math

# Updated conversion factors, aligned with your detailed configuration

def positions_to_degrees_to_radians(positions):
    angle_per_pos = [300 / 48000, 130 / 21000, 90 / 14500, 90 / 9500]  # Correction on the sign for q3
    def position_to_angle1(pos):
        return pos * angle_per_pos[0]

    def position_to_angle2(pos):
        # Correcting the function to handle specific joint transformations properly
        return ((pos - 16375) / 154.17)

    def position_to_angle3(pos):
        return (pos - 14500) * angle_per_pos[2]  # Starting from 14000 as 0 degrees

    def position_to_angle4(pos):
        return (pos) * angle_per_pos[3]  # Inverting the transformation direction

    def convert_positions_to_angles(positions):
        angles = []
        for i in range(len(positions)):
            if i == 0:
                angles.append(position_to_angle1(positions[i]))
            elif i == 1:
                angles.append(position_to_angle2(positions[i]))
            elif i == 2:
                angles.append(position_to_angle3(positions[i]))
            elif i == 3:
                angles.append(position_to_angle4(positions[i]))
        return angles


    # Convert positions to angles in degrees
    angles_in_degrees = []
    for pos in positions:
        angles_in_degrees.append(convert_positions_to_angles(pos))

    # Convert angles in degrees to radians
    angles_in_radians = []
    for angle_set in angles_in_degrees:
        angles_in_radians.append([math.radians(angle) for angle in angle_set])

    return angles_in_radians


# Example usage
positions_example = [[24000, 2500, 14500, 9500]]  # Sample positions corresponding to zero angles
angles_in_radians = positions_to_degrees_to_radians(positions_example)
print(angles_in_radians)
