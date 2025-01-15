import datetime
def calculate_area(rect):
    # Calculate the area of a rectangle
    x1, y1, x2, y2 = rect
    return abs(x2 - x1) * abs(y2 - y1)

def calculate_overlap_area(rect1, rect2):
    # Calculate the dimensions of the overlap
    x_overlap = max(0, min(rect1[2], rect2[2]) - max(rect1[0], rect2[0]))
    y_overlap = max(0, min(rect1[3], rect2[3]) - max(rect1[1], rect2[1]))
    return x_overlap * y_overlap

def is_overlap_50_percent(rect1, rect2):
    # Calculate areas
    area1 = calculate_area(rect1)
    area2 = calculate_area(rect2)
    overlap_area = calculate_overlap_area(rect1, rect2)
    
    # Check if overlap is at least 50% of either rectangle's area
    return overlap_area >= 0.5 * area1 or overlap_area >= 0.5 * area2


def check_safety_equiment(names):
    equiments = 0
    safety = ['Safety vest','Safety glasses','Hard hat']
    for idx, value in enumerate(names):
        if value in safety :
            if is_overlap_50_percent(names['Person'],names[value]):
                equiments += 1
        
    #print(f'Person has equiments {equiments}/3')
    return equiments


def update_dictionary(objects,location,data_dict):
    instalations =['Wood floor','Tiles']
        #Here we add data to dict as another dict.
        #We check how many safety items person has.
    if "Person" in objects:
        number_of_items = check_safety_equiment(objects)
        objects['Person'] = number_of_items

        
        #We add new location and 
    if location not in data_dict:
        data_dict[location] = objects
            
    for object in objects:
        
        if object not in data_dict[location]:
            if object in instalations:
                data_dict[location][object] = datetime.datetime.now().strftime("%H:%M:%S")
            else: data_dict[location][object] = objects[object]
        

    if 'Person' in data_dict[location] and "Person" in objects:
        data_dict[location]['Person'] = max(data_dict[location]['Person'], number_of_items)

    return data_dict



def print_data(data):
    for apartment in data:
            print("")
            print("--------------------------------")
            print(f'LOCATION: {apartment}')
            print("................................")
            
            for item in data[apartment]:
                if item == 'Person':
                    print(f'Item: {item} has: {data[apartment][item]}/3 safety equiment')                   
                else:
                     print(f'Item: {item}')
                    
            print("--------------------------------")
            
def main():
    # Example usage:
    rect1 = (1, 1, 5, 5)  # (x1, y1, x2, y2)
    rect2 = (2, 2, 7, 7)

    if is_overlap_50_percent(rect1, rect2):
        print("The rectangles overlap by at least 50% of their area.")
    else:
        print("The rectangles do not overlap by at least 50% of their area.")
    
if __name__ == '__main__':
    main()