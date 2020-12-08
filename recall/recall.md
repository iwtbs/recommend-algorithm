# 召回
## 内容召回
### word2vec
- 了解skip-gram和cbow两种网络的结构
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225161740893.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- 了解优化方法：Hierarchical Softmax和Negative Sampling
（1）Hierarchical Softmax
霍夫曼树，频度高的词越靠近根节点，复杂度从n降到log2n
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225161832322.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
（2）负采样
每次都只是通每次都只是通过采样neg个不同的中心词做负例，就可以训练模型过采样neg个不同的中心词做负例，转化为二分类问题。
采样的词尽量是热门词
### LDA
我们认为一篇文章的每个词都是通过“以一定概率选择了某个主题，并从这个主题中以一定概率选择某个词语”这样一个过程得到。
文档到主题服从多项式分布，主题到词服从多项式分布。
**核心思想：LDA的目的就是要识别主题，即把文档—词汇矩阵变成文档—主题矩阵（分布）和主题—词汇矩阵（分布）**

对于语料库中的每篇文档，LDA定义了如下生成过程：
1.对每一篇文档，从主题分布中抽取一个主题；
2.从上述被抽到的主题所对应的单词分布中抽取一个单词；
3.重复上述过程直至遍历文档中的每一个单词。
[博客](https://www.jianshu.com/p/fa97454c9ffd)



## 行为召回
### ItemCF
- 对活跃用户进行惩罚。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225130520304.png)
- UserCF的推荐结果着重于反映和用户兴趣相似的小群体的热点，而ItemCF的推荐结果着重于维系用户的历史兴趣
- UserCF比较适合用于新闻推荐等热门程度和实时性较强的场景，ItemCF则适用于图书、电商、电影等场景
### UserCF
- 对热门物品进行惩罚
- 在计算用户行为之间的相似度时，建立Item-User的倒排表，这样在同一个Item下面的User两两之间一定是在这个Item上有交集的，所以只需要遍历所有的Item，对其下所有的User两两进行统计即可，这样可以极大降低时间复杂度。

**CF实效成本低，全量发现能力弱，基于历史相似扩展；存在冷启动问题**
### Swing
阿里原创算法-swing，基于图结构做match，计算商品间的相似度
如果多个user在点击了s的同时，都只共同点了某一个其他的item，那么这个item和s一定是强关联的

### 关联规则
找出用户购买的所有物品数据里频繁出现的项集活序列，来做频繁集挖掘，找到满足支持度阈值的关联物品的频繁N项集或者序列。如果用户购买了频繁N项集或者序列里的部分物品，那么我们可以将频繁项集或序列里的其他物品按一定的评分准则推荐给用户，这个评分准则可以包括支持度，置信度和提升度等

