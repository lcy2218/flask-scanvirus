import pandas as pd
import numpy as np
import pickle
import sklearn.ensemble as ske
from sklearn import model_selection
from sklearn import tree, linear_model
from sklearn.feature_selection import SelectFromModel
import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix

data = pd.read_csv('data.csv', sep='|', low_memory=False, skiprows=0)
X = data.drop(['Name', 'md5', 'legitimate'], axis=1).values
y = data['legitimate'].values
print('一共有%i个重要特征\n' % X.shape[1])

# Feature selection using Trees Classifier
print('正在处理数据...')
fsel = ske.ExtraTreesClassifier().fit(X, y)
model = SelectFromModel(fsel, prefit=True)
X_new = model.transform(X)
nb_features = X_new.shape[1]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X_new, y ,test_size=0.2)

features = []

print('%i个重要字段:' % nb_features)

indices = np.argsort(fsel.feature_importances_)[::-1][:nb_features]
for f in range(nb_features):
    print("%d. 字段 %s (%f)" % (f + 1, data.columns[2+indices[f]], fsel.feature_importances_[indices[f]]))

# XXX : take care of the feature order
for f in sorted(np.argsort(fsel.feature_importances_)[::-1][:nb_features]):
    features.append(data.columns[2+f])

#Algorithm comparison
algorithms = {
        "DecisionTree": tree.DecisionTreeClassifier(max_depth=10),
        "RandomForest": ske.RandomForestClassifier(n_estimators=50),
        "GradientBoosting": ske.GradientBoostingClassifier(n_estimators=50),
        "AdaBoost": ske.AdaBoostClassifier(n_estimators=100),
        "GNB": GaussianNB()
    }

results = {}
print("\n正在测试算法......")
for algo in algorithms:
    clf = algorithms[algo]
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print("%s : %f %%" % (algo, score*100))
    results[algo] = score

winner = max(results, key=results.get)
print('\n最终算法为 %s 正确率为 %f %% ' % (winner, results[winner]*100))

# Save the algorithm and the feature list for later predictions
print('正在classifier目录中保存算法和特征列表...')
joblib.dump(algorithms[winner], 'classifier/classifier.pkl')
open('classifier/features.pkl', 'wb').write(pickle.dumps(features))
print('Saved')

# Identify false and true positive rates
clf = algorithms[winner]
res = clf.predict(X_test)
mt = confusion_matrix(y_test, res)
print("假阳性率为 : %f %%" % ((mt[0][1] / float(sum(mt[0])))*100))
print('假阴性率为 : %f %%' % ( (mt[1][0] / float(sum(mt[1]))*100)))
