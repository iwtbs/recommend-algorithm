def ContentItemKNN(train, content, K, N):
    '''
    :params: train, 训练数据
    :params: content, 物品内容信息
    :params: K, 取相似Top-K相似物品
    :params: N, 推荐TopN物品的个数
    :return: GetRecommendation, 获取推荐结果的接口
    '''
    
    # 建立word-item倒排表
    word_item = {}
    for item in content:
        for word in content[item]:
            if word not in word_item:
                word_item[word] = {}
            word_item[word][item] = 1
            
    for word in word_item:
        for item in word_item[word]:
            word_item[word][item] /= math.log(1 + len(word_item[word]))

    # 计算相似度
    item_sim = {}
    mo = {}
    for word in word_item:
        for u in word_item[word]:
            if u not in item_sim:
                item_sim[u] = {}
                mo[u] = 0
            mo[u] += word_item[word][u] ** 2
            for v in word_item[word]:
                if u == v: continue
                if v not in item_sim[u]:
                    item_sim[u][v] = 0
                item_sim[u][v] += word_item[word][u] * word_item[word][v]
    for u in item_sim:
        for v in item_sim[u]:
            item_sim[u][v] /= math.sqrt(mo[u] * mo[v])
                
    # 按照相似度排序
    sorted_item_sim = {k: list(sorted(v.items(), \
                               key=lambda x: x[1], reverse=True)) \
                       for k, v in item_sim.items()}
        
    # 获取接口函数
    def GetRecommendation(user):
        items = {}
        seen_items = set(train[user])
        for item in train[user]:
            for u, _ in sorted_item_sim[item][:K]:
                # 要去掉用户见过的
                if u not in seen_items:
                    if u not in items:
                        items[u] = 0
                    items[u] += item_sim[item][u]
        recs = list(sorted(items.items(), key=lambda x: x[1], reverse=True))[:N]
        return recs
    
    return GetRecommendation