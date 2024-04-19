def give_me_problem(handle,weak_tags,Table):
    import pandas as pd
    import numpy as np

    from sklearn.feature_extraction.text import CountVectorizer

    cv = CountVectorizer()


    vectors = cv.fit_transform(Table['Tags']).toarray()

    cv.get_feature_names_out()

    from sklearn.metrics.pairwise import cosine_similarity

    similarity = cosine_similarity(vectors)
    import requests
    import json
    def isSolved(id, index):
        url = 'https://codeforces.com/api/contest.standings?contestId=' + str(
            id) + '&showUnofficial=true&handles=' + handle
        try:
            response = requests.get(url)
            x = response.json()
        except:
            print("Failed to Get contest Data")
            return False
        idx = 0
        x = x['result']
        cnt = 0
        for p in x['problems']:
            if p['index'] == index:
                idx = cnt
                break
            cnt = cnt + 1

        for res in x['rows']:
            if int(res['problemResults'][idx]['points']) > 0:
                return True

        return False


    def recommend(weak_tags):
        weak_vector = cv.transform([weak_tags]).toarray()
        similarity = cosine_similarity(weak_vector, vectors)
        distance = similarity[0]
        my_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])
        problem_list = list()
        for x in my_list:
            problem = Table.iloc[x[0]]
            if isSolved(problem.PID,problem.Index)==False:
                problem_list.append(x[0])
            if len(problem_list)>10:
                break
        return problem_list

    res = recommend(weak_tags)
    return res