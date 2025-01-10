import math
def is_point_inside_rotated_rectangle(point, rectangle_center, width, height, angle):
    """
    Check if a point is inside a rotated rectangle.

    Parameters:
    - point: tuple (x, y) coordinates of the point to check.
    - rectangle_center: tuple (cx, cy) coordinates of the rectangle's center.
    - width: float, the width of the rectangle.
    - height: float, the height of the rectangle.
    - angle: float, the rotation angle of the rectangle in degrees (counter-clockwise).

    Returns:
    - bool: True if the point is inside the rotated rectangle, False otherwise.
    """
    px, py = point
    cx, cy = rectangle_center

    # Convert the angle to radians
    angle_rad = math.radians(angle)

    # Translate point to rectangle's local coordinate system
    translated_x = px - cx
    translated_y = py - cy

    # Rotate point back by -angle to align with rectangle's axis-aligned coordinate system
    aligned_x = (translated_x * math.cos(-angle_rad)) - (translated_y * math.sin(-angle_rad))
    aligned_y = (translated_x * math.sin(-angle_rad)) + (translated_y * math.cos(-angle_rad))

    # Check if the point is within the axis-aligned rectangle boundaries
    half_width = width / 2
    half_height = height / 2
    return -half_width <= aligned_x <= half_width and -half_height <= aligned_y <= half_height

def rotate_vector_around_point(vector, pivot, angle_degrees):
    """
    Rotates a 2D vector around a given pivot point by a specified angle.

    :param vector: A tuple (x, y) representing the 2D vector to rotate.
    :param pivot: A tuple (px, py) representing the pivot point.
    :param angle_degrees: The angle by which to rotate the vector, in degrees.
    :return: A tuple (x', y') representing the rotated vector.
    """
    angle_radians = math.radians(angle_degrees)
    
    # Translate vector to pivot-relative coordinates
    x, y = vector
    px, py = pivot
    translated_x = x - px
    translated_y = y - py
    
    # Rotate around the origin (pivot-relative coordinates)
    rotated_x = translated_x * math.cos(angle_radians) - translated_y * math.sin(angle_radians)
    rotated_y = translated_x * math.sin(angle_radians) + translated_y * math.cos(angle_radians)
    
    # Translate back to original coordinates
    final_x = rotated_x + px
    final_y = rotated_y + py
    
    return final_x, final_y

def point_inside_rectangle(rect, point):
    #Takes two point of rectangle and point.
    #Returns true if point is inside.
    (x1, y1), (x2, y2) = rect
    px, py = point
    
    return (
        min(x1, x2) <= px <= max(x1, x2) and
        min(y1, y2) <= py <= max(y1, y2)
    )

