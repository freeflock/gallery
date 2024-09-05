import os

import requests
from dotenv import load_dotenv


def test_upload_malicious_filename():
    load_dotenv("../gallery.env")
    headers = {"gallery_key": os.getenv("GALLERY_KEY")}
    with open("./painting.png", "rb") as painting_file:
        files = {"file": ("../../malicious.png", painting_file, "image/png")}
        upload_response = requests.post("http://0.0.0.0:36363/upload",
                                        files=files,
                                        headers=headers)
        assert upload_response.status_code == 400


def test_download_insane_filename():
    load_dotenv("../gallery.env")
    headers = {"gallery_key": os.getenv("GALLERY_KEY")}
    upload_response = requests.post("http://0.0.0.0:36363/download",
                                    json={"file_name": "../painting.png"},
                                    headers=headers)
    assert upload_response.status_code == 400


def test_container():
    load_dotenv("../gallery.env")
    headers = {"gallery_key": os.getenv("GALLERY_KEY")}
    with open("./painting.png", "rb") as painting_file:
        files = {"file": ("painting.png", painting_file, "image/png")}
        upload_response = requests.post("http://0.0.0.0:36363/upload",
                                        files=files,
                                        headers=headers)
        assert upload_response.status_code == 200
        download_response = requests.post("http://0.0.0.0:36363/download",
                                          json={"file_name": "painting.png"},
                                          headers=headers)
        assert download_response.status_code == 200
        with open("./output.png", "wb") as output_file:
            output_file.write(download_response.content)

    with open("./painting.png", "rb") as painting_file:
        with open("./output.png", "rb") as output_file:
            assert painting_file.read() == output_file.read()
