from PyPDF2 import PdfFileMerger
import os


def pdf_merger(pdf_dir):
    """
    Merges all the pdfs in one directory
    :param pdf_dir: pdf directory
    """
    merger = PdfFileMerger()
    for file in os.listdir(pdf_dir):
        pdf = os.path.join(pdf_dir, file)
        if file.endswith(".pdf"):
            merger.append(pdf)
    merger.write("pdfs/combined_pdfs.pdf")
    merger.close()
    print("PDF merged")


if __name__ == "__main__":
    pdf_folder = "./pdfs/"
    pdf_merger(pdf_folder)
