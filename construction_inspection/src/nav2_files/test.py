import cv2

# Global variables to store coordinates, state, and rectangles
rect_start = None
rect_end = None
drawing = False
rectangles = []
path = "/home/ap/robot_controller/construction_inspection/src/nav2_files/map/"

def write_cordinates():
    cordinate_path = path + "cordinates.txt"
    f = open(cordinate_path, "w")
    for line in rectangles:
        f.write(f'{line[0]} {line[1]} {line[2]} \n')
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
        rectangles.append((name, start, end, ))
        print(f"Rectangle '{name}' added.")
    else:
        print("Rectangle discarded.")

def main():
    global rect_start, rect_end

    # Load the PGM image (grayscale)
    imagepath = path + "apartment1.pgm"
    image = cv2.imread(imagepath)
    if image is None:
        print("Error: Could not load image.")
        return

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
    write_cordinates()
    for rect in rectangles:
        start, end, name = rect
        print(f"Name: {name}, Start: {start}, End: {end}")

if __name__ == "__main__":
    main()