import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv("./RandomForestModel/ksi_collisions.csv")

categorical_features = [
    'LIGHT', 'VISIBILITY', 'ROAD_CONDITION', 'DOW', 'TIME_OF_DAY',
    'SEASON', 'VEHICLE_TYPE', 'DRIVER_ACTION', 'IMPACT_TYPE',
    'NEIGHBOURHOOD', 'AGE_RANGE'
]
target = 'SEVERE_COLLISION'

X = df[categorical_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore',
         sparse_output=False), categorical_features)
    ],
    remainder='drop'
)

pipe = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

params = {
    'classifier__n_estimators': list(range(80, 90, 5)),
    'classifier__max_depth': list(range(24, 26, 2)),
    'classifier__min_samples_split': [2],
    'classifier__min_samples_leaf': [1],
    'classifier__max_features': ['sqrt']
}

grid = GridSearchCV(pipe, params, cv=5, scoring='f1', n_jobs=-1, verbose=2)
grid.fit(X_train, y_train)

print("Best Params:", grid.best_params_)
print("Best F1 Score:", grid.best_score_)
