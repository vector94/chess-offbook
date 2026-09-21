import httpx

from offbook.insight.config import InsightConfig


def generate(prompt: str, config: InsightConfig) -> str:
    body = {"model": config.ollama_model, "prompt": prompt, "stream": False}
    with httpx.Client(timeout=config.generate_timeout_seconds) as client:
        response = client.post(f"{config.ollama_base_url}/api/generate", json=body)
    response.raise_for_status()
    return response.json()["response"].strip()
