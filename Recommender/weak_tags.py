import requests
import json
from .Target import get_lo_hi
from Dataset.models import Counter
def get_weak_tags(handle):
    url = 'https://codeforces.com/api/user.rating?handle=' + handle
    try:
        response = requests.get(url)
        x = response.json()
    except:
        return 'null'
    (current,target) = get_lo_hi(handle)
    if current==-1:
        return  'null'
    start = 1332435435465465656656765767676576577678775
    for con in x['result']:
        if con['newRating'] >= con['oldRating'] and con['newRating']>=current:
            start = min(start,con['ratingUpdateTimeSeconds'])
    url = 'https://codeforces.com/api/user.status?handle=' + handle + '&from=1'
    try:
        response = requests.get(url)
    except:
        return 'null'
    map = {}
    weak_tags=[]
    x = response.json()
    for sub in x['result']:
        if start <= sub['creationTimeSeconds'] and sub['verdict'] == 'OK':
            if 'rating' in sub['problem'] and sub['problem']['rating'] > current:
                tags = sub['problem']['tags']
                tags.append(str(sub['problem']['rating']))
                for i in range(len(tags)):
                    tags[i] = tags[i].replace(" ", "");
                    tags[i] = tags[i].replace("-", "");
                    if tags[i] not in map:
                        map.update({str(tags[i]):1})
                    else:
                        map[tags[i]]+=1
                tags = ', '.join(tags)
    nob = Counter.objects.filter(Tag_Name = 'users').last()
    print(map)
    percentage =[]
    for ob in Counter.objects.all():
        if ob.Tag_Name== 'users':
            continue
        dorkar =0
        if target == 1200:
            dorkar = ob.Pupil//nob.Pupil
        if target == 1400:
            dorkar = ob.Specialist//nob.Specialist
        if target == 1600:
            dorkar = ob.Expert//nob.Expert
        if target == 1900:
            dorkar = ob.Candidate_Master//nob.Candidate_Master
        if target == 2100:
            dorkar = ob.Master//nob.Master
        ase =0
        if ob.Tag_Name in map:
            ase= map[ob.Tag_Name]
        if ase < dorkar:
            percentage.append(round((dorkar-ase)*100/dorkar))
            weak_tags.append(str(ob.Tag_Name))
    weak_tags = ', '.join(weak_tags)
    return (weak_tags, percentage)