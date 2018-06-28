result = ((u'Raaz', u'AMC Metrion', 1, '15:30:00', u'2'), (u'Raaz', u'AMC Metrion', 1, '18:30:00', u'2'), (u'Raazi', u'AMC Metrion', 1, '12:30:00', u'2'), (u'Raazi', u'AMC Metrion', 1, '15:00:00', u'3'), (u'Raazi', u'AMC Metrion', 1, '18:30:00', u'4'), (u'Raaz', u'AMC Van Ness', 2, '17:00:00', u'3'))
d = {}

for r in result:
    if r[0] not in d:
        # print(r[0])
        d[r[0]] = {}
        # if r[1] not in d[r[0]]:
        d[r[0]][r[1]] = []
        d[r[0]][r[1]].append({})
        for dict in d[r[0]][r[1]]:
            dict['show_timing'] = []
            dict['show_timing'].append(r[3])
            dict['theater_id'] = r[2]
            dict['screen_id'] = r[4]
    else:
        if r[1] not in d[r[0]]:
            d[r[0]][r[1]] = []
            d[r[0]][r[1]].append({})
            for dict in d[r[0]][r[1]]:
                dict['show_timing'] = []
                dict['show_timing'].append(r[3])
                dict['theater_id'] = r[2]
                dict['screen_id'] = r[4]
        else:
            flag = 0
            for dict in d[r[0]][r[1]]:
                if dict['screen_id'] == r[4]:
                    dict['show_timing'].append(r[3])
                    flag = 1
            if flag == 0:
                d[r[0]][r[1]].append({})
                list_dict = d[r[0]][r[1]]
                last_dict = list_dict[-1]
                last_dict['show_timing'] = []
                last_dict['show_timing'].append(r[3])
                last_dict['theater_id'] = r[2]
                last_dict['screen_id'] = r[4]

print(d)
print(d['Raazi']['AMC Metrion'])
for dict in d['Raazi']['AMC Metrion']:
    # print(dict)
    # for time in dict['show_timing']:
    #     print(time)
    print(dict['screen_id'])
