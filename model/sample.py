result = ((u'Raaz', u'AMC Metrion', '15:30:00'), (u'Raaz', u'AMC Metrion', '18:30:00'), (u'Raaz', u'AMC Van Ness', '11:30:00'), (u'Raazi', u'AMC Metrion', '12:30:00'), (u'Raazi', u'AMC Metrion', '15:00:00'), (u'Raazi', u'AMC Metrion', '18:30:00'))
d = {}
for r in result:
    # print(r)
    if r[0] not in d:
        # print(r[0])
        d[r[0]] = {}
        if r[1] not in d[r[0]]:
            d[r[0]][r[1]] = []
        d[r[0]][r[1]].append(r[2])
    else:
        if r[1] not in d[r[0]]:
            d[r[0]][r[1]] = []
        d[r[0]][r[1]].append(r[2])
print (d.keys())
for key in d.keys():
    print(d[key].keys())