常用的关联推荐算法有Apriori，FP Tree和PrefixSpan。如果大家不熟悉这些算法，可以参考我的另外几篇文章：
[Apriori算法](https://blog.csdn.net/qq_34219959/article/details/102381162)
[FpGrowth算法](https://blog.csdn.net/qq_34219959/article/details/102390588)
[序列模式挖掘PrefixSpan算法](https://blog.csdn.net/qq_34219959/article/details/97015246)
### 聚类协同
常用的聚类推荐算法有K-Means, BIRCH, DBSCAN和谱聚类

介绍下DBSCAN
- DBSCAN的主要优点有：
（1） 可以对任意形状的稠密数据集进行聚类，相对的，K-Means之类的聚类算法一般只适用于凸数据集。
（2） 可以在聚类的同时发现异常点，对数据集中的异常点不敏感。
（3） 聚类结果没有偏倚，相对的，K-Means之类的聚类算法初始值对聚类结果有很大影响。
- DBSCAN的主要缺点有：
（1）如果样本集的密度不均匀、聚类间距差相差很大时，聚类质量较差，这时用DBSCAN聚类一般不适合。
（2） 如果样本集较大时，聚类收敛时间较长，此时可以对搜索最近邻时建立的KD树或者球树进行规模限制来改进。
（3） 调参相对于传统的K-Means之类的聚类算法稍复杂，主要需要对距离阈值ϵ，邻域样本数阈值MinPts联合调参，不同的参数组合对最后的聚类效果有较大影响
## 矩阵分解
### 隐语义LFM
- 用两个低阶向量相乘来模拟实际的User-Item矩阵
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225130819331.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225131153230.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225131412990.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225131401259.png)
- label要怎么标注？
一般数据集里面的都是只有正向反馈，即只有标签1，这时就需要进行负采样，即采出标签0来。采样是针对每个用户来进行的，对于每个用户，负采样的Item要遵循如下原则：
（1）对每个用户，要保证正负样本的平衡(数目相似)。
（2）对每个用户采样负样本时，要选取那些很热门，而用户却没有行为的物品。
- 离线计算的空间复杂度：基于邻域的方法需要维护一张离线的相关表。假设有M个用户和N个物品，UserCF需要$O(M∗M)$的空间，ItemCF需要$O(N∗N)$的空间，而对于LFM，有F个隐类的话，需要$O(F∗(M+N))$的空间
- LFM不太适合用于物品数非常庞大的系统，如果要用，我们也需要一个比较快的算法给用户先计算一个比较小的候选列表，然后再用LFM重新排名。另一方面，LFM在生成一个用户推荐列表时速度太慢，因此不能在线实时计算，而需要离线将所有用户的推荐结果事先计算好存储在数据库中。因此，LFM不能进行在线实时推荐，也就是说，当用户有了新的行为后，他的推荐列表不会发生变化。
## 图召回
### PersonalRank
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020022513152310.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225131613954.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
## 图嵌入
- deepwalk
- line
相比DeepWalk纯粹随机游走的序列生成方式，LINE可以应用于有向图、无向图以及边有权重的网络，并通过将一阶、二阶的邻近关系引入目标函数，能够使最终学出的node embedding的分布更为均衡平滑，避免DeepWalk容易使node embedding聚集的情况发生。
- node2vec
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020030222532484.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- SDNE
相比于node2vec对游走方式的改进，SDNE模型主要从目标函数的设计上解决embedding网络的局部结构和全局结构的问题。而相比LINE分开学习局部结构和全局结构的做法，SDNE一次性的进行了整体的优化，更有利于获取整体最优的embedding。
- 阿里EGES
阿里通过引入side information解决embedding问题非常棘手的冷启动问题，不同的side information有权重。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200302233300405.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
### 图神经网络模型召回
知识图谱是图神经网络的特例，但是，知识图谱编码的是静态知识，而不是用户直接的行为数据，和具体应用距离较远，这可能是导致两者在推荐领域表现差异的主要原因
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200229234345769.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
知识图谱其实是图神经网络的一个比较特殊的具体实例，但是，知识图谱因为编码的是静态知识，而不是用户比较直接的行为数据，和具体应用距离比较远，这可能是导致两者在推荐领域表现差异的主要原因。信息在图中的传播性，所以对于推荐的冷启动以及数据稀疏场景应该特别有用。
图神经网络做推荐，因为需要全局信息，所以计算速度是个问题
GraphSAGE 则通过一些手段比如从临近节点进行采样等减少计算规模，加快计算速度，很多后期改进计算效率的方法都是从这个工作衍生的；而 PinSage 在 GraphSAGE 基础上 ( 这是同一拨人做的 )，进一步采取大规模分布式计算，拓展了图计算的实用性，可以计算 Pinterest 的30亿规模节点、180亿规模边的巨型图，并产生了较好的落地效果。
## item2vec（embedding）
思想：用户、物品分别embedding
好处：多路召回每路截断条数的超参个性化问题等会自然被消解掉
坏处：召回内容头部问题（训练数据对头部领域的降采样，减少某些领域主导，以及在模型角度鼓励多样性等不同的方法）
注意：召回阶段使用模型召回，也应该同步采用和排序模型相同的优化目标，尤其是如果排序阶段采用多目标优化的情况下，召回模型也应该对应采取相同的多目标优化。
### FM模型召回
[FM模型召回](https://zhuanlan.zhihu.com/p/58160982?from_voters_page=true)
1. 离线训练
我们想要的其实是：每个特征和这个特征对应的训练好的embedding向量
2. 映射函数
用户特征，物品特征以及上下文特征。
用户向量存入在线数据库中比如Redis，物品向量存入Faiss(Facebook开源的embedding高效匹配库)数据库中
### 双塔模型
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200303153108766.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200302203528282.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
### aribnb的embedding策略
1. click session：切片点击序列，然后每个序列用w2v来embedding。序列要求（停留时间超过30s才是有效物品；超过30分钟没有动作就切片）。
2. book session：购买行为很稀疏（总量小，单一用户行为少），所以不能用w2v那一套，只能基于某些属性规则做相似user和相似listing的聚合。
### 用户行为序列召回
输入是用户行为过的物品序列，可以只用物品 ID 表征，也可以融入物品的 Side  Information，需要通过一定的方法把这些进行糅合到一个 embedding 里，代表了用户兴趣。
GRU ( RNN 的变体模型 ) 可能是聚合用户行为序列效果最好又比较简单的模型
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200229230814739.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
用户往往是多兴趣的，所以又引申出了多兴趣拆分。
### 多兴趣拆分
用户多兴趣拆分与用户行为序列召回相比，输入是一样的，输出不同，由输出单独一个用户 embedding，换成输出多个用户兴趣 embedding 
把不同的 Item，聚类到不同的兴趣类别里去，聚类方法常用胶囊网络和 Memory Network
## 知识图谱融合
用于做推荐，一般有两大类知识图谱融合模式：知识图谱 Embedding 模式 ( KGE ) 及图路径模式
- 知识图谱 Embedding 模式：用 TransE 将节点和边转换成 Embedding ，计算距离扩展物品的信息含量。（可解释性不佳）
- 图路径模式：人工定义的知识图谱中知识的关联和传播模式，通过中间属性来对知识传播进行路径搭建（效果不好）
## 深度树TDM
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020030214313682.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- 检索方法是自顶向下Beam Search
- 如何对每层选取Top-K节点，具体做法就如上图中的红色框的部分，该部分的输入包括用户的历史行为特征以及节点的Embedding特征，在对每一层选取Top-K的时候，需要将这一层的每一个节点输入左侧模型中得到相应的预测分数，最终根据分数来取Top。（涉及到对负样本的采样操作）
- 在初始化树结构的时候，首先借助商品的类别信息进行排序，将相同类别的商品放到一起，然后递归的将同类别中的商品等量的分到两个子类中，直到集合中只包含一项，利用这种自顶向下的方式来初始化一棵树。基于该树采样生成深度模型训练所需的样本，然后进一步训练模型，训练结束之后可以得到每个树节点对应的Embedding向量，利用节点的Embedding向量，采用K-Means聚类方法来重新构建一颗树，最后基于这颗新生成的树，重新训练深层网络