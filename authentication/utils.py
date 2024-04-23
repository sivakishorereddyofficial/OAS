

import qrcode
from io import BytesIO
from base64 import b64encode


def generate_qr(string):
    qrcode_img = qrcode.make(string)  # This should be the device for which you want to generate the QR code
    buffer = BytesIO()
    qrcode_img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64,{encoded_img}'

    return qr_code_data