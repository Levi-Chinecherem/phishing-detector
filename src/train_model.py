import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_curve, auc,
    precision_recall_curve, ConfusionMatrixDisplay
)
from data_preprocessing import get_dataset, preprocess

df = get_dataset()
X, y = preprocess(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]  # Probabilities for the positive class (1: legitimate)

# Print evaluation metrics
print(classification_report(y_test, y_pred))

# Create results directory if it doesn't exist
results_dir = 'results/'
os.makedirs(results_dir, exist_ok=True)

# Save metrics to text file
with open(os.path.join(results_dir, 'metrics.txt'), 'w') as f:
    f.write(classification_report(y_test, y_pred))

# Confusion Matrix Plot
disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test, y_pred), display_labels=['Phishing', 'Legitimate'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig(os.path.join(results_dir, 'confusion_matrix.png'))
plt.close()

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob, pos_label=1)
roc_auc = auc(fpr, tpr)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc='lower right')
plt.savefig(os.path.join(results_dir, 'roc_curve.png'))
plt.close()

# Precision-Recall Curve
precision, recall, _ = precision_recall_curve(y_test, y_prob, pos_label=1)
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

# Save the model
with open('models/random_forest_model.pkl', 'wb') as f:
    pickle.dump(model, f)