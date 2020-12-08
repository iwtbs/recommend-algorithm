# 因子分解排序
## FM
FM和树模型都能够自动学习特征交叉组合，但树的模型只适合连续型或值空间较小的稀疏数据；另一方面树模型也不能学习到训练数据中很少或没有出现的特征组合，因为树模型只是对历史的一个记忆，泛化能力较弱。相反，FM模型因为通过隐向量的内积来提取特征组合，对于训练数据中很少或没有出现的特征组合也能够学习到

FM可以解决特征组合以及高维稀疏矩阵问题
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225162835212.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225162909827.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
## FFM
FM模型中，每一个特征对应一个向量；FFM中认为每一个特征对于每一个域field对应一个向量。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225164600582.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225164804771.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
FFM的组合特征有10项，如下图所示
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225164814121.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
其中，红色是field编号，蓝色是特征编号

# 树模型排序
## GBDT+LR
facebook采用了这个模型，树的数量《=500，每棵树的节点《=12，大致有三种组合方案
1. 离散特征onehot + 连续特征gbdt
2. 低频离散特征onehot + 连续特征/高频离散特征 gbdt
3. 原始特征onehot + ID类gbdt + 非id类gbdt
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225193555470.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
【LR特征如何处理】为了让线性模型能够学习到原始特征与拟合目标之间的非线性关系，通常需要对原始特征做一些非线性转换。常用的转换方法包括：特征聚类、连续特征离散化（包括等频离散、等间距离散，或者采用树模型通过gain来找到最优分裂点进行划分）、特征交叉（数值累加、累乘，类目组合等）等

【为什么建树采用GBDT而非RF】：很多实践证明GBDT的效果要优于RF，且GBDT前面的树，特征分裂主要体现对多数样本有区分度的特征；后面的树，主要体现的是经过前N颗树，残差仍然较大的少数样本。优先选用在整体上有区分度的特征，再选用针对少数样本有区分度的特征，思路更加合理，这应该也是用GBDT的原因

