# 算法原理
## CBOW 和 Skip-Gram 模型
1. CBOW是上下文预测中间词
2. Skip-gram是中间词预测上下文
- Q：w2v和dnn的区别是什么？
dnn训练太慢了，w2v做了优化
## 使用霍夫曼树代替隐藏层和输出层神经元
叶子结点是输出层，叶子结点个数为词汇表大小，内部节点起到隐藏层作用
霍夫曼树中权值高的叶子结点越靠近根节点。权值高的节点编码值短，权值低的节点编码值长，由此树的带权路径最短，符合信息论。
不一样的是w2v中左子树编码1右子树编码0，左边权重不小于右边
左子树走是负类，霍夫曼编码1.判别正负的方法是使用sigmod函数
复杂度降低，符合贪心思想
- Q：缺点？
如果遇到一个非常生僻的词，会在霍夫曼树下走很久。过于复杂
## negative sampling-负采样
对于某个词w，可以采样content(w)个词，我们现在采样和w不同的neg个词，则neg个词都是content(w)的负例。进行二元逻辑回归，得到负采样对应的每个词对应的模型参数和词向量。
不需要霍夫曼树就可以训练模型，还比较简单。

# 训练word2vec
## 中文切词
与处理英文不同，中文没有切词，需要使用jieba进行切词处理。
## 模型训练
库函数：pip install gensim
	def train_word2vec(filename):
	    #模型文件不存在才处理
	    if not os.path.exists(word2vec_file):
	        sentences = LineSentence(filename)
	        #sg=0 使用cbow训练, sg=1对低频词较为敏感
	        model = Word2Vec(sentences,
	                         size=n_dim, window=5, min_count=2, sg=1, workers=2)
	        model.save(word2vec_file)
## 测试效果
model.most_similar(u'微信')
model.most_similar(positive=[u'足球'+u'明星'])
model.most_similar(positive=[u'球星'],negative=[u'明星'])
model.wv.similarity(u'微信', u'陌陌')