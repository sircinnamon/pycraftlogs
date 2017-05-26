import pycraftlogs

key=sys.argv[1]
lst = generateGuildReportList("Vitium","Korgath","US",start=1490241142311)
for l in lst:
    print(l.title + " ("+l.id+")")
recent_report_code = lst[len(lst)-1].id

table = wow_report_tables("debuffs", recent_report_code, end=4058391)
print("DEBUFFS")
for entry in table:
    print(entry.name + " -> " + str(entry.totalUses))
    print("    "+str(entry.totalUptime) + " over "+ str(len(entry.bands)))

json_rankings = wow_rankings_encounter(1866, metric="hps", server="Korgath", region="US", guild="Vitium")
print(json_rankings["rankings"][1]["name"])