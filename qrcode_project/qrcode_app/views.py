from django.shortcuts import render
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse

def index(request):
    qr_code_image = None
    download_link = None

    if request.method == 'POST':
        data = request.POST.get('data')  # Get data from the form
        if data:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create an image
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            img_data = buffer.getvalue()

            # Encode image for rendering
            qr_code_image = base64.b64encode(img_data).decode()

            # Create a download link
            download_link = base64.b64encode(img_data).decode()

    return render(request, 'index.html', {
        'qr_code_image': qr_code_image,
        'download_link': download_link,
        'data': request.POST.get('data', '')
    })

def download_qr(request, data):
    # Generate the QR code for download
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Create HTTP response to download the QR code
    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="qrcode.png"'
    return response
