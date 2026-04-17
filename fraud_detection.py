import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("transactions.csv")

df = df.fillna(0)

# Defines the festures and the labels
X = df[['amount', 'time']]   
y = df['is_fraud']           

# dataset split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#training the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

#evaluating the model
y_pred = model.predict(X_test)
print("Fraud Detection Report:")
print(classification_report(y_test, y_pred))

#example prediction
new_transaction = pd.DataFrame([[5000, 12]], columns=['amount', 'time'])
prediction = model.predict(new_transaction)
print("Prediction for new transaction:", prediction[0])
