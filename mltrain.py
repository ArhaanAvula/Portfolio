import pandas as pd
import re
from urllib.parse import urlparse
import lightgbm as lgb
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import json

def extract_features(df):
    suspicious_words = ['login', 'secure', 'account', 'update', 'free', 'verify', 'webscr']
    suspicious_tlds = ['.xyz', '.top', '.club', '.online', '.info', '.biz']

    def has_ip(url):
        try:
            host = urlparse(url).netloc
            return 1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', host) else 0
        except:
            return 0

    def has_https(url):
        try:
            return 1 if urlparse(url).scheme == 'https' else 0
        except:
            return 0

    def count_at_symbol(url):
        return url.count('@')

    def count_question_mark(url):
        return url.count('?')

    def count_percent_sign(url):
        return url.count('%')

    def count_slashes(url):
        try:
            path = urlparse(url).path
            return path.count('/')
        except:
            return 0

    def count_equal_sign(url):
        return url.count('=')

    def count_suspicious_words(url):
        url_lower = url.lower()
        return sum(word in url_lower for word in suspicious_words)

    def domain_length(url):
        try:
            domain = urlparse(url).netloc
            return len(domain)
        except:
            return 0

    def count_subdomains(url):
        try:
            domain = urlparse(url).netloc
            parts = domain.split('.')
            return max(len(parts) - 2, 0)
        except:
            return 0

    def hyphen_in_domain(url):
        try:
            domain = urlparse(url).netloc
            return 1 if '-' in domain else 0
        except:
            return 0

    def url_length(url):
        return len(url)

    def count_digits(url):
        return sum(c.isdigit() for c in url)

    def count_letters(url):
        return sum(c.isalpha() for c in url)

    def count_special_chars(url):
        return sum(url.count(c) for c in ['#', '&', '~', '$', '!', '*'])

    def ends_with_slash(url):
        return 1 if url.endswith('/') else 0

    def at_in_path(url):
        try:
            path = urlparse(url).path
            return 1 if '@' in path else 0
        except:
            return 0

    def subdirectory_depth(url):
        try:
            path = urlparse(url).path
            # count how many '/' beyond the first
            return len([p for p in path.split('/') if p]) - 1 if len(path.split('/')) > 1 else 0
        except:
            return 0

    def digit_ratio(url):
        length = len(url)
        digits = count_digits(url)
        return digits / length if length > 0 else 0

    def suspicious_tld(url):
        try:
            domain = urlparse(url).netloc.lower()
            return 1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0
        except:
            return 0

    df['has_ip'] = df['url'].apply(has_ip)
    df['has_https'] = df['url'].apply(has_https)
    df['count_at'] = df['url'].apply(count_at_symbol)
    df['count_question'] = df['url'].apply(count_question_mark)
    df['count_percent'] = df['url'].apply(count_percent_sign)
    df['count_slashes'] = df['url'].apply(count_slashes)
    df['count_equal'] = df['url'].apply(count_equal_sign)
    df['count_suspicious_words'] = df['url'].apply(count_suspicious_words)
    df['domain_length'] = df['url'].apply(domain_length)
    df['count_subdomains'] = df['url'].apply(count_subdomains)
    df['hyphen_in_domain'] = df['url'].apply(hyphen_in_domain)
    df['url_length'] = df['url'].apply(url_length)
    df['count_digits'] = df['url'].apply(count_digits)
    df['count_letters'] = df['url'].apply(count_letters)
    df['count_special_chars'] = df['url'].apply(count_special_chars)
    df['ends_with_slash'] = df['url'].apply(ends_with_slash)
    df['at_in_path'] = df['url'].apply(at_in_path)
    df['subdirectory_depth'] = df['url'].apply(subdirectory_depth)
    df['digit_ratio'] = df['url'].apply(digit_ratio)
    df['suspicious_tld'] = df['url'].apply(suspicious_tld)

    feature_cols = ['has_ip', 'has_https', 'count_at', 'count_question', 'count_percent',
                    'count_slashes', 'count_equal', 'count_suspicious_words',
                    'domain_length', 'count_subdomains', 'hyphen_in_domain',
                    'url_length', 'count_digits', 'count_letters', 'count_special_chars',
                    'ends_with_slash', 'at_in_path', 'subdirectory_depth', 'digit_ratio',
                    'suspicious_tld']

    return df[feature_cols]

def main():
    print("Loading data...")
    df = pd.read_csv('malicious_phish.csv')
    df['label'] = df['type'].apply(lambda x: 1 if x == 'phishing' else 0)

    print("Extracting features...")
    X = extract_features(df)
    y = df['label']

    print("Splitting into train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    print("Preparing LightGBM dataset...")
    train_data = lgb.Dataset(X_train, label=y_train)

    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'seed': 42
    }

    print("Training model on training data...")
    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
    )

    print("Evaluating on test data...")
    y_pred_proba = model.predict(X_test)

    # Calculate precision, recall, f1 for multiple thresholds
    thresholds = np.arange(0.0, 1.01, 0.01)
    f1_scores = []
    precisions = []
    recalls = []

    for thresh in thresholds:
        y_pred = (y_pred_proba > thresh).astype(int)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
        f1_scores.append(f1)
        precisions.append(precision)
        recalls.append(recall)

    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx]

    print(f"Best threshold by F1 score: {best_threshold:.4f}")

    # Final evaluation using best threshold
    y_pred = (y_pred_proba > best_threshold).astype(int)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    TP = cm[1, 1]
    FN = cm[1, 0]
    FP = cm[0, 1]
    TN = cm[0, 0]

    TPR = TP / (TP + FN) if (TP + FN) > 0 else 0
    FPR = FP / (FP + TN) if (FP + TN) > 0 else 0
    PPV = TP / (TP + FP) if (TP + FP) > 0 else 0

    print(f"Accuracy: {acc:.4f}")
    print(f"True Positive Rate (Recall): {TPR:.4f}")
    print(f"False Positive Rate: {FPR:.4f}")
    print(f"Positive Predictive Value (Precision): {PPV:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print(f"True Negatives: {TN}, False Positives: {FP}")
    print(f"False Negatives: {FN}, True Positives: {TP}")

    # Save model and threshold
    model.save_model('lightgbm_model_advanced.txt')
    with open('best_threshold.json', 'w') as f:
        json.dump({'threshold': best_threshold}, f)

    print("Model saved as 'lightgbm_model_advanced.txt'")
    print("Best threshold saved as 'best_threshold.json'")

    # Plot precision, recall, f1 vs threshold
    plt.figure(figsize=(10,6))
    plt.plot(thresholds, precisions, label='Precision')
    plt.plot(thresholds, recalls, label='Recall')
    plt.plot(thresholds, f1_scores, label='F1 Score')
    plt.axvline(x=best_threshold, color='r', linestyle='--', label=f'Best Threshold ({best_threshold:.2f})')
    plt.xlabel('Threshold')
    plt.ylabel('Score')
    plt.title('Precision, Recall, and F1 Score vs Threshold')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()