# 随机推荐
def Random(train, K, N):
    '''
    :params: train, 训练数据集
    :params: K, 可忽略
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation，推荐接口函数
    '''
    items = {}
    for user in train:
        for item in train[user]:
            items[item] = 1
    
    def GetRecommendation(user):
        # 随机推荐N个未见过的
        user_items = set(train[user])
        rec_items = {k: items[k] for k in items if k not in user_items}
        rec_items = list(rec_items.items())
        random.shuffle(rec_items)
        return rec_items[:N]
    
    return GetRecommendation

# 热门推荐
def MostPopular(train, K, N):
    '''
    :params: train, 训练数据集
    :params: K, 可忽略
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation, 推荐接口函数
    '''
    items = {}
    for user in train:
        for item in train[user]:
            if item not in items:
                items[item] = 0
            items[item] += 1
        
    def GetRecommendation(user):
        # 随机推荐N个没见过的最热门的
        user_items = set(train[user])
        rec_items = {k: items[k] for k in items if k not in user_items}
        rec_items = list(sorted(rec_items.items(), key=lambda x: x[1], reverse=True))
        return rec_items[:N]
    
    return GetRecommendation