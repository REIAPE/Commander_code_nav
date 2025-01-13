"""
This file is fully testing purposes.

"""
import yaml
from yaml.loader import SafeLoader

def get_cordinate_list():
    with open('yaml_files/apartment2_data.yaml', 'r') as f:
       data = list(yaml.load_all(f, Loader=SafeLoader))
    Apartments = {} 
    for i in data:
        pointlist = []
        for points in i["ApartmentSquare"]:
            pointlist.append(((points[0][0],points[0][1]),(points[1][0],points[1][1])))
        Apartments[i['Apartment']] = pointlist

        Wc_apartment = i['Apartment'] + ':WC'
        if "WcSquare" in i:
            Apartments[Wc_apartment] = [(((i["WcSquare"][0][0],i["WcSquare"][0][1]),(i["WcSquare"][1][0],i["WcSquare"][1][1])))]

    return Apartments

def is_point_inside_rectangle(rect, point):
    #Takes two point of rectangle and point.
    #Returns true if point is inside.
    (x1, y1), (x2, y2) = rect
    px, py = point
    
    return (
        min(x1, x2) <= px <= max(x1, x2) and
        min(y1, y2) <= py <= max(y1, y2)
    )

    

def main():
    #as8, as9:wc, as5, as6:wc
    points = [(0,3),(4,-2),(-12,4),(-4,-2)]
    cordinates = get_cordinate_list()
    for point in points:
        for apartment in cordinates:
            for rectangle in cordinates[apartment]:
                if is_point_inside_rectangle(rectangle,point): print(apartment)
        
if __name__ == "__main__":
    main()