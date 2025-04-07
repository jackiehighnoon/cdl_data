# loads matchup_features.csv, splits, trains RF, saves model.pkl
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Assign the path to the CSV file
X = pd.read_csv("processed/single_matchups/matchup_features.csv")
X = X.select_dtypes(include=[int, float])
y = pd.read_csv("processed/single_matchups/labels.csv").squeeze("columns")

#Split data into features and labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the objective function for Optuna
def objective(trial):
    # Suggest hyperparameters for the RandomForestClassifier
    n_estimators = trial.suggest_int("n_estimators", 50, 300)
    max_features = trial.suggest_categorical("max_features", ["sqrt", "log2", None])
    min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 10)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
    bootstrap = trial.suggest_categorical("bootstrap", [True, False])
    
    # Create the model with the suggested hyperparameters
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_features=max_features,
        min_samples_leaf=min_samples_leaf,
        min_samples_split=min_samples_split,
        random_state=42,
        bootstrap=bootstrap
    )

    # Use cross-validation to evaluate model performance (accuracy in this case)
    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    return scores.mean()

# Create a study object with the goal of maximizing accuracy
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)

print("Best hyperparameters: ", study.best_params)
print("Best accuracy: ", study.best_value)

rf_model = RandomForestClassifier(**study.best_params)
rf_model.fit(X_train, y_train)

joblib.dump(rf_model, "model.pkl")
print("Model saved to model.pkl")

""" # metrics specific to classification
accuracy_score(y_test, y_pred)
classification_report(y_test, y_pred)
confusion_matrix(y_test, y_pred)

print("accuracy_score: ", accuracy_score(y_test, y_pred))
print("classification_report: ", classification_report(y_test, y_pred))
print("confusion_matrix: ", confusion_matrix(y_test, y_pred)) """