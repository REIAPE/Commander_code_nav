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