- gbdt只是历史记忆，没有泛化能力
# 深度模型排序
发展历程可以参考我的文章[推荐算法—ctr预估](https://blog.csdn.net/qq_34219959/article/details/103822973)
这里只画出结构，写一些面试注意点
- LR模型采用原始人工特征交叉
- FM自动学习xi和xj的二阶交叉特征
- PNN用内积、外积做二阶交叉
- NFM、AFM采用BI-Interaction方式学习二阶交叉
- 更高阶：DCN，任意进行特征交叉，且不增加网络参数
- DIN在embeeding层后做了一个action unit操作，对用户的兴趣分布进行学习后再输入DNN
## FNN
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225194754116.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- 利用DNN优化高阶特征
- wide deep的深度部分就是这样的结构
## Wide Deep
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225222559707.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
特征工程后的离散特征：线性模型
离散+连续：DNN
## Deepfm
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225222644220.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
离散+连续：线性模型
离散：FM
离散+连续：DNN
## PNN
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020022522430542.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- z是embedding层的复制，p有IPNN和OPNN两种
- embbeding大小:M,filed大小:N
- IPNN是内积，OPNN是矩阵

## NFM
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020022522462527.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- Bi-Interaction Layer名字挺高大上的，其实它就是计算FM中的二次项的过程
## AFM
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225224657238.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- attention相等于加权的过程，因此我们的预测公式变为![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301220346890.png)
圆圈中有个点的符号代表的含义是element-wise product
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301220619511.png)
- 后面两部分，则是AFM的创新所在，也就是我们的Attention net
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301221135722.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- 没经过DNN
## DCN
- 提出了一种新的交叉网络，在每个层上明确地应用特征交叉，有效地学习有界度的预测交叉特征，并且不需要手工特征工程或穷举搜索
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225224718538.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
交叉层：
交叉维度为L层交叉网络层数L + 1
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301211911362.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301211816986.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
## MLR
用分片线性的模式来拟合高维空间的非线性分类面
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301221547838.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- MLR在建模时引入了L1和L2，模型具有较高的稀疏度， 模型的学习和在线预测性能更好
## DIN

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225224752423.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- 用户特征、用户行为特征、广告特征、上下文特征
- embedding之后，使用weighted-sum，即attention
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301224310165.png)
- 评价指标是GAUC
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020030122442342.png)
根据用户的展示数或者点击数来对每个用户的AUC进行加权处理
- Dice激活函数。
PRelu、Relu 认为分割点都是0，Dice每一个yi对应了一个概率值pi，pi的计算主要分为两步：将yi进行标准化和进行sigmoid变换
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200301225707515.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- 自适应正则。针对feature id出现的频率，来自适应的调整他们正则化的强度；对于出现频率高的，给与较小的正则化强度；对于出现频率低的，给予较大的正则化强度
## DIEN
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225224827644.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
- DIN没有考虑用户历史之间的时序关系, DIEN则使用了GRU来建模用户历史的时间序列
- 用户历史肯定是一个时间序列，将其喂入RNN，则最后一个状态可以认为包含了所有历史信息。因此，作者用一个双层的GRU来建模用户兴趣。
- 将用户历史接触过的item embedding微量，喂进第一层GRU，输出的就是用户各时刻的兴趣。这一层被称为Interest Extraction Layer
- 将第一层的输出，喂进第二层GRU，并用attention score（基于第一层的输出向量与候选物料计算得出）来控制第二层的GRU的update gate。这一层叫做Interest Evolving Layer。
- Interest Evolving Layer的最后一个状态作为用户兴趣的向量表示，与ad, context的特征一同喂入MLP，预测点击率。
## DSIN
[DSIN](https://zhuanlan.zhihu.com/p/97015090)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200225224933683.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
主要贡献在于对用户的历史点击行为划分为不同session，对每个session使用Transformer学习session embedding，最后使用BiLSTM对session序列建模
- Session Division Layer是对用户的历史行为划分到不同session
将间隔超过30分钟作为session的划分。
- Session Interest Interacting Layer是学习session之间的表征
相同session内的行为是高度相关的，在session内的一些随意行为会偏离整个session表达。为了刻画相同session内行为间的相关性，同时减小不相关行为的影响。
DSIN使用**multi-head self-attention**对每个session建模。为了刻画不同session间的顺序，DSIN使用了**Bias Encoding**
Bias Encoding：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200302104939957.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
multi-head self-attention：
将第k个session划分为H个head
![](https://img-blog.csdnimg.cn/20200302105442214.png)
- Session Interest Interacting Layer是学习session之间的演变
使用双向LSTM建模session之间的演变
- Session Interest Activating Layer是学习当前item和历史点击session的相关性
通过Attention机制刻画Item和session之间的相关性。用户的session与目标物品越相近，越应该赋予更大的权重
## MIND
召回阶段建模表达用户的多样兴趣
既然使用一个向量表达用户多样兴趣有困难，那么为什么不使用一组向量呢？具体来说，如果我们可以对用户历史行为的embedding进行聚类，聚类后的每个簇代表用户的一组兴趣

胶囊网络(Capsule Network)
Capsule输入是一组向量，对这组向量进行仿射变换之后求加权和，把加权和输入非线性激活函数得到一个向量的输出
如果我们K个capsule，就会有K个输出向量
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200404164212641.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200404165952426.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)

## MIMN
- **UIC的提出**：（ 背景）存储用户行为序列需要空间太大，且RNN类模型速度慢。（改进）于是构建了一个单独的模块UIC来完成用户行为序列的建模计算工作。UIC server负责存储每个用户最近的行为兴趣，而且UIC server的核心在于其更新策略，即用户行为序列的更新只依赖于具体的触发事件，而不依赖于请求。
- 一方面是NTM中基本的memory read和memory write操作；另一方面是为提取高阶信息而采用多通道GRU的memory induction unit。网络的右侧则为传统的embedding+MLP的经典结构
## DMR
DMR（Deep Match to Rank）
通过User-to-Item子网络和Item-to-Item子网络来表征U2I相关性，进一步提升模型的表达能力
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200325092025809.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70)