from io import BytesIO
import base64

def pil_to_b64(im, enc_format="png", **kwargs):
    buff = BytesIO()
    im.save(buff, format=enc_format, **kwargs)
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")

    return encoded