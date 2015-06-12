import requests

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


def wow_rankings():
    response = requests.get(
        "https://www.warcraftlogs.com:443/v1/rankings/encounter/1691?metric=dps&size=20&difficulty=5&region=1&class=8&spec=1&bracket=0&limit=3&page=1&api_key=" + key)
    # print response.content
    json_data = response.json()
    # print json_data
    rank_totals = json_data['total']
    print "Total:", rank_totals
    for x in json_data['rankings']:
        rank_name = x['name']
        rank_class = x['class']
        rank_spec = x['spec']
        rank_total = x['total']
        rank_duration = x['startTime']
        rank_fightID = x['fightID']
        rank_reportID = x['reportID']
        rank_guild = x['guild']
        rank_server = x['server']
        rank_ilevel = x['itemLevel']
        #try:
        #    print rank_name
        #except:
        #    print "failure"
        print rank_name, rank_class, rank_spec, rank_total, rank_duration, rank_fightID, rank_reportID, rank_guild, rank_server, rank_ilevel


def wow_reports():
    return


def wow_report():
    return

wow_rankings()
