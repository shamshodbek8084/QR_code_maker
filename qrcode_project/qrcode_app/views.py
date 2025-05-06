from django.shortcuts import render
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import quote, unquote

def index(request):
    qr_code_image = None
    download_link = None
    data = request.POST.get('data', '')

    if request.method == 'POST' and data:
        # QR kod yaratish
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # QR kod rasmini yaratish
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        img_data = buffer.getvalue()

        # Rasmni Base64 formatiga o‘tkazish
        qr_code_image = base64.b64encode(img_data).decode()

        # Yuklab olish havolasini yaratish
        encoded_data = quote(data, safe='')  # URL'ni kodlash
        download_link = reverse('download_qr', args=[encoded_data])

    return render(request, 'index.html', {
        'qr_code_image': qr_code_image,
        'download_link': download_link,
        'data': data
    })

def download_qr(request, data):
    original_data = unquote(data)  # URL'ni asl holiga qaytarish

    # QR kod yaratish
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(original_data)
    qr.make(fit=True)

    # Rasm yaratish
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # HTTP javobi (QR kodni yuklab olish uchun)
    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
    return response
