import yaml
from pathlib import Path

def load_settings():
    settings_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(settings_path, "r", encoding="utf-8") as file:
        settings = yaml.safe_load(file)
    return settings

def load_credentials():
    credentials_path = Path(__file__).parent.parent / "config" / "credentials.yaml"
    with open(credentials_path, "r", encoding="utf-8") as file:
        credentials = yaml.safe_load(file)
    return credentials

if __name__ == "__main__":
    settings = load_settings()
    credentials = load_credentials()

    print("⚙️ Settings loaded:", settings)
    print("🔑 Credentials loaded:", {k: "****" for k in credentials})