# 基于归一化的物品余弦相似度的推荐
def ItemCF_Norm(train, K, N):
    '''
    :params: train, 训练数据集
    :params: K, 超参数，设置取TopK相似物品数目
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation, 推荐接口函数
    '''
    # 计算物品相似度矩阵
    sim = {}
    num = {}
    for user in train:
        items = train[user]
        for i in range(len(items)):
            u = items[i]
            if u not in num:
                num[u] = 0
            num[u] += 1
            if u not in sim:
                sim[u] = {}
            for j in range(len(items)):
                if j == i: continue
                v = items[j]
                if v not in sim[u]:
                    sim[u][v] = 0
                sim[u][v] += 1
    for u in sim:
        for v in sim[u]:
            sim[u][v] /= math.sqrt(num[u] * num[v])
            
    # 对相似度矩阵进行按行归一化
    for u in sim:
        s = 0
        for v in sim[u]:
            s += sim[u][v]
        if s > 0:
            for v in sim[u]:
                sim[u][v] /= s
    
    # 按照相似度排序
    sorted_item_sim = {k: list(sorted(v.items(), \
                               key=lambda x: x[1], reverse=True)) \
                       for k, v in sim.items()}
    
    # 获取接口函数
    def GetRecommendation(user):
        items = {}
        seen_items = set(train[user])
        for item in train[user]:
            for u, _ in sorted_item_sim[item][:K]:
                if u not in seen_items:
                    if u not in items:
                        items[u] = 0
                    items[u] += sim[item][u]
        recs = list(sorted(items.items(), key=lambda x: x[1], reverse=True))[:N]
        return recs
    
    return GetRecommendation