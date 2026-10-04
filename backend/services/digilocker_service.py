DIGILOCKER_REDIRECTS = {
    "Aadhaar": "https://myaadhaar.uidai.gov.in/",
    "PAN": "https://www.onlineservices.nsdl.com/paam/ReprintEPan.html",
    "Driving Licence": "https://parivahan.gov.in/",
    "DigiLocker Portal": "https://www.digilocker.gov.in/"
}


def get_digilocker_routes() -> dict:
    return DIGILOCKER_REDIRECTS