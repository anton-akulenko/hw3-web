import os
import shutil

from threading import Thread
from pathlib import Path
import logging
from logger_file import get_logger

log = get_logger(__name__)



def normalize(file_name) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ/@^|"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", '_', "_", "_", "_")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    return file_name.translate(TRANS)

folders_list = []

def search_all_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders_list.append(el)
            search_all_folder(el)


def sort_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                shutil.move(el, new_path / normalize(el.name))
                log.info(
                    f"File {el.name} succesfully copied to {new_path} directory")
            except OSError as e:
                log.error(f"Error {e}")

def del_empty_folder(path):
    if not os.path.isdir(path):
        return
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                del_empty_folder(fullpath)

    files = os.listdir(path)
    if len(files) == 0:
        os.rmdir(path)
        log.warning(f'Path {path} empty and was removed')





if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format="%(threadName)s %(asctime)s %(message)s")

    path_to_sort = 'D:\\test_folder_for_sorting'
    output_path = 'D:\\test_folder_for_sorting\\sorted'
    base_folder = Path(path_to_sort)
    output_folder = Path(output_path)

    folders_list.append(base_folder)
    search_all_folder(base_folder)

    threads = []
    for folder in folders_list:
        folder_thread = Thread(target=sort_file, args=(folder,))
        folder_thread.start()
        threads.append(folder_thread)

    [folder_thread.join() for folder_thread in threads]
    del_empty_folder(path_to_sort)
    print('Sorting done')


