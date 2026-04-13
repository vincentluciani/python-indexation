"""Load YAML configuration files from the config directory."""

from pathlib import Path
import yaml


def load_yaml_config(configuration_name):
    """Return parsed YAML configuration data for the given name."""
    script_path = Path(__file__).resolve().parents[2] / "config" / (
        f"{configuration_name}.yaml"
    )

    with script_path.open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)
