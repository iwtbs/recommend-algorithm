Exploration and Exploitation(EE问题，探索与开发）是推荐领常见的问题，主要是为了平衡准确性和多样性。
Exploitation是指我们要迎合用户兴趣给他推荐他想要的，Exploitation指的是怕用户腻，所以要推一些新的东西，万一用户感兴趣呢是吧。

多臂老虎机问题就很像推荐这个场景，我们不知道每个机器吐钱的分布，只能根据现有的知识摇，如果一直摇所知最高的就是Exploitation，但这个吐钱最多的未必是真的，还需要通过Exploitation来探索。
# 先验知识
1. 累积遗憾
错误的选择到底有多少遗憾，累计遗憾如下
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201119000259278.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70#pic_center)
t表示轮数，r表示回报。左边可以认为是最理想情况下的总收益，右边是自己策略的总收益。

2. Beta分布
beta分布可以看作一个概率的概率分布，当你不知道一个东西的具体概率是多少时，它可以给出了所有概率出现的可能性大小。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201119000841403.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70#pic_center)
a和b分别代表在a+b次伯努利实验中成功和失败的次数
# 朴素Bandit算法
先随机尝试若干次，统计每个臂的平均收益，选最多的那个一直摇
# Epsilon-Greedy算法
选0-1间较小的数epsilon，每次以epsilon的概率选一个臂，以1-epsilon的概率选目前最好的臂，根据该次回报值对回报期望进行更新。
优点是有了探索的行为，并且可以调整权重，epsilon=0相当于完全不探索。
缺点是实际上epsilon理想情况下应该是动态的，前期多探索，等后期稳定了就少探索一点。
# 汤普森采样
使用了beta分布，假设每个臂都有一个吐钱的概率p，同时每个臂都可以维护一个beta分布。
诶次选择臂的方式是：用每个臂现有的beta分布产生一个随机数b，选择所有数中最大的那个摇
# UCB算法
解决Epsilon-Greedy的缺点，因为之前提到了Epsilon-Greedy并没有利用到之前的信息，包括臂吐钱的概率和探索的次数。
根据当前每个臂探索的次数和吐钱的次数，其实可以计算出每个臂吐钱的观测概率P'，真实的概率假设是P，核心就是计算gap
我们先确定两个事实：(1)每个臂选择的次数越多，gap越小 (2)对于没被选中的老虎机，gap会随着轮数的增大而增大
ucb算法中p=p’+gap的计算如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201119002551164.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70#pic_center)
T是目前的试验次数，n是臂被试次数
# LinUCB
传统的实现方法存在很大的缺陷，主要是缺乏用附加信息刻画决策过程的机制。
在推荐系统中，通常把待推荐的商品作为MAB问题的arm。UCB是context-free类的算法，没有充分利用推荐场景的上下文信息，为所有用户的选择展现商品的策略都是相同的，忽略了用户作为一个个活生生的个性本身的兴趣点、偏好、购买力等因素，因而，同一个商品在不同的用户、不同的情景下接受程度是不同的。故在实际的推荐系统中，context-free的MAB算法基本都不会被采用。
在LinUCB中，每一个arm维护一组参数，用户和每一个arm的组合可以形成一个上下文特征（上下文特征的特征维度为d），那么对于一个用户来说，在每个arm上所能够获得的期望收益如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201119003327116.png#pic_center)
对于一个老虎机来说，假设收集到了m次反馈，特征向量可以写作Da(维度为md)，假设我们收到的反馈为Ca(维度为m1)，那么通过求解下面的loss，我们可以得到当前每个老虎机的参数的最优解：
其实就是岭回归，我们很容易得到最优解为：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201119004320393.png#pic_center)
既然是UCB方法的扩展，我们除了得到期望值外，我们还需要一个置信上界，但是，我们没法继续用Chernoff-Hoeffding Bound的定理来量化这个上界，幸运的是，这个上界已经被人找到了：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201119004445232.png#pic_center)
因此，我们推荐的item就能够确定了：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201119004512284.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjE5OTU5,size_16,color_FFFFFF,t_70#pic_center)
可以看到，我们在计算参数及最后推荐结果的时候，用到了以下几部分的信息：上下文特征x，用户的反馈c。而这些信息都是可以每次都存储下来的，因此在收集到了一定的信息之后，参数都可以动态更新，因此我们说LinUCB是一种在线学习方法。





