import os

from starlette.testclient import TestClient


def test_authentication_empty_header():
    os.environ["GALLERY_KEY"] = "super_secret"
    os.environ["STORAGE_DIRECTORY"] = "/tmp/gallery"
    from gallery.main import app
    with TestClient(app) as client:
        with open("./painting.png", "rb") as painting_file:
            response = client.post("/upload", files={"file": painting_file})
            assert response.status_code == 403
            response = client.post("/download", json={"file_name": "painting.png"})
            assert response.status_code == 403


def test_authentication_invalid_key():
    os.environ["GALLERY_KEY"] = "super_secret"
    os.environ["STORAGE_DIRECTORY"] = "/tmp/gallery"
    from gallery.main import app
    with TestClient(app) as client:
        headers = {"gallery_key": "wrong"}
        with open("./painting.png", "rb") as painting_file:
            response = client.post("/upload", files={"file": painting_file}, headers=headers)
            assert response.status_code == 403
            response = client.post("/download", json={"file_name": "painting.png"}, headers=headers)
            assert response.status_code == 403


def test_upload_invalid_mime_type():
    os.environ["GALLERY_KEY"] = "super_secret"
    os.environ["STORAGE_DIRECTORY"] = "/tmp/gallery"
    from gallery.main import app
    with TestClient(app) as client:
        headers = {"gallery_key": "super_secret"}
        with open("./painting.pdf", "rb") as painting_file:
            response = client.post("/upload", files={"file": painting_file}, headers=headers)
            assert response.status_code == 400


def test_upload():
    os.environ["GALLERY_KEY"] = "super_secret"
    os.environ["STORAGE_DIRECTORY"] = "/tmp/gallery"
    from gallery.main import app
    with TestClient(app) as client:
        headers = {"gallery_key": "super_secret"}
        with open("./painting.png", "rb") as painting_file:
            response = client.post("/upload", files={"file": painting_file}, headers=headers)
            assert response.status_code == 200


def test_download_does_not_exist():
    os.environ["GALLERY_KEY"] = "super_secret"
    os.environ["STORAGE_DIRECTORY"] = "/tmp/gallery"
    from gallery.main import app
    with TestClient(app) as client:
        headers = {"gallery_key": "super_secret"}
        download_response = client.post("/download", json={"file_name": "nonsense.png"}, headers=headers)
        assert download_response.status_code == 400


def test_download():
    os.environ["GALLERY_KEY"] = "super_secret"
    os.environ["STORAGE_DIRECTORY"] = "/tmp/gallery"
    from gallery.main import app
    with TestClient(app) as client:
        headers = {"gallery_key": "super_secret"}
        with open("./painting.png", "rb") as painting_file:
            upload_response = client.post("/upload", files={"file": painting_file}, headers=headers)
            assert upload_response.status_code == 200
            download_response = client.post("/download", json={"file_name": "painting.png"}, headers=headers)
            assert download_response.status_code == 200
            with open("./output.png", "wb") as output_file:
                output_file.write(download_response.content)

        with open("./painting.png", "rb") as painting_file:
            with open("./output.png", "rb") as output_file:
                assert painting_file.read() == output_file.read()
