import sys
import os
import shutil
from transliterate import translit


def normalize(filename):
    name, extension = os.path.splitext(filename)
    normalized_name = translit(name, 'ru', reversed=True)
    normalized_name = ''.join(c if c.isalnum() else '_' for c in normalized_name)
    normalized_filename = normalized_name + extension
    return normalized_filename


def sort_files(folder):
    images = []
    videos = []
    documents = []
    music = []
    archives = []
    unknown = []

    for root, dirs, files in os.walk(folder):
        if any(ignore_folder in root for ignore_folder in ["archives", "videos", "audio", "documents", "images"]):
            continue

        for filename in files:
            file_path = os.path.join(root, filename)
            extension = os.path.splitext(filename)[1][1:].upper()
            normalized_filename = normalize(filename)
            normalized_file_path = os.path.join(root, normalized_filename)

            if extension in ['JPEG', 'PNG', 'JPG', 'SVG']:
                images.append(normalized_file_path)
                images_folder = os.path.join(folder, "images")
                os.makedirs(images_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(images_folder, normalized_filename))
            elif extension in ['AVI', 'MP4', 'MOV', 'MKV', 'WEBM']:
                videos.append(normalized_file_path)
                videos_folder = os.path.join(folder, "videos")
                os.makedirs(videos_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(videos_folder, normalized_filename))
            elif extension in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
                documents.append(normalized_file_path)
                documents_folder = os.path.join(folder, "documents")
                os.makedirs(documents_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(documents_folder, normalized_filename))
            elif extension in ['MP3', 'OGG', 'WAV', 'AMR']:
                music.append(normalized_file_path)
                music_folder = os.path.join(folder, "music")
                os.makedirs(music_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(music_folder, normalized_filename))
            elif extension in ['ZIP', 'GZ', 'TAR']:
                archive_folder = os.path.splitext(normalized_file_path)[0]
                archives.append(archive_folder)
                archives_folder = os.path.join(folder, "archives")
                os.makedirs(archives_folder, exist_ok=True)
                shutil.unpack_archive(file_path, os.path.join(archives_folder, normalized_filename))
                os.remove(file_path)
            else:
                unknown.append(normalized_file_path)
                unknown_folder = os.path.join(folder, "unknown")
                os.makedirs(unknown_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(unknown_folder, normalized_filename))

    # Удаляем пустые папки
    for dir_path, _, _ in os.walk(folder, topdown=False):
        if dir_path != folder and not os.listdir(dir_path):
            os.rmdir(dir_path)

    return {
        'images': images,
        'videos': videos,
        'documents': documents,
        'music': music,
        'archives': archives,
        'unknown': unknown
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: clean-folder <folder>")
        sys.exit(1)

    folder = sys.argv[1]
    result = sort_files(folder)

    print("\nUnknown files:")
    print("[" + ", ".join(os.path.basename(file) for file in result['unknown']) + "]")

    print("\nImages:")
    print("[" + ", ".join(os.path.basename(file) for file in result['images']) + "]")

    print("\nVideos:")
    print("[" + ", ".join(os.path.basename(file) for file in result['videos']) + "]")

    print("\nDocuments:")
    print("[" + ", ".join(os.path.basename(file) for file in result['documents']) + "]")

    print("\nMusic:")
    print("[" + ", ".join(os.path.basename(file) for file in result['music']) + "]")

    print("\nArchives:")
    print("[" + ", ".join(os.path.basename(file) for file in result['archives']) + "]")


if __name__ == "__main__":
    main()
