# mcp_server.py
import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Iris Classifier", log_level="WARNING")


@mcp.tool()
def classify_iris(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> str:
    """Classify an iris flower from its four measurements, in centimeters.
    Returns the predicted species: setosa, versicolor, or virginica.
    """
    response = httpx.post(
        "http://127.0.0.1:8000/predict",
        json={
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
        },
    )
    return f"Predicted species: {response.json()['species']}"


@mcp.tool()
def iris_probabilities(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> str:
    """Estimate how likely an iris flower is to be each species, from its four measurements in centimeters.
    Returns a probability (0 to 1) for setosa, versicolor, and virginica that sum to about 1.
    Use this instead of classify_iris when the user asks how confident or sure the model is,
    wants to see the alternatives, or when the flower may be borderline between two species.
    Use classify_iris when only the single most likely species is needed.
    """
    response = httpx.post(
        "http://127.0.0.1:8000/probabilities",
        json={
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
        },
    )
    probs = response.json()
    return "Species probabilities: " + ", ".join(f"{k} {v:.2f}" for k, v in probs.items())


if __name__ == "__main__":
    mcp.run()
