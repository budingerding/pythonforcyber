from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import os
import pickle

# Read binary files
def read_binary(file_path):
	try:
		with open(file_path, 'rb') as f:
			return f.read()
	except Exception as e:
		print(f"Error reading file {file_path}: {e}")
		return None

# Function to extract n-grams from binary data
def extract_ngrams(data, n=4):
	"""
	Extracts n-grams from binary data.
	Returns a space-seperated string of n-grams.
	"""
	ngrams = [data[i:i+n] for i in range(len(data) - n + 1)]
	ngrams = [''.join(format(byte, '02x') for byte in ngram) for ngram in ngrams]
	return ' '.join(ngrams)



# Prepare dataset
def prepare_dataset_with_ngrams(data_dir, n=4):
	"""
	prepare the dataset by extracting n-grams from binary blobs.
	"""
	X = []
	y = []
	for arch in os.listdir(data_dir):
		arch_dir = os.path.join(data_dir, arch)
		if os.path.isdir(arch_dir):
			for file in os.listdir(arch_dir):
				file_path = os.path.join(arch_dir, file)
				binary_data = read_binary(file_path)
				if binary_data:
					ngram_features = extract_ngrams(binary_data, n)
					X.append(ngram_features)
					y.append(arch)
	return X, y


# Training and saving the model
def train_and_save_model(data_dir, model_path, ngram_size=4):
	# Prepare the dataset
    X_raw, y = prepare_dataset_with_ngrams(data_dir, n=ngram_size)

    # Convert n-grams to a numerical feature matrix
    vectorizer = CountVectorizer(analyzer='word', token_pattern=r'\S+')
    X = vectorizer.fit_transform(X_raw)

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

    # Train the classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the classifier
    y_pred = clf.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save the trained model, vectorizer, and label encoder
    model_data = {
        'classifier': clf,
        'vectorizer': vectorizer,
        'label_encoder': label_encoder
    }
    with open(model_path, "wb") as f:
        pickle.dump(model_data, f)
    print(f"Model saved to {model_path}")

# Main function
if __name__ == "__main__":
	# Path to your binary dataset
	data_dir = "PathToBinaryDataSet"

	# Path to save the trained model
	model_path = "PathTobin_arc_model.pkl"

	# Train the model and save it
	train_and_save_model(data_dir, model_path)
