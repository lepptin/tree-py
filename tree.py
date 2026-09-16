#!/usr/bin/env python3
import os
import sys
import argparse

EXCLUDED_FOLDERS = {'.next', 'node_modules', '.git', 'public'}
INDENT = '  '


def list_files(startpath):
    """Verilen dizindeki klasör ve dosya yapısını tree formatında döndürür."""
    if not os.path.isdir(startpath):
        raise ValueError(f"Hata: '{startpath}' geçerli bir dizin değil.")

    output = []
    for root, dirs, files in os.walk(startpath):
        # Hariç tutulacak klasörleri filtrele
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]
        level = root.replace(startpath, '').count(os.sep)
        indent = INDENT * level
        output.append(f"{indent}📂 {os.path.basename(root) or root}")
        subindent = INDENT * (level + 1)
        for f in files:
            output.append(f"{subindent}📄 {f}")
    return "\n".join(output)


def main():
    # Komut satırı argümanlarını ayrıştır
    parser = argparse.ArgumentParser(
        description="Bir dizindeki klasör ve dosya yapısını tree formatında çıktı olarak verir."
    )
    parser.add_argument(
        "folder_path",
        nargs="?",
        default=".",
        help="Taranacak ana dizinin yolu (varsayılan: mevcut dizin)"
    )
    parser.add_argument(
        "-o", "--output",
        default="output.txt",
        help="Çıktının kaydedileceği dosya adı (varsayılan: output.txt)"
    )

    args = parser.parse_args()
    folder_path = os.path.abspath(args.folder_path)
    output_file = args.output

    # Çıktıyı oluştur
    try:
        result = list_files(folder_path)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # Dosyaya yaz
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"✅ Klasör yapısı '{output_file}' dosyasına kaydedildi.")
    print(f"📍 Taranan dizin: {folder_path}")


if __name__ == "__main__":
    main()
