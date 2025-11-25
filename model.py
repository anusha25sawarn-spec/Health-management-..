# model.py

def predict_health_risk(data):
    """
    Simulated function to predict health risk (e.g., Diabetes Risk).
    In a real app, this would load a trained Keras/Scikit-learn model.
    Data is expected as a list/array of numerical features:
    [Age, BMI, Glucose, BloodPressure, Insulin]
    """
    
    # Simple risk calculation for demonstration:
    # High risk if Glucose > 140 OR (BMI > 30 AND Age > 40)
    
    age, bmi, glucose, bp, insulin = data
    
    if glucose > 140:
        return 1, "High Blood Sugar detected. **Consult a physician immediately.**"
    elif bmi > 30 and age > 40:
        return 1, "Elevated risk based on BMI and Age. Focus on lifestyle changes."
    else:
        return 0, "Low risk detected. Keep up the good work!"