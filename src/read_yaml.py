import yaml
from yaml.loader import SafeLoader


def read_yaml_file_for_points():
    with open('Drone_pointdata.yaml', 'r') as f:
        yaml_data = list(yaml.load_all(f, Loader=SafeLoader))
    Apartments = {} 
    for i in yaml_data:
        pointlist = []
        for y in i["points"]:
            pointlist.append((float(i["points"][y][0]),float(i["points"][y][1]),float(i["points"][y][2])))
        Apartments[i["Apartment"]] = pointlist
    return Apartments