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


def wow_rankings(encounter_id=-1, character_name="", server_name="", server_region="", metric="", size=-1, difficulty=-1, partition=-1, class_id=-1, spec=-1,bracket=-1,limit=-1,guild="",server="",region="",page=-1,filter_str=""):
    if(encounter_id == -1 and (character_name+server_name+server_region == "")):
        print("Invalid query: Requires encounter_id or character_name, server_name and server_region")
        return None 
    character_mode = False
    if(character_name == "" or server_name=="" or server_region==""):
        url = "https://www.warcraftlogs.com:443/v1/rankings/encounter/"+str(encounter_id)+"?api_key=" + key
    else:
        url = "https://www.warcraftlogs.com:443/v1/rankings/character/"+character_name+"/"+server_name+"/"+server_region+"?api_key=" + key
        if(not encounter_id == -1): url = url+"&encounter="+str(encounter_id)
        character_mode=True
    if(not metric == ""): url = url+"&metric="+metric
    if(not size == -1): url = url+"&size="+str(size)
    if(not difficulty == -1): url = url+"&difficulty="+str(difficulty)
    if(not partition == -1): url = url+"&partition="+str(partition)
    if(not class_id == -1 and not character_mode): url = url+"&class="+str(class_id)
    if(not spec == -1 and not character_mode): url = url+"&spec="+str(spec)
    if(not bracket == -1 and not character_mode): url = url+"&bracket="+str(bracket)
    if(not limit == -1 and not character_mode): url = url+"&limit="+str(limit)
    if(not guild == "" and not character_mode): url = url+"&guild="+guild
    if(not server == "" and not character_mode): url = url+"&server="+server
    if(not region == "" and not character_mode): url = url+"&region="+region
    if(not page == -1 and not character_mode): url = url+"&page="+str(page)
    if(not filter_str == "" and not character_mode): url = url+"&filter="+filter_str

    print(url)
    response = requests.get(url)
    # print response.content
    json_data = response.json()
    return json_data

def wow_reports():
    return


def wow_report():
    return

key=sys.argv[1]
data = wow_rankings(character_name="Riloin", limit=10, guild="Vitium", server_name="Korgath", server_region="US")
#rankings = data["rankings"]
for x in data:
    print(x["rank"])
    import unicodedata
    #print unicodedata.normalize("NFKD", x["name"]).encode("ascii", "ignore")
