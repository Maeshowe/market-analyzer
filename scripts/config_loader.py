import yaml
from pathlib import Path

def load_credentials():
    cred_path = Path(__file__).parent.parent / "config" / "credentials.yaml"
    with open(cred_path, "r") as file:
        return yaml.safe_load(file)

def load_settings():
    settings_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(settings_path, "r") as file:
        return yaml.safe_load(file)

# Tesztelési lehetőség (opcionális)
if __name__ == "__main__":
    credentials = load_credentials()
    settings = load_settings()
    print(credentials)
    print(settings)