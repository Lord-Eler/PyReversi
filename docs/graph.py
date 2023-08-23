import pickle
import matplotlib.pyplot as plt
from random import randint
with open('docs/best_graph/results3.pickle','rb') as f:
    results_list = pickle.load(f)
with open('docs/best_graph/total3.pickle','rb') as f:
    total = pickle.load(f)




inf,sup = 5,20
results = {k:0 for k in range(inf,sup)}
for a in range(inf,sup):
    for b in range(inf,sup):
        if results_list[(a-inf)*(sup-inf)+b-inf] == -2:
            continue
        results[a] += results_list[(a-inf)*(sup-inf)+b-inf]
        results[b] += total[(a-inf)*(sup-inf)+b-inf] - results_list[(a-inf)*(sup-inf)+b-inf]
        

        

print(results)
X = []
Y = []
for key in results.keys():
    X.append(key/10)
    Y.append(results[key]/560)

plt.plot(X,Y)
plt.xlabel('Exploration Factor')
plt.ylabel('Win Rate')
plt.title('Win Rate depending on Exploration Factor')
plt.show()

sum = 0
for key in results.keys():
    sum += results[key]
print(sum)