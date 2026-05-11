"""
QR code generation for digital tickets.
"""

import io
import json
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M

from app.config import get_settings


def generate_qr_code(data: str) -> bytes:
    """Generate a QR code PNG image as bytes."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_ticket_qr(ticket_code: str) -> str:
    """Generate a QR code for a ticket and save it locally. Returns the URL path."""
    settings = get_settings()
    payload = json.dumps({"code": ticket_code, "v": 1})
    png_bytes = generate_qr_code(payload)

    key = f"qrcodes/{ticket_code}.png"
    upload_root = Path(settings.upload_dir)
    file_path = upload_root / key
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(png_bytes)

    if settings.upload_base_url:
        return f"{settings.upload_base_url.rstrip('/')}/{key}"
    return f"/uploads/{key}"
