import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
%matplotlib inline
# Read the bank data
data = pd.read_csv("bank-full.csv", delimiter=";")
data.head()
# Drop unrelated subjects
data.drop(['contact','day','month','duration','poutcome', "previous", "pdays"], inplace=True, axis=1)
# Encode labels
encoder = LabelEncoder()

data['marital'] = encoder.fit_transform(data['marital'])
data['job'] = encoder.fit_transform(data['job'])
data['education'] = encoder.fit_transform(data['education'])
data['default'] = encoder.fit_transform(data['default'])
data['housing'] = encoder.fit_transform(data['housing'])
data['loan'] = encoder.fit_transform(data['loan'])
data['y'] = encoder.fit_transform(data['y'])

# Create correlation
correlation = data.corr(method='pearson')
plt.figure(figsize=(25,10))
sns.heatmap(correlation, vmax=1, square=True,  annot=True ) 
plt.show()

# Split the data using K-fold
X = data.drop('y',axis = 1).values
y = data['y'].values
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Graph k-means with different k-values (elbow method)
wcss = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, init="k-means++")
    kmeans.fit(data.iloc[:,1:])
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(12,6))    
plt.grid()
plt.plot(range(1,11),wcss, linewidth=2, color="red", marker ="8")
plt.xlabel("K Value")
plt.xticks(np.arange(1,11,1))
plt.ylabel("WCSS")
plt.show()
# Creating scatter plot with k = 4 (k value from elbow method)
km=KMeans(n_clusters=4)

Age = data['age'].values
Balance = data['balance'].values
Xe = np.array(list(zip(Age, Balance)))

y_means = km.fit_predict(X)

plt.scatter(Xe[y_means==0,0],Xe[y_means==0,1],s=10, c='purple',label='Cluster1')
plt.scatter(Xe[y_means==1,0],Xe[y_means==1,1],s=10, c='blue',label='Cluster2')
plt.scatter(Xe[y_means==2,0],Xe[y_means==2,1],s=10, c='green',label='Cluster3')
plt.scatter(Xe[y_means==3,0],Xe[y_means==3,1],s=10, c='cyan',label='Cluster4')

plt.title('Customer segmentation')
plt.xlabel('Balance')
plt.ylabel('Age of customer')
plt.legend()
plt.show()

# Fit K-Means model
predictions = km.fit_predict(X_test)

# Create confusion matrix and generate accuracy report
print("Accuracy : ", accuracy_score(Y_test, predictions))
print("Confusion Matrix : \n",confusion_matrix(Y_test, predictions))
print("Classification Report: \n",classification_report(Y_test, predictions))
