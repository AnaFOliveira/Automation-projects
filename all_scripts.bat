ECHO OFF
ECHO photo editing
python photo_editor.py
ECHO downloading
python youtube_downloader.py "https://www.youtube.com/watch?v=vEQ8CXFWLZU"
ECHO merging
python pdf_merger.py