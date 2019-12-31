import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

y1=[5, 17, 17, 17, 19, 19, 19, 20, 12, 19, 19] 
y2=[5, 6, 15, 16, 5, 11, 13, 17, 12, 9, 3]
y3=[6, 7, 20, 20, 20, 18, 20, 19, 20, 20, 20]

date_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
date_labels = ['11-05', '11-06', '11-07', '11-08', '11-09', '11-10', '11-11', '11-12', '11-13', '11-14', '11-15']

rank_values = [0, 5, 10, 15, 20]
rank_labels = ['0', '5', '10', '15', '20']

plt.title('abtest id 2 10 vs 5')
plt.xlabel('date')
plt.ylabel('rank')
 
plt.plot(date_values, y1, 'b', label='abtest_id:2')
plt.plot(date_values, y2, 'r',label='abtest_id:5')
plt.plot(date_values, y3, 'g', label='abtest_id:10')

plt.xticks(date_values, date_labels)
#plt.yticks(rank_values, rank_labels)

for a, b in zip(date_values, y1):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
for a, b in zip(date_values, y2):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
for a, b in zip(date_values, y3):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=8)


plt.legend(bbox_to_anchor=[0.5, 0.25]) 
plt.grid()
plt.show()
plt.savefig('rank.jpg')
