from torch import nn, load

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layer1 = nn.Linear(10000, 128)
        self.first_filter = nn.ReLU()
        self.hidden_layer = nn.Linear(128, 16)
        self.second_filter = nn.ReLU()
        self.layer2 = nn.Linear(16, 1)
        self.last_filter = nn.Sigmoid()
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.first_filter(x)
        x = self.hidden_layer(x)
        x = self.second_filter(x)
        x = self.layer2(x)
        x = self.last_filter(x)
        return x
    
def load_model():
    try:
        model = Model()
        model.load_state_dict(load("../output/model.pth", weights_only=True))
        model.eval()
        print("Model successfully loaded!")
        return model
    except FileNotFoundError:
        print("Couldn't find model")
        model = None
        return
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None
        return