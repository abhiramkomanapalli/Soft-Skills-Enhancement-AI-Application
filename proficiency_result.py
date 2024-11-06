import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import re

# Step 1: Extract scores from results.html
def extract_scores_from_html(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()

    # Using regex to find scores in the HTML content
    scores = {}
    pattern = r'id="([^"]+Score)">([^<]+)</td>'
    matches = re.findall(pattern, html_content)

    for match in matches:
        section = match[0].replace('Score', '').lower()  # Get the section name
        score = int(match[1])  # Convert score to integer
        scores[section] = score

    return scores

# Step 2: Create a dataset
def create_dataset():
    data = []
    for vocab in range(16):  # Scores from 0 to 15
        for grammar in range(16):
            for aptitude in range(16):
                for technical in range(16):
                    data.append([vocab, grammar, aptitude, technical])

    return pd.DataFrame(data, columns=['Vocabulary', 'Grammar', 'Aptitude', 'Technical'])

# Step 3: Define the model
def train_model(dataset):
    X = dataset[['Vocabulary', 'Grammar', 'Aptitude', 'Technical']]
    y = dataset.apply(lambda row: 'Proficient' if all(score >= 14 for score in row) else
                      ', '.join(sorted([col for col in X.columns if row[col] < 14])), axis=1)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model

# Step 4: Predict using the model
def predict_proficiency(model, scores):
    input_data = np.array([[scores['vocabulary'], scores['grammar'], scores['aptitude'], scores['technical']]])
    prediction = model.predict(input_data)
    return prediction[0]

# Step 5: Write the proficiency result to a text file
def write_proficiency_result(result):
    with open('proficiency_result.txt', 'w') as file:
        file.write(result)

# Main function to run the code
def main():
    # Extract scores from results.html
    scores = extract_scores_from_html('results.html')

    # Create dataset
    dataset = create_dataset()

    # Train the model
    model = train_model(dataset)

    # Predict proficiency
    proficiency = predict_proficiency(model, scores)

    print(f'The proficiency result is: {proficiency}')
    write_proficiency_result(proficiency)  # Write the result to a text file

if __name__ == '__main__':
    main()
