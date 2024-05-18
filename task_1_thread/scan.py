import sys
from pathlib import Path

archives_str = 'archives'
video_str = 'video'
audio_str = 'audio'
doc_str = 'documents'
images_str = 'images'
others_str = 'others'

archives_files = list()
video_files = list()
audio_files = list()
doc_files = list()
images_files = list()

folders = list()
others = list()

unknown_extensions = set()
known_extentions = {
    archives_str: set(),
    video_str: set(),
    audio_str: set(),
    doc_str: set(),
    images_str: set()
}

registered_extensions = {
    '/ZIP/GZ/TAR/': [archives_files, archives_str],
    '/AVI/MP4/MOV/MKV/': [video_files, video_str],
    '/MP3/OGG/WAV/AMR/': [audio_files, audio_str],
    '/DOC/DOCX/TXT/PDF/XLSX/PPTX/': [doc_files, doc_str],
    '/JPEG/PNG/JPG/SVG/': [images_files, images_str],
    'Not found': [others, others_str]
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):

    for item in folder.iterdir():

        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'others'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        file_full_name = folder/item.name
        
        if not extension:
            others.append(file_full_name)
        else:
            try:
                find_extension = False

                for key_extension, container_list in registered_extensions.items():

                    if '/' + extension + '/' in key_extension:
                        
                        known_extentions[container_list[1]].add(extension)
                        container_list[0].append(file_full_name)

                        find_extension = True
                        break
                
                if not find_extension:
                    unknown_extensions.add(extension)
                    others.append(file_full_name)
                 
            except KeyError:
                unknown_extensions.add(extension)
                others.append(file_full_name)
                

if __name__ == '__main__':

    path = sys.argv[1]
    print(f"Start in {path}")

    folder = Path(path)

    scan(folder)

    print(f"archives: {archives_files}")
    print(f"video: {video_files}")
    print(f"audio: {audio_files}")
    print(f"docs: {doc_files}")
    print(f"images: {images_files}")
    
    print(f"others files: {others}")
    print(f"all known extensions: {known_extentions}")
    print(f"unknown extensions: {unknown_extensions}")
    print(f"folders: {folders}")