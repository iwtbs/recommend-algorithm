# 1. MostPopular算法
def MostPopular(train, profile, N):
    '''
    :params: train, 训练数据
    :params: profile, 用户的注册信息
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    '''
    
    items = {}
    for user in train:
        for item in train[user]:
            if item not in items:
                items[item] = 0
            items[item] += 1
    items = list(sorted(items.items(), key=lambda x: x[1], reverse=True))
        
    # 获取接口函数
    def GetRecommendation(user):
        seen_items = set(train[user]) if user in train else set()
        recs = [x for x in items if x[0] not in seen_items][:N]
        return recs
    
    return GetRecommendation

# 2. GenderMostPopular算法
def GenderMostPopular(train, profile, N):
    '''
    :params: train, 训练数据
    :params: profile, 用户的注册信息
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    '''
    
    mitems, fitems = {}, {} # 男、女
    for user in train:
        if profile[user]['gender'] == 'm':
            tmp = mitems
        elif profile[user]['gender'] == 'f':
            tmp = fitems
        for item in train[user]:
            if item not in tmp:
                tmp[item] = 0
            tmp[item] += 1
    mitems = list(sorted(mitems.items(), key=lambda x: x[1], reverse=True))
    fitems = list(sorted(fitems.items(), key=lambda x: x[1], reverse=True))
    
    mostPopular = MostPopular(train, profile, N)
    
    # 获取接口函数
    def GetRecommendation(user):
        seen_items = set(train[user]) if user in train else set()
        if profile[user]['gender'] == 'm':
            recs = [x for x in mitems if x[0] not in seen_items][:N]
        elif profile[user]['gender'] == 'f':
            recs = [x for x in fitems if x[0] not in seen_items][:N]
        else: # 没有提供性别信息的，按照MostPopular推荐
            recs = mostPopular(user)
        return recs
    
    return GetRecommendation

# 3. AgeMostPopular算法
def AgeMostPopular(train, profile, N):
    '''
    :params: train, 训练数据
    :params: profile, 用户的注册信息
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    '''
    
    # 对年龄进行分段
    ages = []
    for user in profile:
        if profile[user]['age'] >= 0:
            ages.append(profile[user]['age'])
    maxAge, minAge = max(ages), min(ages)
    items = [{} for _ in range(int(maxAge // 10 + 1))]
    
    # 分年龄段进行统计
    for user in train:
        if profile[user]['age'] >= 0:
            age = profile[user]['age'] // 10
            for item in train[user]:
                if item not in items[age]:
                    items[age][item] = 0
                items[age][item] += 1
    for i in range(len(items)):
        items[i] = list(sorted(items[i].items(), key=lambda x: x[1], reverse=True))
    
    mostPopular = MostPopular(train, profile, N)
    
    # 获取接口函数
    def GetRecommendation(user):
        seen_items = set(train[user]) if user in train else set()
        if profile[user]['age'] >= 0:
            age = profile[user]['age'] // 10
            # 年龄信息异常的，按照全局推荐
            if age >= len(items) or len(items[age]) == 0:
                recs = mostPopular(user)
            else:
                recs = [x for x in items[age] if x[0] not in seen_items][:N]
        else: # 没有提供年龄信息的，按照全局推荐
            recs = mostPopular(user)
        return recs
    
    return GetRecommendation

# 4. CountryMostPopular算法
def CountryMostPopular(train, profile, N):
    '''
    :params: train, 训练数据
    :params: profile, 用户的注册信息
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    '''
        
    # 分城市进行统计
    items = {}
    for user in train:
        country = profile[user]['country']
        if country not in items:
            items[country] = {}
        for item in train[user]:
            if item not in items[country]:
                items[country][item] = 0
            items[country][item] += 1
    for country in items:
        items[country] = list(sorted(items[country].items(), key=lambda x: x[1], reverse=True))
    
    mostPopular = MostPopular(train, profile, N)
    
    # 获取接口函数
    def GetRecommendation(user):
        seen_items = set(train[user]) if user in train else set()
        country = profile[user]['country']
        if country in items:
            recs = [x for x in items[country] if x[0] not in seen_items][:N]
        else: # 没有提供城市信息的，按照全局推荐
            recs = mostPopular(user)
        return recs
    
    return GetRecommendation

# 5. DemographicMostPopular算法
def DemographicMostPopular(train, profile, N):
    '''
    :params: train, 训练数据
    :params: profile, 用户的注册信息
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    '''

    # 建立多重字典，将缺失值当成other，同归为一类进行处理
    items = {}
    for user in train:
        gender = profile[user]['gender']
        if gender not in items:
            items[gender] = {}
        age = profile[user]['age'] // 10
        if age not in items[gender]:
            items[gender][age] = {}
        country = profile[user]['country']
        if country not in items[gender][age]:
            items[gender][age][country] = {}
        for item in train[user]:
            if item not in items[gender][age][country]:
                items[gender][age][country][item] = 0
            items[gender][age][country][item] += 1
    for gender in items:
        for age in items[gender]:
            for country in items[gender][age]:
                items[gender][age][country] = list(sorted(items[gender][age][country].items(), 
                                                          key=lambda x: x[1], reverse=True))
                
    mostPopular = MostPopular(train, profile, N)
    
    # 获取接口函数
    def GetRecommendation(user):
        seen_items = set(train[user]) if user in train else set()
        gender = profile[user]['gender']
        age = profile[user]['age']
        country = profile[user]['country']
        if gender not in items or age not in items[gender] or country not in items[gender][age]:
            recs = mostPopular(user)
        else:
            recs = [x for x in items[gender][age][country] if x[0] not in seen_items][:N]
        return recs
    
    return GetRecommendation