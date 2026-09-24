import httpx

from offbook.insight.config import InsightConfig


def generate(prompt: str, config: InsightConfig) -> str:
    body = {"model": config.ollama_model, "prompt": prompt, "stream": False}
    with httpx.Client(timeout=config.generate_timeout_seconds) as client:
        response = client.post(f"{config.ollama_base_url}/api/generate", json=body)
    response.raise_for_status()
    return response.json()["response"].strip()


def model_is_pulled(config: InsightConfig) -> bool:
    # raises httpx.HTTPError when Ollama itself is down
    with httpx.Client(timeout=5.0) as client:
        response = client.get(f"{config.ollama_base_url}/api/tags")
    response.raise_for_status()

    names = [model["name"] for model in response.json()["models"]]
    return config.ollama_model in names or f"{config.ollama_model}:latest" in names
