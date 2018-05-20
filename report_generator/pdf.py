from xhtml2pdf import pisa  # pip install xhtml2pdf


def convert_html_to_pdf(source, pdf_filename):
    # open output file for writing (truncated binary)
    pdf_file = open(pdf_filename, "w+b")

    # convert HTML to PDF
    status = pisa.CreatePDF(source, dest=pdf_file)

    # close output file
    pdf_file.close()

    # return True on success and False on errors
    if status.err is 0:
        return True
    else:
        return False
