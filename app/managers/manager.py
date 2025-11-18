import os
import re
import io
import zipfile


class PYQManager:
    """Handles business logic for subjects, papers, filtering, and ZIP creation."""

    def __init__(self, base_folder: str):
        self.base_folder = base_folder

    # -----------------------------------------
    # Extract Year
    # -----------------------------------------
    def extract_year(self, filename: str) -> str:
        match = re.search(r"(20\d{2})", filename)
        return match.group(1) if match else "Unknown Year"

    # -----------------------------------------
    # Get Subject Folders
    # -----------------------------------------
    def get_subjects(self):
        if not os.path.exists(self.base_folder):
            return []

        return [
            d for d in os.listdir(self.base_folder)
            if os.path.isdir(os.path.join(self.base_folder, d))
        ]

    # -----------------------------------------
    # Get Files for a Selected Subject
    # -----------------------------------------
    def get_files(self, subject: str):
        subject_path = os.path.join(self.base_folder, subject)

        if not os.path.exists(subject_path):
            return []

        output = []
        for filename in os.listdir(subject_path):
            full_path = os.path.join(subject_path, filename)

            if os.path.isfile(full_path):
                year = self.extract_year(filename)
                output.append({
                    "file_name": filename,
                    "full_path": full_path,
                    "year": year
                })

        return output

    # -----------------------------------------
    # Filter by Year
    # -----------------------------------------
    def filter_by_year(self, files, year):
        if year == "All Years":
            return files
        return [f for f in files if f["year"] == year]

    # -----------------------------------------
    # Filter by Keyword
    # -----------------------------------------
    def filter_by_keyword(self, files, keyword):
        keyword = keyword.lower().strip()
        if not keyword:
            return files

        return [
            f for f in files
            if keyword in f["file_name"].lower()
        ]

    # -----------------------------------------
    # Create ZIP File
    # -----------------------------------------
    def create_zip(self, file_paths):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for path in file_paths:
                zipf.write(path, os.path.basename(path))
        return buffer.getvalue()
