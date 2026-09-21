# Standard Library
import re

try:
    # Standard Library
    import tomllib
except ImportError:
    # Third Party
    import tomli as tomllib

# This script prints the minimal version of Openfisca-Core to ensure their compatibility during CI testing
with open("./pyproject.toml", "rb") as file:
    config = tomllib.load(file)
    deps = config["project"]["dependencies"]
    # Depuis la 8.0.0, ce paquet ne dépend plus d'openfisca-core directement, mais
    # d'openfisca-tunisia[pension], qui livre le système des pensions : c'est alors sa
    # version minimale qu'il faut tester.
    for dep in deps:
        version = re.search(r"(openfisca-core|openfisca-tunisia)\[([^\]]+)\]\s*>=\s*([\d\.]*)", dep)
        if version:
            try:
                print(f"{version[1]}[{version[2]}]=={version[3]}")
            except Exception as e:
                print(f'Error processing "{dep}": {e}')
                exit(1)
