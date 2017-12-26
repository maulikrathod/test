## File names & paths of all Files

import os

folder_name = "data"

input_filename = "input_data.xlsx"
input_file_path = os.path.join(folder_name, input_filename)

updated_input_filename = "input_data.xlsx"
updated_input_file_path = os.path.join(folder_name, updated_input_filename)

input_pdf_filename = "inputfile.pdf"
input_pdf_file_path = os.path.join(folder_name, input_pdf_filename)

output_pdf_filename = "outputfile_with_Footer.pdf"
output_pdf_file_path = os.path.join(folder_name, output_pdf_filename)

logo_name = "input_logo.jpg"
logo_path = os.path.join(folder_name, logo_name)
