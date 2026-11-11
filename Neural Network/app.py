import random
import math

# ---------- Activation function ----------
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(output):
    # derivative expressed in terms of the sigmoid's output
    return output * (1 - output)

# ---------- Training data: AND gate ----------
training_data = [
    ([0, 0], 0),
    ([0, 1], 0),
    ([1, 0], 0),
    ([1, 1], 1),
]

# ---------- Initialize parameters ----------
random.seed(42)
weights = [random.uniform(-1, 1), random.uniform(-1, 1)]
bias = random.uniform(-1, 1)
learning_rate = 0.5
epochs = 10000

# ---------- Forward pass ----------
def predict(inputs):
    z = sum(w * x for w, x in zip(weights, inputs)) + bias
    return sigmoid(z)

# ---------- Training loop ----------
for epoch in range(epochs):
    total_loss = 0
    for inputs, target in training_data:
        # 1. Forward pass
        output = predict(inputs)

        # 2. Error (mean squared error for one sample)
        error = target - output
        total_loss += error ** 2

        # 3. Backpropagation (gradient of loss w.r.t. weights and bias)
        delta = error * sigmoid_derivative(output)

        # 4. Update weights and bias
        for i in range(len(weights)):
            weights[i] += learning_rate * delta * inputs[i]
        bias += learning_rate * delta

    if epoch % 1000 == 0:
        print(f"Epoch {epoch:5d} | Loss: {total_loss / len(training_data):.6f}")

# ---------- Results ----------
print("\nTrained weights:", [round(w, 4) for w in weights])
print("Trained bias:   ", round(bias, 4))

print("\nPredictions:")
for inputs, target in training_data:
    out = predict(inputs)
    print(f"{inputs} -> {out:.4f} (rounded: {round(out)}) | expected: {target}")