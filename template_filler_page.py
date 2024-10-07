from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from docx import Document
from datetime import date
from pathlib import Path
import uvicorn

app = FastAPI()

TEMPLATE_DOCX_PATH = Path("templates/PCI Policy.docx")  # Path to the template docx file


def replace_merge_fields(document, field_value, author_name, network_name, network_desc):
    current_date = date.today().strftime('%d/%m/%Y')

    for element in document._element.iter():
        if element.tag.endswith(('}t', '}p', '}r')):
            for child in element.iter():
                if child.text:
                    if '[Company]' in child.text:
                        child.text = child.text.replace('[Company]', field_value)
                    if '[Date]' in child.text:
                        child.text = child.text.replace('[Date]', current_date)
                    if '[Author]' in child.text:
                        child.text = child.text.replace('[Author]', author_name)
                    if '[Network]' in child.text:
                        child.text = child.text.replace('[Network]', network_name)

                    if '[Desc]' in child.text:
                        child.text = child.text.replace('[Desc]', network_desc)



@app.post("/generate-docx")
async def generate_docx(
    company_name: str = Form(...),
    author_name: str = Form(...),
    network_name: str = Form(...),
    network_desc: str = Form(...),
):
    # Open the template Word document
    template_doc = Document(TEMPLATE_DOCX_PATH)

    # Replace merge fields in the template
    replace_merge_fields(template_doc, company_name, author_name, network_name, network_desc)

    # Generate a new file name
    new_file_name = f"{company_name}_PCI_Policy.docx"

    # Save the modified document with the new name
    template_doc.save(new_file_name)

    return FileResponse(new_file_name, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3333)
