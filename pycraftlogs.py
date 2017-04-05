import requests
import sys

key = "yourAPIkey"

def wow_zones():
    response = requests.get(
        "https://www.warcraftlogs.com:443/v1/zones?api_key=" + key)
    json_data = response.json()
    return json_data
    # for i in json_data:
    #     zone_id = i['id']
    #     zone_name = i['name']
    #     for encounter in i['encounters']:
    #         encounter_name = encounter['name']
    #         if 'brackets' not in i:
    #             print zone_id, zone_name, encounter_name
    #         else:
    #             for bracket in i['brackets']:
    #                 bracket_name = bracket['name']
    #                 print zone_id, zone_name, encounter_name, bracket_name


def wow_classes():
    response = requests.get(
        "https://www.warcraftlogs.com:443/v1/classes?api_key=" + key)
    json_data = response.json()
    return json_data
    # for i in json_data:
    #     class_id = i['id']
    #     class_name = i['name']
    #     for spec in i['specs']:
    #         spec_name = spec['name']
    #         print class_id, class_name, spec_name


def wow_rankings_encounter(encounter_id, character_name=None,
                           server_name=None, server_region=None, 
                           metric=None, size=None, difficulty=None,
                           partition=None, class_id=None, spec=None,
                           bracket=None, limit=None, guild=None,
                           server=None, region=None, page=None,
                           filter_str=None):
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

def wow_rankings_character(character_name, server_name, server_region,
                           zone=None, encounter_id=None, metric=None,
                           bracket=None, partition=None):
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

def wow_parses(character_name, server_name, server_region, zone=None,
               encounter_id=None, metric=None, bracket=None, 
               compare=None, partition=None):
    url = "https://www.warcraftlogs.com:443/v1/parses/character/"+character_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "zone":zone,
              "encounter":encounter_id,
              "metric":metric,
              "bracket":bracket,
              "compare":compare,
              "partition":partition}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data

def wow_reports_guild(guild_name, server_name, server_region,
                      start=None, end=None):
    url = "https://www.warcraftlogs.com:443/v1/reports/guild/"+guild_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "start":start,
              "end":end}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data

def wow_reports_user(username, start=None, end=None):
    url = "https://www.warcraftlogs.com:443/v1/reports/user/"+username
    params = {"api_key":key,
              "start":start,
              "end":end}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data


def wow_report_fights(code, translate=None):
    url = "https://www.warcraftlogs.com:443/v1/report/fights/"+code
    params = {"api_key":key,
              "translate":translate}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data

def wow_report_events(code, start=None, end=None, actorid=None,
                      actorinstance=None, actorclass=None, cutoff=None,
                      encounter=None, wipes=None, difficulty=None,
                      filter_str=None, translate=None):
    url = "https://www.warcraftlogs.com:443/v1/report/events/"+code
    params = {"api_key":key,
              "start":start, 
              "end":end, 
              "actorid":actorid, 
              "actorinstance":actorinstance, 
              "actorclass":actorclass, 
              "cutoff":cutoff, 
              "encounter":encounter, 
              "wipes":wipes, 
              "difficulty":difficulty, 
              "filter":filter_str,
              "translate":translate}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data

def wow_report_tables(view, code, start=None, end=None, hostility=None, 
                      by=None, sourceid=None, sourceinstance=None, 
                      sourceclass=None, targetid=None, 
                      targetinstance=None, targetclass=None, 
                      abilityid=None, options=None, cutoff=None, 
                      encounter=None, wipes=None, difficulty=None, 
                      filter_str=None, translate=None):
    url = "https://www.warcraftlogs.com:443/v1/report/tables/"+view+"/"+str(code)
    params = {"api_key":key,
              "start":start, 
              "end":end, 
              "hostility":hostility, 
              "by":by, 
              "sourceid":sourceid, 
              "sourceinstance":sourceinstance, 
              "sourceclass":sourceclass, 
              "targetid":targetid, 
              "targetinstance":targetinstance, 
              "targetclass":targetclass, 
              "abilityid":abilityid, 
              "options":options, 
              "cutoff":cutoff, 
              "encounter":encounter, 
              "wipes":wipes, 
              "difficulty":difficulty, 
              "filter":filter_str,
              "translate":translate}
    response = requests.get(url, params=params)
    print(response.url)
    json_data = response.json()
    return json_data

key=sys.argv[1]
data = wow_reports_guild(guild_name="Vitium",server_name="Korgath", server_region="US")
#rankings = data["rankings"]
recent_report_code = ""
raid_start = 0
for x in data:
    #print x.items()
    print(x["title"] + " "+ x["owner"])
    import unicodedata
    recent_report_code = x["id"]
    raid_start = x["start"]
    #print unicodedata.normalize("NFKD", x["name"]).encode("ascii", "ignore")
data = wow_report_fights(code=recent_report_code)
recent_fight_start = 0
recent_fight_end = 0
for x in data["fights"]:
    #print x.items()
    print(x["name"] + " "+ str(x["kill"]))
    recent_fight_start = x["start_time"]
    recent_fight_end = x["end_time"]
    import unicodedata
    #print unicodedata.normalize("NFKD", x["name"]).encode("ascii", "ignore")
data = wow_report_tables(view="healing",code=recent_report_code,start=(recent_fight_start), end=(recent_fight_end))
for x in data["entries"]:
    print x.keys()
    print(x["name"] + " "+ str(x["total"]))