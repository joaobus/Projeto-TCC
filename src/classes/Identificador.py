from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def Identificador(Fa0V,y):

    # Assume Fa0V is your vector and y is the target variable with disturb type and intensity
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(Fa0V, y, test_size=0.4)

    # Create a Random Forest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=0)

    # Train the classifier
    clf.fit(X_train, y_train)

    # Predict the test set results
    y_pred = clf.predict(X_test)

    print(y_pred)
    


     #Calculate the accuracy score
    #accuracy = accuracy_score(y_test_int, y_pred_int)

    # Print the accuracy score
    #print("Accuracy:", accuracy)

    # To compare the predicted values with the real values, you can use the following code
    for i in range(len(y_test)):
        print("Real value:", y_test[i], "Predicted value:", y_pred[i])
