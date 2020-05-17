import math
import os
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter


def split_pdf_to_even_length_parts(num_of_parts, path):
    reader = PdfFileReader(path)
    num_of_pages = reader.getNumPages()
    avg_part_length = round(num_of_pages / num_of_parts)
    page_ranges = [[n, (n + avg_part_length - 1)]  # inclusive ranges!
                   for n in range(1, num_of_pages, avg_part_length)]
    if page_ranges[-1][1] > num_of_pages:
        page_ranges[-2][1] = num_of_pages
        del page_ranges[-1]
    for first, last in page_ranges:
        writer = PdfFileWriter()
        for i in range(first-1, last):  # getPage works 0-indexed
            writer.addPage(reader.getPage(i))
        root, _ = os.path.splitext(path)
        out_path = root + f'_pp{first}-{last}.pdf'
        with open(out_path, 'wb') as out:
            writer.write(out)
        print(f'Created {out_path}')


def split_pdf_to_parts_of_size(max_size_in_mbytes, path):
    size_in_bytes = os.path.getsize(path)
    size_in_mbytes = size_in_bytes / (1024 ** 2)
    num_of_parts = math.ceil(size_in_mbytes / max_size_in_mbytes)
    split_pdf_to_even_length_parts(num_of_parts, path)

