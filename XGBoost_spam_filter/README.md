# XGBoost Spam Filter

A project utilising the XGBoost algorithm to create a spam filter focusing on minimizing false negatives for a cybersecurity use-case.

## 1. Objective

- **Aim:** Develop a spam filter with strong cybersecurity attributes.
- **Emphasis:** Minimise False Negatives over False Positives due to their larger cybersecurity implications.

## 2. Dataset

- Contains 5,693 labelled emails.
- Unbalanced: Positive class (spam) is the minority at 1/3.
- Raw text format, requiring feature extraction.

## 3. Feature Selection

- Used CountVectorizer's bag of words to create a sparse matrix.
- Emails converted to a consistent feature vector length, suitable for tree-based algorithms.
- Punctuations and the word 'Subject' removed; accented characters retained.
- Started with 37,000 features, reduced to the top 500 based on frequency.

## 4. Algorithm Selection, Training, and Evaluation

**Why XGBoost?**
- Allows for a weighted loss function.
- Tree-based, so no feature scaling required.
- Handles collinearity.
- Efficient for sparse datasets.
- L1 regularization can be implemented for outlier handling.
- Performs swiftly, albeit slower than LightGBM.

**Performance metrics:**

| Metric               | Training | Testing |
|----------------------|----------|---------|
| Accuracy             | 0.99     | 0.98    |
| Precision            | 0.97     | 0.92    |
| Recall               | 1.00     | 0.99    |
| ROC AUC              | 1.00     | 1.00    |
| False Positive Rate  | -        | 0.03    |
| False Negative Rate  | -        | 0.01    |
| Specificity          | -        | 0.96    |
| Sensitivity          | -        | 0.99    |

## 5. Conclusion

The current model effectively categorises spam with a 99% accuracy. However, it is slightly overcautious, leading to 3-4% of legitimate emails being mistakenly classified as spam.

## 6. Future Improvements

- Feature selection could be enhanced due to observed high feature correlation.
- Automated hyperparameter tuning (e.g., through GridSearchCV) to optimise results.
