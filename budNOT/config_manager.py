import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Загружает конфигурацию из файла."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"expenses": {}, "training_data": [], "calendar": {}}

def save_config(config):
    """Сохраняет конфигурацию в файл."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)

def clear_config():
    """Очищает конфигурацию."""
    config = {"expenses": {}, "training_data": [], "calendar": {}}
    save_config(config)
    return config

def clear_incomes(config):
    """Очищает доходы."""
    config["training_data"] = []
    save_config(config)
    return config

def clear_categories(config):
    """Очищает категории."""
    config["expenses"] = {}
    save_config(config)
    return config
