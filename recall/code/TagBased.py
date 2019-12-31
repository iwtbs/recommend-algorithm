# 1. 基于热门标签的推荐
def SimpleTagBased(train, N):
    '''
    :params: train, 训练数据集
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation，推荐接口函数
    '''
    # 统计user_tags和tag_items
    user_tags, tag_items = {}, {}
    for user in train:
        user_tags[user] = {}
        for item in train[user]:
            for tag in train[user][item]:
                if tag not in user_tags[user]:
                    user_tags[user][tag] = 0
                user_tags[user][tag] += 1
                if tag not in tag_items:
                    tag_items[tag] = {}
                if item not in tag_items[tag]:
                    tag_items[tag][item] = 0
                tag_items[tag][item] += 1
    
    def GetRecommendation(user):
        # 按照打分推荐N个未见过的
        if user not in user_tags:
            return []
        seen_items = set(train[user])
        item_score = {}
        for tag in user_tags[user]:
            for item in tag_items[tag]:
                if item in seen_items:
                    continue
                if item not in item_score:
                    item_score[item] = 0
                item_score[item] += user_tags[user][tag] * tag_items[tag][item]
        item_score = list(sorted(item_score.items(), key=lambda x: x[1], reverse=True))
        return item_score[:N]
    
    return GetRecommendation

# 2. 改进一：为热门标签加入惩罚项
def TagBasedTFIDF(train, N):
    '''
    :params: train, 训练数据集
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation，推荐接口函数
    '''
    # 统计user_tags和tag_items
    user_tags, tag_items = {}, {}
    # 统计标签的热门程度，即打过此标签的不同用户数
    tag_pop = {}
    for user in train:
        user_tags[user] = {}
        for item in train[user]:
            for tag in train[user][item]:
                if tag not in user_tags[user]:
                    user_tags[user][tag] = 0
                user_tags[user][tag] += 1
                if tag not in tag_items:
                    tag_items[tag] = {}
                if item not in tag_items[tag]:
                    tag_items[tag][item] = 0
                tag_items[tag][item] += 1
                if tag not in tag_pop:
                    tag_pop[tag] = set()
                tag_pop[tag].add(user)
    tag_pop = {k: len(v) for k, v in tag_pop.items()}
    
    def GetRecommendation(user):
        # 按照打分推荐N个未见过的
        if user not in user_tags:
            return []
        seen_items = set(train[user])
        item_score = {}
        for tag in user_tags[user]:
            for item in tag_items[tag]:
                if item in seen_items:
                    continue
                if item not in item_score:
                    item_score[item] = 0
                item_score[item] += user_tags[user][tag] * tag_items[tag][item] / tag_pop[tag]
        item_score = list(sorted(item_score.items(), key=lambda x: x[1], reverse=True))
        return item_score[:N]
    
    return GetRecommendation

# 3. 改进二：同时也为热门商品加入惩罚项
def TagBasedTFIDF_Improved(train, N):
    '''
    :params: train, 训练数据集
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation，推荐接口函数
    '''
    # 统计user_tags和tag_items
    user_tags, tag_items = {}, {}
    # 统计标签和物品的热门程度，即打过此标签的不同用户数，和物品对应的不同用户数
    tag_pop, item_pop = {}, {}
    for user in train:
        user_tags[user] = {}
        for item in train[user]:
            if item not in item_pop:
                item_pop[item] = 0
            item_pop[item] += 1
            for tag in train[user][item]:
                if tag not in user_tags[user]:
                    user_tags[user][tag] = 0
                user_tags[user][tag] += 1
                if tag not in tag_items:
                    tag_items[tag] = {}
                if item not in tag_items[tag]:
                    tag_items[tag][item] = 0
                tag_items[tag][item] += 1
                if tag not in tag_pop:
                    tag_pop[tag] = set()
                tag_pop[tag].add(user)
    tag_pop = {k: len(v) for k, v in tag_pop.items()}
    
    def GetRecommendation(user):
        # 按照打分推荐N个未见过的
        if user not in user_tags:
            return []
        seen_items = set(train[user])
        item_score = {}
        for tag in user_tags[user]:
            for item in tag_items[tag]:
                if item in seen_items:
                    continue
                if item not in item_score:
                    item_score[item] = 0
                item_score[item] += user_tags[user][tag] * tag_items[tag][item] / tag_pop[tag] / item_pop[item]
        item_score = list(sorted(item_score.items(), key=lambda x: x[1], reverse=True))
        return item_score[:N]
    
    return GetRecommendation

# 4. 基于标签改进的推荐
def ExpandTagBased(train, N, M=20):
    '''
    :params: train, 训练数据集
    :params: N, 超参数，设置取TopN推荐物品数目
    :params: M，超参数，设置取TopM的标签填补不满M个标签的用户
    :return: GetRecommendation，推荐接口函数
    '''
    
    # 1. 计算标签之间的相似度
    item_tag = {}
    for user in train:
        for item in train[user]:
            if item not in item_tag:
                item_tag[item] = set()
            for tag in train[user][item]:
                item_tag[item].add(tag)
    tag_sim, tag_cnt = {}, {}
    for item in item_tag:
        for u in item_tag[item]:
            if u not in tag_cnt:
                tag_cnt[u] = 0
            tag_cnt[u] += 1
            if u not in tag_sim:
                tag_sim[u] = {}
            for v in item_tag[item]:
                if u == v:
                    continue
                if v not in tag_sim[u]:
                    tag_sim[u][v] = 0
                tag_sim[u][v] += 1
    for u in tag_sim:
        for v in tag_sim[u]:
            tag_sim[u][v] /= math.sqrt(tag_cnt[u] * tag_cnt[v])
    
    # 2. 为每个用户扩展标签
    user_tags = {}
    for user in train:
        if user not in user_tags:
            user_tags[user] = {}
        for item in train[user]:
            for tag in train[user][item]:
                if tag not in user_tags[user]:
                    user_tags[user][tag] = 0
                user_tags[user][tag] += 1
    expand_tags = {}
    for user in user_tags:
        if len(user_tags[user]) >= M:
            expand_tags[user] = user_tags[user]
            continue
        # 不满M个的进行标签扩展
        expand_tags[user] = {}
        seen_tags = set(user_tags[user])
        for tag in user_tags[user]:
            for t in tag_sim[tag]:
                if t in seen_tags:
                    continue
                if t not in expand_tags[user]:
                    expand_tags[user][t] = 0
                expand_tags[user][t] += user_tags[user][tag] * tag_sim[tag][t]
        expand_tags[user].update(user_tags[user])
        expand_tags[user] = dict(list(sorted(expand_tags[user].items(), key=lambda x: x[1], reverse=True))[:M])
        
    # 3. SimpleTagBased算法
    tag_items = {}
    for user in train:
        for item in train[user]:
            for tag in train[user][item]:
                if tag not in tag_items:
                    tag_items[tag] = {}
                if item not in tag_items[tag]:
                    tag_items[tag][item] = 0
                tag_items[tag][item] += 1
    
    def GetRecommendation(user):
        # 按照打分推荐N个未见过的
        if user not in user_tags:
            return []
        seen_items = set(train[user])
        item_score = {}
        for tag in expand_tags[user]:
            for item in tag_items[tag]:
                if item in seen_items:
                    continue
                if item not in item_score:
                    item_score[item] = 0
                item_score[item] += expand_tags[user][tag] * tag_items[tag][item]
        item_score = list(sorted(item_score.items(), key=lambda x: x[1], reverse=True))
        return item_score[:N]
    
    return GetRecommendation