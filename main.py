from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename))


def handle_archive(filename: Path, target_folder: Path) -> None:
    # Створюємо папку для архівів
    target_folder.mkdir(exist_ok=True, parents=True)
    # Створюємо папку куди розпаковуємо архів
    # Беремо суфікс у файлу і забираємо replace(filename.suffix, '')
    folder_for_file = target_folder / normalize(filename.with_suffix(""))
    # Створюємо папку для архіву з іменем файлу
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Its not archive {filename}!')
        folder_for_file.rmdir()
        return
    filename.unlink()


def handle_folder(folder: Path) -> None:
    try:
        folder.rmdir()
    except OSError:
        print(f'Sorry, we can not delete the folder: {folder}')


def main(folder: Path) -> None:
    parser.scan(folder)
    for fldr in parser.REGISTER_EXTENSION:
        for ext, file_list in parser.REGISTER_EXTENSION[fldr].items():
            for file in file_list:
                handle_media(file, folder / fldr / ext)

    for file in parser.OTHERS:
        handle_other(file, folder / 'OTHER')
    for file_ext in parser.ARCHIVES:
        for file in parser.ARCHIVES[file_ext]:
            handle_archive(file, folder / 'archives' / file_ext)

    for folder in parser.FOLDERS:
        handle_folder(folder)


def start():
    try:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
    except IndexError:
        print('Please provide folder you need to sort/clean')


if __name__ == '__main__':
    start()