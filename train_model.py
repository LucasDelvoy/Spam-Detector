from torch import nn, optim, FloatTensor, save
import joblib

dataset = joblib.load("./output/data.pkl")
vectorizer = joblib.load("./output/vectorizer.pkl")


input_size = dataset["X_train"].shape[1]

X_train_array = dataset["X_train"].toarray()
X_test_array = dataset["X_test"].toarray()

X_train = FloatTensor(X_train_array)
X_test = FloatTensor(X_test_array)
y_train = FloatTensor(dataset["y_train"].values.copy()).view(-1, 1)
y_test = FloatTensor(dataset["y_test"].values.copy()).view(-1, 1)

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layer1 = nn.Linear(input_size, 16)
        self.first_filter = nn.ReLU()
        self.layer2 = nn.Linear(16, 1)
        self.last_filter = nn.Sigmoid()
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.first_filter(x)
        x = self.layer2(x)
        x = self.last_filter(x)
        return x
    
model = Model()

loss = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), 0.001)

for epoch in range(100):
    optimizer.zero_grad()
    predictions = model.forward(X_train)
    output = loss(predictions, y_train)
    output.backward()
    optimizer.step()
    if epoch % 10 == 0:
        print(output.item())

save(model.state_dict(), "output/model.pth")
print("Training done, model saved")