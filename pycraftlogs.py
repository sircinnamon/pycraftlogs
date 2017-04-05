import requests
import sys

key = "yourAPIkey"

def wow_zones():
    response = requests.get(
        "https://www.warcraftlogs.com:443/v1/zones?api_key=" + key)
    json_data = response.json()
    for i in json_data:
        zone_id = i['id']
        zone_name = i['name']
        for encounter in i['encounters']:
            encounter_name = encounter['name']
            if 'brackets' not in i:
                print zone_id, zone_name, encounter_name
            else:
                for bracket in i['brackets']:
                    bracket_name = bracket['name']
                    print zone_id, zone_name, encounter_name, bracket_name


def wow_classes():
    response = requests.get(
        "https://www.warcraftlogs.com:443/v1/classes?api_key=" + key)
    json_data = response.json()

    for i in json_data:
        class_id = i['id']
        class_name = i['name']
        for spec in i['specs']:
            spec_name = spec['name']
            print class_id, class_name, spec_name


def wow_rankings_encounter(encounter_id, character_name=None, server_name=None, server_region=None, metric=None, size=None, difficulty=None, partition=None, class_id=None, spec=None,bracket=None,limit=None,guild=None,server=None,region=None,page=None,filter_str=None):
    url = "https://www.warcraftlogs.com:443/v1/rankings/encounter/"+str(encounter_id)
    params = {"api_key":key,
              "metric":metric,
              "size":size,
              "difficulty":difficulty,
              "partition":partition,
              "class":class_id,
              "spec":spec,
              "bracket":bracket,
              "limit":limit,
              "guild":guild,
              "server":server,
              "region":region,
              "page":page,
              "filter":filter_str}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data

def wow_rankings_character(character_name, server_name, server_region, zone=None, encounter_id=None, metric=None, bracket=None, partition=None):
    url = "https://www.warcraftlogs.com:443/v1/rankings/character/"+character_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "zone":zone,
              "encounter":encounter_id,
              "metric":metric,
              "bracket":bracket,
              "partition":partition}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data

def wow_reports():
    return


def wow_report():
    return

key=sys.argv[1]
data = wow_rankings_character(character_name="Riloin",server_name="Korgath", server_region="US",encounter_id=1871,metric="hps")
#rankings = data["rankings"]
for x in data:
    #print x.items()
    print(x["rank"])
    import unicodedata
    #print unicodedata.normalize("NFKD", x["name"]).encode("ascii", "ignore")
