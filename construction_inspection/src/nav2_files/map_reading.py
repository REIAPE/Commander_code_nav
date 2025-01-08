"""
This file opens ros map as pgm image. You draw rectangles to give apartment cordinates.
"""

import sys
import cv2
import yaml


# Global variables to store coordinates, state, and rectangles
rect_start = None
rect_end = None
drawing = False
rectangles = []
path = "/home/ap/robot_controller/dokuments/maps/"


def check_correct_start():
    if len(sys.argv) < 2:
        print("error: you must give a file")
        sys.exit(1)

def read_yaml(filename):
    path_to_file = path + filename
    with open(path_to_file, 'r') as f:
        data = yaml.full_load(f)
    image_data = {
        'image_name': data.get('image'),
        'resolution': data.get('resolution'),
        'origin': data.get('origin')
    }
    

    return image_data

def write_cordinates(resolution,origin):
    f = open("cordinates.txt", "w")
    for line in rectangles:
        cor1 = (line[1][0]*resolution + origin[0], line[1][1]*resolution + origin[1])
        cor2 = (line[2][0]*resolution + origin[0], line[2][1]*resolution + origin[1])
        f.write(f'{line[0]} {cor1} {cor2} \n')
    f.close()

def draw_rectangle(event, x, y, flags, param):
    global rect_start, rect_end, drawing

    # Left mouse button pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        rect_start = (x, y)

    # Mouse movement with button pressed
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            rect_end = (x, y)

    # Left mouse button released
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rect_end = (x, y)
        if rect_start and rect_end:
            print(f"Proposed rectangle coordinates: Start {rect_start}, End {rect_end}")
            confirm_rectangle(rect_start, rect_end)

def confirm_rectangle(start, end):
    global rectangles

    # Prompt the user for a name and confirmation
    name = input("Enter a name for this rectangle: ")
    confirm = input(f"Confirm rectangle '{name}' with coordinates Start {start}, End {end}? (y/n): ").strip().lower()

    if confirm == 'y':
        rectangles.append((name, start, end))
        print(f"Rectangle '{name}' added.")
    else:
        print("Rectangle discarded.")

def open_image(imagepath):

    image = cv2.imread(imagepath)
    print(f'Found image at : {imagepath}')
    print(f'image shape: {image.shape}. Press q to quit')
    if image is None:
        print("Error: Could not load image.")
        return

    return image

def main():
    global rect_start, rect_end
    filename = sys.argv[1]
    image_data = read_yaml(filename)

    imagepath = path + image_data['image_name']
    image = open_image(imagepath)

    clone = image.copy()
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_rectangle)

    while True:
        img = clone.copy()

        # Draw rectangle dynamically if in drawing mode
        if rect_start and rect_end and drawing:
            cv2.rectangle(img, rect_start, rect_end, (255,0,0), 2)

        # Draw finalized rectangles with names
        for rect in rectangles:
            name, start, end = rect
            cv2.rectangle(img, start, end, (255,0,0), 2)

        cv2.imshow("Image", img)

        # Break loop on 'q' key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    # Print all finalized rectangles
    print("Finalized rectangles:")
    rectangles.sort()
    write_cordinates(image_data['resolution'],image_data['origin'])
    for rect in rectangles:
        name,start, end = rect
        print(f"Name: {name}, Start: {start}, End: {end}")

if __name__ == '__main__':
    check_correct_start()
    main()