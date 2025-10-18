import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from wordcloud import WordCloud
import pandas as pd

def train_model(data_file, model_file):
    # Load preprocessed data
    with open(data_file, "rb") as f:
        X, y, vectorizer = pickle.load(f)

    # Load original data for word clouds
    original_data = pd.read_csv("data/phishing_emails.csv")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define models and parameters for grid search
    models = {
        'RandomForest': (RandomForestClassifier(random_state=42), {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20]
        }),
        'LogisticRegression': (LogisticRegression(random_state=42, max_iter=1000), {
            'C': [0.1, 1, 10]
        }),
        'SVM': (SVC(random_state=42, probability=True), {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf']
        })
    }

    best_model = None
    best_score = 0
    best_name = ''
    trained_models = {}

    for name, (model, params) in models.items():
        grid = GridSearchCV(model, params, cv=5, scoring='f1')
        grid.fit(X_train, y_train)
        score = grid.best_score_
        print(f"{name} Best CV F1: {score:.2f} with params: {grid.best_params_}")

        trained_models[name] = grid.best_estimator_

        if score > best_score:
            best_score = score
            best_model = grid.best_estimator_
            best_name = name

    # Train the best model on full training data
    best_model.fit(X_train, y_train)

    # Evaluate the best model
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"Best Model: {best_name}")
    print(f"Test Accuracy: {accuracy:.2f}")
    print(f"Test Precision: {precision:.2f}")
    print(f"Test Recall: {recall:.2f}")
    print(f"Test F1 Score: {f1:.2f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Phishing', 'Phishing'], yticklabels=['Not Phishing', 'Phishing'])
    plt.title('Confusion Matrix')
    plt.savefig('models/confusion_matrix.png')
    plt.close()

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, best_model.predict_proba(X_test)[:, 1])
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(6,4))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.savefig('models/roc_curve.png')
    plt.close()

    # Word Clouds
    phishing_texts = original_data[original_data['label'] == 1]['text'].str.cat(sep=' ')
    non_phishing_texts = original_data[original_data['label'] == 0]['text'].str.cat(sep=' ')

    wordcloud_phishing = WordCloud(width=800, height=400, background_color='white').generate(phishing_texts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_phishing, interpolation='bilinear')
    plt.axis('off')
    plt.title('Phishing Emails Word Cloud')
    plt.savefig('models/wordcloud_phishing.png')
    plt.close()

    wordcloud_non_phishing = WordCloud(width=800, height=400, background_color='white').generate(non_phishing_texts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_non_phishing, interpolation='bilinear')
    plt.axis('off')
    plt.title('Non-Phishing Emails Word Cloud')
    plt.savefig('models/wordcloud_non_phishing.png')
    plt.close()

    # Save all trained models
    for name, model in trained_models.items():
        joblib.dump(model, f'models/{name.lower()}_model.pkl')

    # Save the best model
    joblib.dump(best_model, model_file)

    # Save metrics
    metrics = {
        'model_name': best_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc
    }
    with open('models/metrics.pkl', 'wb') as f:
        pickle.dump(metrics, f)

    print(f"Best model ({best_name}) saved to {model_file}")
    print("All models and visualizations saved to models/ folder")
    print("Metrics saved to models/metrics.pkl")

if __name__ == "__main__":
    train_model("data/preprocessed_data.pkl", "models/phishing_detector.pkl")
