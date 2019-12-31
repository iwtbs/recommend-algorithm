def PersonalRank(train, alpha, N):
    '''
    :params: train, 训练数据
    :params: alpha, 继续随机游走的概率
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    ''' 
    
    # 构建索引
    items = []
    for user in train:
        items.extend(train[user])
    id2item = list(set(items))
    users = {u: i for i, u in enumerate(train.keys())}
    items = {u: i+len(users) for i, u in enumerate(id2item)}
    
    # 计算转移矩阵（注意！！！要按照出度进行归一化）
    item_user = {}
    for user in train:
        for item in train[user]:
            if item not in item_user:
                item_user[item] = []
            item_user[item].append(user)
            
    data, row, col = [], [], []
    for u in train:
        for v in train[u]:
            data.append(1 / len(train[u]))
            row.append(users[u])
            col.append(items[v])
    for u in item_user:
        for v in item_user[u]:
            data.append(1 / len(item_user[u]))
            row.append(items[u])
            col.append(users[v])
            
    M = csc_matrix((data, (row, col)), shape=(len(data), len(data)))
    
    # 获取接口函数
    def GetRecommendation(user):
        seen_items = set(train[user])
        # 解矩阵方程 r = (1-a)r0 + a(M.T)r
        r0 = [0] * len(data)
        r0[users[user]] = 1
        r0 = csc_matrix(r0)
        r = (1 - alpha) * linalg.inv(eye(len(data)) - alpha * M.T) * r0
        r = r.T.toarray()[0][len(users):]
        idx = np.argsort(-r)[:N]
        recs = [(id2item[ii], r[ii]) for ii in idx]
        return recs
    
    return GetRecommendation