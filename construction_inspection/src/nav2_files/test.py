import yaml
from yaml.loader import SafeLoader




def main():
    with open('yaml_files/apartment2_data.yaml', 'r') as f:
       data = list(yaml.load_all(f, Loader=SafeLoader))
    Apartments = {} 
    print(data)
    for i in data:
        print(i['ApartmentSquare'])
    """
    for i in yaml_data:
        pointlist = []
        for y in i["points"]:
            pointlist.append((float(i["points"][y][0]),float(i["points"][y][1]),float(i["points"][y][2])))
        Apartments[i["Apartment"]] = pointlist
    return Apartments

    """
if __name__ == "__main__":
    main()