import mimetypes
import os

import magic
import requests

from .HandlerError import HandlerError

ALLOWED_EXTENSIONS = ["pdf"]
VIRUS_ANALYZER_API = "https://www.virustotal.com/gui/home/upload"
UNSUPPORTED_MEDIA_TYPE = "This type of file is not supported"
WARNING_FILE = "File could have potential virus"
NOT_FOUND = "Not found"


def is_valid_type(file, allowed_extensions=ALLOWED_EXTENSIONS):
    mime_type, _ = mimetypes.guess_type(file)
    if mime_type not in allowed_extensions:
        raise HandlerError(UNSUPPORTED_MEDIA_TYPE)

    my_magic = magic.Magic()
    file_type = my_magic.from_buffer(file.read(1024))
    my_magic.close()
    if file_type not in allowed_extensions:
        raise HandlerError(UNSUPPORTED_MEDIA_TYPE)

    return True


def is_safe(file, virus_api=VIRUS_ANALYZER_API) -> str:
    if virus_api is not None:
        is_ok = requests.post(virus_api, files=file)
        if is_ok != 200:
            raise HandlerError(WARNING_FILE)


def upload_file(media_path, uploaded_file, file_name):
    if not os.path.exists(media_path):
        raise HandlerError(NOT_FOUND, f"Path does not exists {media_path}")
    if not os.path.isdir(media_path):
        raise HandlerError(NOT_FOUND, f"Path is not a directory {media_path}")

    # If the old name had no extension, simply return the new name
    file_path = os.path.join(media_path, file_name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())


def file_exists(media_path, file_name: str) -> bool:
    file_path = os.path.join(media_path, file_name)
    if not os.path.isfile(file_path):
        return False
    return True
