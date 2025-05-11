import os
import random
import string
import shutil
from uuid import uuid4
from io import BytesIO
from fastapi import UploadFile
from PIL import Image, ImageOps
from pdf2image import convert_from_path
from dotenv import load_dotenv
import boto3
import logging

from core.exceptions import custom_exception

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class ImageHandler:
    def __init__(self):
        self.backend_url: str | None = os.getenv("BACKEND_URL")
        self.cdn_url: str | None = os.getenv("CDN_URL")
        self.origin_cdn_url: str | None = os.getenv("ORIGIN_CDN_URL")
        self.bucket_name: str | None = os.getenv("DO_SPACES_BUCKET")
        self.client = boto3.session.Session().client(
            "s3",
            region_name=os.getenv("DO_SPACES_REGION"),
            endpoint_url=self.origin_cdn_url,
            aws_access_key_id=os.getenv("DO_SPACES_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("DO_SPACES_SECRET_KEY"),
        )

    @staticmethod
    def is_image(filename: str) -> bool:
        """Check if the file is an image based on its extension."""
        image_extensions: list[str] = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic"]
        return os.path.splitext(filename)[1].lower() in image_extensions

    @staticmethod
    def get_random_string(length: int) -> str:
        """Generate a random string of lowercase letters."""
        return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

    @staticmethod
    def get_random_number_string(length: int) -> str:
        """Generate a random string of digits."""
        digits = string.digits
        return "".join(random.choice(digits) for _ in range(length))

    @staticmethod
    def save_upload_file(upload_file: UploadFile, path: str = "media/temp.pdf"):
        """Save the uploaded file to a specified path."""
        with open(path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

    def pdf_to_single_png(
        self, upload_file: UploadFile, directory: str, file_name: str
    ) -> str:
        """Convert a PDF file to a single PNG image."""
        os.makedirs(directory, exist_ok=True)
        temp_pdf_path: str = os.path.join(directory, f"{uuid4().hex}.pdf")

        with open(temp_pdf_path, "wb") as temp_pdf:
            temp_pdf.write(upload_file.file.read())

        pages: list[Image.Image] = convert_from_path(
            temp_pdf_path, fmt="png", thread_count=4
        )
        file_name: str = file_name.replace(".pdf", ".png")
        final_image_path: str = os.path.join(directory, file_name)

        width, height = pages[0].size
        combined_height: int = height * len(pages)
        combined_image: Image.Image = Image.new("RGB", (width, combined_height))

        for i, page in enumerate(pages):
            combined_image.paste(page, (0, i * height))

        combined_image: Image.Image | None = ImageOps.exif_transpose(combined_image)
        combined_image.save(final_image_path, format="PNG", optimize=True)
        os.remove(temp_pdf_path)

        return final_image_path

    def save_image(
        self,
        image: UploadFile | str,
        directory: str = "common",
        resize: bool = True,
        convert: bool = False,
        random_count: int = 5,
    ) -> str:
        """Save an image to a specified directory and return its URL."""
        if not image:
            return ""
        if isinstance(image, str):
            return image

        file_name: str = f"{self.get_random_string(random_count)}_{image.filename}"

        if convert and ".pdf" in image.filename:
            temp_directory = "temp"
            os.makedirs(temp_directory, exist_ok=True)
            local_path = self.pdf_to_single_png(image, temp_directory, file_name)
            with open(local_path, "rb") as file:
                image_content: bytes = file.read()
            os.remove(local_path)
            file_name: str = file_name.replace(".pdf", ".png")
        else:
            image_content = image.file.read()

        if self.is_image(image.filename) and resize:
            img = Image.open(BytesIO(image_content))
            base_width = 800
            wpercent = base_width / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
            img = ImageOps.exif_transpose(img)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            image_content = buffer.getvalue()

        object_name: str = f"{directory}/{file_name}"

        try:
            content_type: str = (
                "image/png"
                if image.content_type == "application/pdf" and convert
                else image.content_type
            )
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=image_content,
                ACL="public-read",
                ContentType=content_type,
            )
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            raise custom_exception(detail="Failed to upload file. Please try again.")

        return f"{self.cdn_url}/{object_name}"

    def extract_object_key_from_url(self, url: str) -> str:
        """Extract the object key from the URL."""
        return url.replace(f"{self.cdn_url}/", "")

    def remove_single_file(self, file_url: str) -> bool:
        """Remove a single file from the CDN."""
        try:
            object_key = self.extract_object_key_from_url(file_url)
            self.client.delete_object(Bucket=self.bucket_name, Key=object_key)
        except Exception as e:
            logger.error(f"Error deleting file {file_url}: {e}")
            return False
        return True
