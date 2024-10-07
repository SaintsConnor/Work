from fastapi import FastAPI, Request, Form, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

from fastapi.responses import FileResponse
import os

@app.get("/download_saq_pdf/{saq_type}")
async def download_saq_pdf(request: Request, saq_type: str):
    saq_type_url_map = {
        "SAQ A": "saq_files/PCI-DSS-v4-0-SAQ-A-r1.docx",
        "SAQ A-EP": "saq_files/PCI-DSS-v4-0-SAQ-A-EP-r1.docx",
        "SAQ B": "saq_files/PCI-DSS-v4-0-SAQ-B-r1.docx",
        "SAQ B-IP": "saq_files/PCI-DSS-v4-0-SAQ-B-IP-r1.docx",
        "SAQ C": "saq_files/PCI-DSS-v4-0-SAQ-C-r1.docx",
        "SAQ C-VT": "saq_files/PCI-DSS-v4-0-SAQ-C-VT-r1.docx",
        "SAQ D for Merchants": "saq_files/PCI-DSS-v4-0-SAQ-D-Merchant-r1.docx",
        "SAQ D for Service Providers": "saq_files/PCI-DSS-v4-0-SAQ-D-Service-Provider-r1.docx",
        "SAQ P2PE": "saq_files/PCI-DSS-v4-0-SAQ-P2PE-r1.docx"
    }

    saq_file_path = saq_type_url_map.get(saq_type)
    if saq_file_path is None:
        raise HTTPException(status_code=404, detail="SAQ type not found")
    return FileResponse(saq_file_path)

@app.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/get_saq_type")
def get_saq_type(request: Request, service_provider: str = Form(...), card_data_storage: str = Form(...), e_commerce: str = Form(...), face_to_face: str = Form(...), moto: str = Form(...), pci_dss_compliant_provider: str = Form(...), p2pe: str = Form(...), internet_connection: str = Form(...), payment_app: str = Form(...), pts_check: str = Form(...)):
    if service_provider.lower() == "yes":
        saq_type = "SAQ D for Service Providers"
    else:
        if card_data_storage.lower() == "yes":
            saq_type = "SAQ D for Merchants"
        else:
            if e_commerce.lower() == "yes":
                if pci_dss_compliant_provider.lower() == "yes":
                    saq_type = "SAQ A"
                elif payment_outsourced.lower() == "yes":
                    saq_type = "SAQ A-EP"
                else:
                    saq_type = "SAQ D for Merchants"
            else:
                if face_to_face.lower() == "yes":
                    if p2pe.lower() == "yes":
                        saq_type = "SAQ P2PE"
                    else:
                        if internet_connection.lower() == "no":
                            saq_type = "SAQ B"
                        else:
                            if payment_app.lower() == "yes":
                                saq_type = "SAQ C-VT"
                            elif pts_check.lower() == "yes":
                                saq_type = "SAQ B-IP"
                            else: 
                                saq_type = "SAQ C"
                else:
                    if pci_dss_compliant_provider.lower() == "yes":
                        saq_type = "SAQ A"
                    else:
                        if internet_connection.lower() == "no":
                            saq_type = "SAQ B"
                        else:
                            if payment_app.lower() == "yes":
                                saq_type = "SAQ C-VT"
                            elif pts_check.lower() == "yes":
                                saq_type = "SAQ B-IP"
                            else: 
                                saq_type = "SAQ C"
    
    
    return templates.TemplateResponse("result.html", {"request": request, "saq_type": saq_type})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3333)
