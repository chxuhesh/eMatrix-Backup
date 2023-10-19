### Image Generation
import qrcode
from PIL import Image, ImageDraw, ImageFont
### Brother printer device connection
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send,discover
from brother_ql.raster import BrotherQLRaster
from brother_ql.devicedependent import label_type_specs

### Image Generation and send to printer
def text(strlist):
    image = Image.new("RGB", (202, 202), "white")
    draw = ImageDraw.Draw(image)
    result_font = ImageFont.truetype("arial.ttf", size=80)
    font = ImageFont.load_default()
    draw.text((10, 30), strlist, font=font, fill='black')
    return image


def print_image(strlist):
    im = text(strlist)
    backend = 'linux_kernel'  # 'pyusb', 'linux_kernal', 'network'
    model = 'QL-820NWB'  # your printer model.
   # printer = 'usb://0x04f9:0x209d'  # Get these values from the Windows usb driver filter.  Linux/Raspberry Pi uses '/dev/usb/lp0'.
    #printer = 'tcp//192.168.1.108'
    #printer = discover('pyusb')[0]['identifier'][:-2]
    printer = '/dev/usb/lp0'

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    instructions = convert(
        qlr=qlr,
        images=[im],  # Takes a list of file names or PIL objects.
        label='23x23',
        # rotate='Auto',    # 'Auto', '0', '90', '270'
        threshold=70.0,  # Black and white threshold in percent.
        dither=False,
        compress=False,
        red=False,  # Only True if using Red/Black 62 mm label tape.
        dpi_600=False,
        hq=True,  # False for low quality.
        cut=True
    )
    try:
        send_result = send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)
        return send_result['did_print']
    except ValueError as ve:
        print(ve)
        return "Fail Print"

if __name__ == '__main__':
    print(print_image('Pass'))
