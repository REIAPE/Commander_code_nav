
from ultralytics import YOLO


def main():
    model=YOLO('yolov8s.pt')
    results = model(source='test_images/1_3_safety.PNG', show=True, conf=0.6, save=False)
    
    for result in results:
        classes_names = result.names
            
            # iterate over each box
        for box in result.boxes:
                # check if confidence is greater than 60 percent

                    # get coordinates
            [x1, y1, x2, y2] = box.xyxy[0]
                    # convert to int
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # get the class
            cls = int(box.cls[0])

                    # get the class name
            class_name = classes_names[cls]
            print(class_name, box.conf)
if __name__ == '__main__':
    main()