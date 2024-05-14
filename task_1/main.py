import sys
import shutil
from pathlib import Path

import scan
import normalize

from threading import Thread
import datetime


def handle_files(folder_path, file_path, folder_name):

    if folder_name == scan.archives_str:
        handle_archive(folder_path, file_path, folder_name)
    else:

        type_folder = folder_path/folder_name
        type_folder.mkdir(exist_ok=True)
        file_path.replace(type_folder/normalize.normalize(file_path.name))


def handle_archive(folder_path, file_path, archive_folder_name):

    archive_folder = folder_path / archive_folder_name
    archive_folder.mkdir(exist_ok=True)

    extention = Path(file_path.name).suffix
    archive_file_folder_name = normalize.normalize(file_path.name.replace(extention, '')) 

    archive_file_folder = archive_folder / archive_file_folder_name
    archive_file_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(file_path.resolve()), str(archive_file_folder.resolve()))
    except shutil.ReadError:
        archive_file_folder.rmdir()
        return
    except FileNotFoundError:
        archive_file_folder.rmdir()
        return
    
    file_path.unlink()


def remove_empty_folders(path):

    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def main(folder_path):
    threads = []
    scan.scan(folder_path)

    for container_list in scan.registered_extensions.values():
        for file in container_list[0]:
            # Виклик функції переведено на використання потоків
            # handle_files(folder_path, file, container_list[1])
            th = Thread(target=handle_files, args=(folder_path, file, container_list[1]))
            th.start()
            threads.append(th)
    
    [th.join() for th in threads]
    remove_empty_folders(folder_path)


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())

    end_time = datetime.datetime.now()
    print(f'result time: {end_time - start_time}')

    # print(f"folders: {scan.folders}")
    # print(f"archives: {scan.archives_files}")
    # print(f"video: {scan.video_files}")
    # print(f"audio: {scan.audio_files}")
    # print(f"docs: {scan.doc_files}")
    # print(f"images: {scan.images_files}")
    
    # print(f"others files: {scan.others}")
    
    # print(f"all known extensions: {scan.known_extentions}")
    # print(f"unknown extensions: {scan.unknown_extensions}")
    