from PyPDF2 import PdfFileMerger
from .. import pdf_merger
import pytest
import os

"""Further tests:
- test if the merged file was created
- if it has the .pdf 
- if it has the number of pages/images the other has
"""


def test_merger():
    """Tests if pdf merger works as expected"""
    pdf_folder = "./pdfs/"
    pdf_merger.pdf_merger(pdf_folder)
    assert os.path.exists("pdfs/combined_pdfs.pdf")


if __name__ == "__main__":
    pytest.main()
