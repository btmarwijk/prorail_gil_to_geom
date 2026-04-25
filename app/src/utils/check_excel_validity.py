import shutil
from pathlib import Path

from utils.excel_reader import ExcelReader


def sort_excel_files(file_paths: list[Path], base_dir: Path):
    """
    Attempts to read Excel files and moves them to 'valid_file' or 'unvalid_file'.
    """
    # 1. Define and create target directories
    valid_dir = base_dir / "valid_file"
    invalid_dir = base_dir / "invalid_file"

    valid_dir.mkdir(parents=True, exist_ok=True)
    invalid_dir.mkdir(parents=True, exist_ok=True)

    results = {"valid": 0, "invalid": 0}

    for file_path in file_paths:
        # Ignore temporary Excel lock files (starting with ~$)
        if file_path.name.startswith("~$"):
            continue

        try:
            # 2. Attempt to read the file
            # We only read the header (nrows=0) to make the check fast
            ExcelReader(file_path).render()

            # 3. If successful, move to valid_dir
            shutil.copy(file_path, valid_dir / file_path.name)
            results["valid"] += 1
            print(f"✅ Valid: {file_path.name}")

        except Exception as e:
            # 4. If it fails (corrupt, wrong format, encrypted), move to invalid_dir
            shutil.copy(file_path, invalid_dir / file_path.name)
            results["invalid"] += 1
            print(f"❌ Invalid: {file_path.name} | Reason: {e}")

    return results


if __name__ == "__main__":
    from core.config import test_files

    sort_excel_files(test_files.excel_files, base_dir=Path("./data/output/"))
