import torch
import pandas
from train_model import Model
import joblib
from sklearn.metrics import classification_report, confusion_matrix


df = pandas.read_csv("emails.csv")

model = Model()
dataset = joblib.load("./output/data.pkl")
vectorizer = joblib.load("./output/vectorizer.pkl")

X_test_array = dataset["X_test"].toarray()
X_test = torch.FloatTensor(X_test_array)
y_test = torch.FloatTensor(dataset["y_test"].values.copy()).view(-1, 1)

model.load_state_dict(torch.load("output/model.pth"))
model.eval()

with torch.no_grad():
    raw_predictions = model(X_test)
    y_pred = (raw_predictions > 0.5).int()

y_test_np = y_test.numpy().flatten()
y_pred_np = y_pred.numpy().flatten()

print(classification_report(y_test, y_pred_np))
print(confusion_matrix(y_test, y_pred_np))

test_index = dataset["y_test"].index
mask_fn = (y_test_np == 1) & (y_pred_np == 0)
spam_errors = df.loc[test_index[mask_fn]]

mask_fp = (y_test_np == 0) & (y_pred_np == 1)
lost_mails = df.loc[test_index[mask_fp]]

print("\n --- EXAMPLES OF UNDETECTED SPAM ---")
print(spam_errors.head())

print("\n --- LOST MAILS ---")
print(lost_mails)

report = classification_report(y_test_np, y_pred_np)
with open("output/evaluation_report.txt", "w") as f:
    f.write("--- EVALUATION REPORT ---\n")
    f.write(report)
    f.write("\n--- CONFUSION MATRIX ---\n")
    f.write(str(confusion_matrix(y_test_np, y_pred_np)))

print("✅ Results saved in 'output/evaluation_report.txt'")