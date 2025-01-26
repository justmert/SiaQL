import os
import subprocess
from pathlib import Path


def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    docs_config = project_root / "docs" / "config.yml"
    output_dir = project_root / "docs" / "public"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run SpectaQL with the config file
    subprocess.run(
        [
            "spectaql",
            str(docs_config),
            "--target-dir",
            str(output_dir),
        ],
        check=True,
    )

    print(f"Documentation has been built successfully in {output_dir}")


if __name__ == "__main__":
    main()
