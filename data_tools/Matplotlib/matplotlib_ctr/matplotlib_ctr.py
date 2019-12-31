import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

y1=[0.0098, 0.0101, 0.0103, 0.0107, 0.0102, 0.0102, 0.009, 0.0096, 0.0093, 0.01, 0.0095] 
y2=[0.0098, 0.0098, 0.0101, 0.0106, 0.0093, 0.0094, 0.0084, 0.0089, 0.0093, 0.0091, 0.0084]
y3=[0.0099, 0.0099, 0.0104, 0.0111, 0.0102, 0.0099, 0.0092, 0.0095, 0.0099, 0.0101, 0.01]

date_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
date_labels = ['11-05', '11-06', '11-07', '11-08', '11-09', '11-10', '11-11', '11-12', '11-13', '11-14', '11-15']

ctr_values = [0, 0.0075, 0.01, 0.0125, 0.015]
ctr_labels = ['0', '0.0075', '0.01', '0.0125', '0.015']

plt.title('abtest id 2 10 vs 5')
plt.xlabel('date')
plt.ylabel('ctr')
 
plt.plot(date_values, y1, 'b', label='abtest_id:2')
plt.plot(date_values, y2, 'r',label='abtest_id:5')
plt.plot(date_values, y3, 'g', label='abtest_id:10')

plt.xticks(date_values, date_labels)
#plt.yticks(ctr_values, ctr_labels)

for a, b in zip(date_values, y1):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
for a, b in zip(date_values, y2):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
for a, b in zip(date_values, y3):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=8)


plt.legend(bbox_to_anchor=[0.7, 0.75]) 
plt.grid()
plt.show()
plt.savefig('ctr.jpg')
