import sys
from pathlib import Path
import shutil
import re


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "e", "u", "ja")

TRANS = {}

for k, v in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(k)] = v
    TRANS[ord(k.upper())] = v.upper()


def normalize(name: str) -> str:
    translated_name = name.translate(TRANS)
    translated_name = re.sub(r"\W", "_", translated_name)
    return translated_name

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
DOC_DOC = []
DOCX_DOC = []
XLSX_DOC = []
PPTX_DOC = []
PDF_DOC = []
ZIP_ARCH = []
TAR_ARCH = []
MP3_MUSIC = []
FOLDERS = []
OTHER = []
EXTENSIONS = set()

REGISTERED_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'DOC': DOC_DOC,
    'DOCX': DOCX_DOC,
    'XLSX': XLSX_DOC,
    'PPTX': PPTX_DOC,
    'PDF': PDF_DOC,
    'ZIP': ZIP_ARCH,
    "TAR": TAR_ARCH,
    "MP3": MP3_MUSIC,
    'OTHER': OTHER
}


def parse_folder(path):
    p = Path(path)
    for file in p.iterdir():
        if file.is_dir():
            if file.name not in ['IMAGES', 'DOCS', 'ARCH', 'OTHER', 'VIDEOS', 'MUSIC']:
                FOLDERS.append(file)
                parse_folder(file)

            continue
        else:
            ext = file.suffix[1:].upper()
            EXTENSIONS.add(ext)
            if ext in REGISTERED_EXTENSIONS.keys():
                REGISTERED_EXTENSIONS[ext].append(file)
            else:
                REGISTERED_EXTENSIONS['OTHER'].append(file)

    return REGISTERED_EXTENSIONS


def handle_image(file: Path, root_folder: Path, dist: str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_target_folder = target_folder / ext.upper()
    new_target_folder.mkdir(exist_ok=True)
    new_name = normalize(file.name.replace(ext, "")) + ext
    file.replace(target_folder / new_name)


def handle_doc(file: Path, root_folder: Path, dist: str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_target_folder = target_folder / ext.upper()
    new_target_folder.mkdir(exist_ok=True)
    new_name = normalize(file.name.replace(ext, "")) + ext
    file.replace(target_folder / new_name)


def handle_music(file: Path, root_folder: Path, dist: str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_target_folder = target_folder / ext.upper()
    new_target_folder.mkdir(exist_ok=True)
    new_name = normalize(file.name.replace(ext, "")) + ext
    file.replace(target_folder / new_name)    


def handle_other(file: Path, root_folder: Path, dist: str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_name = normalize(file.name.replace(ext, "")) + ext
    file.replace(target_folder / new_name)


def handle_archive(file: Path, root_folder: Path, dist:str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    folder_for_arch = normalize(file.name.replace(ext, ""))
    archive_folder = target_folder / folder_for_arch
    archive_folder.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(str(file.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    file.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Не удалось удалить папку {folder}")



def main(folder):
    parse_folder(folder)

    for file in DOC_DOC:
        handle_image(file, folder, "DOCS")


    for file in DOCX_DOC:
        handle_image(file, folder, "DOCS")


    for file in PPTX_DOC:
        handle_image(file, folder, "DOCS")


    for file in XLSX_DOC:
        handle_image(file, folder, "DOCS")


    for file in PDF_DOC:
        handle_image(file, folder, "DOSC")

    
    for file in TAR_ARCH:
        handle_image(file, folder, "ARCH")

    
    for file in MP3_MUSIC:
        handle_image(file, folder, "MUSIC")


    for file in JPEG_IMAGES:
        handle_image(file, folder, "IMAGES")

    for file in JPG_IMAGES:
        handle_image(file, folder, "IMAGES")

    for file in PNG_IMAGES:
        handle_image(file, folder, "IMAGES")

    for file in SVG_IMAGES:
        handle_image(file, folder, "IMAGES")

    for file in OTHER:
        handle_other(file, folder, "OTHER")

    for file in ZIP_ARCH:
        handle_archive(file, folder, "ARCH")

    for f in FOLDERS:
        handle_folder(f)



    scan_path = sys.argv[1]
    print(f"Start in folder {scan_path}")
    search_folder = Path(scan_path)

    

