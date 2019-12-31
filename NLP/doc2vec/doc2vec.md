# 如何将句子做嵌入
## bag of words
词袋模型，未考虑到单词顺序，未考虑单词的语义信息
## average word vectors
词向量取平均，未考虑单词顺序
## tfidf-weighting word vector
词向量根据tfidf加权，也未考虑单词顺序
## lda
文档或句子的主题分布

# doc2vec
每次从一句话中滑动采样固定长度的词，取其中一个词作预测词，其他的作输入词。输入词对应的词向量word vector和本句话对应的句子向量Paragraph vector作为输入层的输入，将本句话的向量和本次采样的词向量相加求平均或者累加构成一个新的向量X，进而使用这个向量X预测此次窗口内的预测词。（预测句子中的下一个单词）

Doc2vec相对于word2vec不同之处在于，在输入层，增添了一个新句子向量Paragraph vector，Paragraph vector可以被看作是另一个词向量，它扮演了一个记忆

每次训练也是滑动截取句子中一小部分词来训练，Paragraph Vector在同一个句子的若干次训练中是共享的，所以同一句话会有多次训练，每次训练中输入都包含Paragraph vector。

它可以被看作是句子的主旨，有了它，该句子的主旨每次都会被放入作为输入的一部分来训练。这样每次训练过程中，不光是训练了词，得到了词向量。同时随着一句话每次滑动取若干词训练的过程中，作为每次训练的输入层一部分的共享Paragraph vector，该向量表达的主旨会越来越准确
## PV-DM
根据每个单词的上下文，预测下一个词
## PV-DBOW
忽略输入的上下文，让模型去预测段落中的随机一个单词