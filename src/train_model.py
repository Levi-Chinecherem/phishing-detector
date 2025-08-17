import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_curve, auc,
    precision_recall_curve, ConfusionMatrixDisplay, roc_auc_score
)
from data_preprocessing import get_dataset, preprocess
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load and preprocess dataset
df = get_dataset()
X, y = preprocess(df)

# Convert labels to 0 (phishing) and 1 (legitimate) for XGBoost
y = (y + 1) // 2  # Maps -1 to 0, 1 to 1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Log feature distribution
logger.debug("Feature distribution in training data:")
for col in X.columns:
    logger.debug(f"{col}: {X[col].value_counts().to_dict()}")

# Train XGBoost model with class weighting
scale_pos_weight = sum(y == 0) / sum(y == 1)  # Weight phishing class higher
model = XGBClassifier(
    random_state=42,
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    scale_pos_weight=scale_pos_weight
)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Print and save metrics
report = classification_report(y_test, y_pred, target_names=['Phishing', 'Legitimate'])
logger.debug(f"Classification Report:\n{report}")
results_dir = 'results/'
os.makedirs(results_dir, exist_ok=True)
with open(os.path.join(results_dir, 'metrics.txt'), 'w') as f:
    f.write(report)

# Confusion Matrix
disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test, y_pred), display_labels=['Phishing', 'Legitimate'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig(os.path.join(results_dir, 'confusion_matrix.png'))
plt.close()

# ROC Curve with Optimal Threshold
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]
logger.debug(f"Optimal ROC threshold: {optimal_threshold:.3f}")
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.scatter(fpr[optimal_idx], tpr[optimal_idx], marker='o', color='red', label=f'Optimal threshold ({optimal_threshold:.3f})')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc='lower right')
plt.savefig(os.path.join(results_dir, 'roc_curve.png'))
plt.close()

# Precision-Recall Curve
precision, recall, _ = precision_recall_curve(y_test, y_prob)
plt.figure()
plt.plot(recall, precision, color='blue', lw=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.savefig(os.path.join(results_dir, 'precision_recall_curve.png'))
plt.close()

# Feature Importances
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
features = X.columns
plt.figure(figsize=(10, 6))
plt.title('Feature Importances')
plt.bar(range(X.shape[1]), importances[indices], align='center')
plt.xticks(range(X.shape[1]), [features[i] for i in indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.savefig(os.path.join(results_dir, 'feature_importances.png'))
plt.close()

# Save sample test predictions
sample_test = X_test[:10].copy()
sample_pred = model.predict(sample_test)
sample_proba = model.predict_proba(sample_test)[:, 1]
sample_df = pd.DataFrame(sample_test, columns=X.columns)
sample_df['Prediction'] = ['Legitimate' if p == 1 else 'Phishing' for p in sample_pred]
sample_df['Confidence'] = sample_proba
sample_df.to_csv(os.path.join(results_dir, 'sample_predictions.csv'), index=False)
logger.debug(f"Sample predictions saved to {results_dir}sample_predictions.csv")

# Save the model
with open('models/random_forest_model.pkl', 'wb') as f:
    pickle.dump(model, f)