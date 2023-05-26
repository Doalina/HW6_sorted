
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
MP4_VIDEOS = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
OTHERS = []
ARCHIVES = {
    'ZIP': []
}


REGISTER_EXTENSION = {
    "images": {
        'JPEG': JPEG_IMAGES,
        'JPG': JPG_IMAGES,
        'PNG': PNG_IMAGES,
        'SVG': SVG_IMAGES,
    },
    "audio": {
        'MP3': MP3_AUDIO
    },
    "video": {
        'MP4': MP4_VIDEOS
    },
    "documents": {
        'DOC': DOC_DOCUMENTS,
        'DOCS': DOCX_DOCUMENTS,
        'TXT': TXT_DOCUMENTS,
        'PDF': PDF_DOCUMENTS,
    }
}

FOLDERS = []


def get_extension(filename: str) -> str:
    # перетворюємо розширення файлу в назві папки .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        # Якщо це папка то додаємо її в список FOLDERS і переходимо до наступного елементу папки
        if item.is_dir():
            # Перевіряємо, щоб папка не була тією в яку ми вже складаємо файли.
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHER'):
                FOLDERS.append(item)
                # скануємо цю вкладену папку - рекурсія
                scan(item)
            # переходимо до наступного елемента в сканованій папці
            continue

        # Робота з файлом
        ext = get_extension(item.name)  # дістаємо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not ext:
            OTHERS.append(full_name)
        else:
            found = False
            for fldr in REGISTER_EXTENSION:
                for file_ext in REGISTER_EXTENSION[fldr]:
                    if ext == file_ext:
                        container = REGISTER_EXTENSION[fldr][file_ext]
                        container.append(full_name)
                        found = True
                        break
                if found:
                    break
            else:
                if ext in ARCHIVES:
                    ARCHIVES[ext].append(full_name)
                else:
                    OTHERS.append(full_name)


