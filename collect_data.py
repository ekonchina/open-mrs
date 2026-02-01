import os

ROOT_DIR = "."          # корневая папка
OUTPUT_FILE = "all_files.txt"

# Директории, которые нужно исключить
EXCLUDED_DIRS = {
    ".venv",
    ".git",
    "node_modules",
    "__pycache__",
    ".idea"
}

def is_binary(file_path, blocksize=512):
    try:
        with open(file_path, "rb") as f:
            return b"\0" in f.read(blocksize)
    except Exception:
        return True

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(ROOT_DIR):
        # Исключаем директории на лету
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            file_path = os.path.join(root, file)

            # Пропускаем бинарные файлы
            if is_binary(file_path):
                continue

            out.write(f"\n{'='*80}\n")
            out.write(f"FILE: {file_path}\n")
            out.write(f"{'='*80}\n")

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"\n[ERROR READING FILE: {e}]\n")

print(f"Готово! Исключены .venv, .git, node_modules, __pycache__. Результат: {OUTPUT_FILE}")

