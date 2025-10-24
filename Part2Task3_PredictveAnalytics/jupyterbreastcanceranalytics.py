# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.datasets import load_breast_cancer
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# Data Exploration
print("Dataset Info:")
print(df.info())
print("\nTarget Distribution:")
print(df['target'].value_counts())
print("\nMissing Values:")
print(df.isnull().sum())

# Create priority levels based on tumor characteristics for resource allocation
# High priority: malignant tumors with aggressive features
# Medium priority: borderline cases
# Low priority: benign tumors

def create_priority_level(row):
    """Create priority levels based on tumor characteristics"""
    # Using mean radius and worst concavity as indicators of severity
    if row['target'] == 1:  # Malignant
        if row['mean radius'] > 15 or row['worst concavity'] > 0.3:
            return 'high'
        else:
            return 'medium'
    else:  # Benign
        return 'low'

# Apply priority labeling
df['priority'] = df.apply(create_priority_level, axis=1)

print("Priority Level Distribution:")
print(df['priority'].value_counts())

# Data Preprocessing
# Prepare features and target
X = df.drop(['target', 'priority'], axis=1)
y = df['priority']

# Encode the target variable
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print("Feature names:", X.columns.tolist())
print("Target classes:", le.classes_)
print("Encoded targets:", np.unique(y_encoded))


# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
)

print(f"Training set size: {X_train.shape}")
print(f"Testing set size: {X_test.shape}")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest Model
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=10,
    min_samples_split=5,
    class_weight='balanced'
)

# Train the model
rf_model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = rf_model.predict(X_test_scaled)
y_pred_proba = rf_model.predict_proba(X_test_scaled)

# Model Evaluation
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')

print("=== MODEL PERFORMANCE METRICS ===")
print(f"Accuracy: {accuracy:.4f}")
print(f"F1-Score (Weighted): {f1:.4f}")
print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Confusion Matrix
plt.figure(figsize=(10, 8))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.title('Confusion Matrix - Priority Prediction')
plt.xlabel('Predicted Priority')
plt.ylabel('Actual Priority')
plt.show()

# Feature Importance Analysis
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(data=feature_importance.head(15), x='importance', y='feature')
plt.title('Top 15 Most Important Features for Priority Prediction')
plt.xlabel('Feature Importance')
plt.tight_layout()
plt.show()

print("Top 10 Most Important Features:")
print(feature_importance.head(10))

# Model Performance Summary
print("=== PREDICTIVE ANALYTICS FOR RESOURCE ALLOCATION ===")
print("Dataset: Breast Cancer Wisconsin")
print("Model: Random Forest Classifier")
print("\nPERFORMANCE SUMMARY:")
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"F1-Score: {f1:.4f}")

# Calculate class-wise performance
class_report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)
print(f"\nCLASS-WISE PERFORMANCE:")
for class_name in le.classes_:
    precision = class_report[class_name]['precision']
    recall = class_report[class_name]['recall']
    f1_class = class_report[class_name]['f1-score']
    print(f"{class_name.upper()} Priority - Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1_class:.3f}")

print(f"\nRESOURCE ALLOCATION INSIGHTS:")
priority_counts = pd.Series(y_pred).value_counts()
for i, count in priority_counts.items():
    print(f"{le.classes_[i].upper()} Priority cases: {count} ({count/len(y_pred)*100:.1f}%)")

    