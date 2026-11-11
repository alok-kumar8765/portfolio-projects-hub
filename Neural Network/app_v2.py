import math
import random

# Fix seed for reproducible results
random.seed(42)

# 1. Activation Function & Derivative
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_derivative(x):
    # Derivative of Sigmoid in terms of output y = sigmoid(x) is y * (1 - y)
    return x * (1.0 - x)

# 2. Dataset for AND Logic Gate
# Input features (X1, X2) and expected Target output (Y)
X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]
Y = [0, 0, 0, 1]

# 3. Model Parameters
learning_rate = 0.5
epochs = 10000

# Initialize weights and bias with small random values
weights = [random.uniform(-1, 1), random.uniform(-1, 1)]
bias = random.uniform(-1, 1)

print("--- Initial Parameters ---")
print(f"Weights: {weights}")
print(f"Bias: {bias}\n")

# 4. Training Loop (Gradient Descent & Backpropagation)
for epoch in range(epochs):
    total_loss = 0.0

    for i in range(len(X)):
        x1, x2 = X[i]
        target = Y[i]

        # --- Forward Pass ---
        # Weighted sum: z = (w1 * x1) + (w2 * x2) + b
        z = (x1 * weights[0]) + (x2 * weights[1]) + bias
        # Activation: y = sigmoid(z)
        output = sigmoid(z)

        # Loss calculation (Mean Squared Error per sample)
        error = target - output
        total_loss += error ** 2

        # --- Backward Pass (Backpropagation) ---
        # Derivative of error with respect to pre-activation z
        # Loss = (target - output)^2 -> dLoss/dOutput = -2 * (target - output)
        # Output = sigmoid(z)       -> dOutput/dZ = output * (1 - output)
        # Combined gradient term (ignoring scaling constant 2):
        d_z = error * sigmoid_derivative(output)

        # Gradients with respect to weights and bias
        d_w1 = d_z * x1
        d_w2 = d_z * x2
        d_b  = d_z

        # --- Update Weights & Bias ---
        weights[0] += learning_rate * d_w1
        weights[1] += learning_rate * d_w2
        bias       += learning_rate * d_b

    # Print loss every 2000 epochs
    if (epoch + 1) % 2000 == 0 or epoch == 0:
        mse = total_loss / len(X)
        print(f"Epoch {epoch + 1}/{epochs} - Loss (MSE): {mse:.6f}")

print("\n--- Training Complete ---")
print(f"Learned Weights: [w1={weights[0]:.4f}, w2={weights[1]:.4f}]")
print(f"Learned Bias: {bias:.4f}\n")

# 5. Testing & Predictions
print("--- Predictions for AND Gate ---")
for x1, x2 in X:
    z = (x1 * weights[0]) + (x2 * weights[1]) + bias
    output = sigmoid(z)
    prediction = 1 if output >= 0.5 else 0
    print(f"Input: [{x1}, {x2}] -> Raw Output: {output:.4f} -> Predicted: {prediction}")