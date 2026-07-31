# ML Artifacts

This folder stores generated machine learning assets after training.

Expected files:

- `phishing_model.keras`: trained TensorFlow/Keras model
- `scaler.pkl`: fitted feature scaler
- `feature_columns.json`: ordered feature list used during training
- `model_metrics.json`: evaluation metrics from the latest trained model
- `shap_background.pkl`: representative sample used by SHAP explainability

Generated binary artifacts should usually be ignored by Git unless the project
requires a small demo model to be versioned.

