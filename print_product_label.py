'''PrintProductLabelPack'''


from PIL import Image, ImageDraw, ImageFont, ImageWin
import barcode
from barcode.writer import ImageWriter
import win32print
import win32ui
import os


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def create_label_image(product_code, description, barcode_number, lote, quantity, unit):
    DPI = 203
    mm_to_inch = 25.4
    width_mm = 40
    height_mm = 40
    
    path = os.path.dirname(__file__)
    logo_path = os.path.join(path, 'logo_dbtruck.png')
    
    width_px = int(DPI * width_mm / mm_to_inch)
    height_px = int(DPI * height_mm / mm_to_inch)

    img = Image.new('L', (width_px, height_px), 255)
    draw = ImageDraw.Draw(img)

    try:
        font_small = ImageFont.truetype("LiberationSans-Bold.ttf", 20)
        font_medium = ImageFont.truetype("LiberationSans-Bold.ttf", 42)
        font_large = ImageFont.truetype("LiberationSans-Bold.ttf", 50)
    except IOError:
        font_small = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_large = ImageFont.load_default()

    # Código e logo
    y=300
    len_code = len(str(product_code).strip())
    size_font_code = 42
    if len_code > 13 and len_code <= 16:
        size_font_code = 35
    elif len(str(product_code).strip()) > 16:
        size_font_code = 25
    
    font_code = ImageFont.truetype("LiberationSans-Bold.ttf", size_font_code)
    draw.text((10, 3), product_code, font=font_code, fill=0)
    draw.line((0, 55, width_px, 55), fill=0, width=1)
    # Descrição
    draw_multiline_text(draw, description, font_small, width_px - 10, (5, 55))

    # Código de barras
    barcode_writer_options = {
    'module_width': 0.2,
    'module_height': 6.0,
    'font_size': 5,
    'text_distance': 3,
    'quiet_zone': 2,
    'write_text': True,
    'background': 'white',
    'foreground': 'black'
    }
    
    def generate_barcode_image(code: str):
        code = code.strip()
        if not code.isdigit():
            raise ValueError("Código deve conter apenas dígitos")

        length = len(code)

        if length == 8 or length == 9:
            barcode_type = 'ean8'
            data = code[:7]  # usa os 7 primeiros para gerar (ignora o 8º/9º se houver)
            ean_class = barcode.get_barcode_class(barcode_type)
            ean = ean_class(data, writer=ImageWriter())
            # Validação opcional
            if length == 8:
                expected = ean.get_fullcode()
                if code != expected:
                    raise ValueError(f"Dígito verificador inválido para EAN-8. Esperado: {expected}")
        elif length == 12 or length == 13:
            barcode_type = 'ean13'
            data = code[:12]  # usa os 12 primeiros
            ean_class = barcode.get_barcode_class(barcode_type)
            ean = ean_class(data, writer=ImageWriter())
            # Validação opcional
            if length == 13:
                expected = ean.get_fullcode()
                if code != expected:
                    raise ValueError(f"Dígito verificador inválido para EAN-13. Esperado: {expected}")
            
        else:
            raise ValueError("Código deve conter 8, 9, 12 ou 13 dígitos")
        

        # Gera imagem
        return ean.render(writer_options=barcode_writer_options).convert('L')

    ean_img = generate_barcode_image(barcode_number)



    ean_resized = ean_img
    # Centraliza horizontalmente
    x_position = (width_px - ean_resized.width) // 2
    img.paste(ean_resized, (x_position, 180))  # Y pode ser ajustado conforme altura da etiqueta

    # Lote
    draw.text((5, 140), f"Lote", font=font_small, fill=0)
    draw.text((5, 160), lote, font=font_small, fill=0)

    # Quantidade
    quanti_x = 170
    wq, _ = get_text_size(draw, str(quantity), font_large) 
    quanti_unit = quanti_x + 5 + wq
    draw.text((quanti_x, 130), str(quantity), font=font_large, fill=0)
    draw.text((quanti_unit, 150), unit, font=font_small, fill=0)

    try:
        logo = Image.open(logo_path).convert('L')
        logo = logo.resize((50, 50))
        img.paste(logo, (10, 270))
    except Exception as e:
        print("Erro ao carregar o logo:", e)
        
    
    draw.text((75, 300), "www.dbtruck.com.br", font=font_small, fill=0)

    return img

def draw_multiline_text(draw, text, font, max_width, position, fill=0, line_spacing=4):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        w, _ = get_text_size(draw, test_line, font)
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    x, y = position
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = font.getbbox(line)
        line_height = bbox[3] - bbox[1]
        y += line_height + line_spacing

def print_image(img):
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    hDC.StartDoc("Etiqueta")
    hDC.StartPage()

    dib = ImageWin.Dib(img)
    dib.draw(hDC.GetHandleOutput(), (0, 0, img.width, img.height))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

def print_labels_in_batch(img, copies=1):
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    hDC.StartDoc("Etiquetas")

    for _ in range(copies):
        hDC.StartPage()
        dib = ImageWin.Dib(img)
        dib.draw(hDC.GetHandleOutput(), (0, 0, img.width, img.height))
        hDC.EndPage()

    hDC.EndDoc()
    hDC.DeleteDC()


if __name__ == "__main__":
    product_code = "FIX18  "
    description = "ALTO FALANTE 6X9 QUADRIAXIAL PAR HURRICANE (180W RMS PAR)"
    barcode_number = "8727900390483       "
    lote = "22/07/2025"
    quantity = 1
    unit = "PR"


    etiqueta_img = create_label_image(product_code, description, barcode_number, lote, quantity, unit)
    etiqueta_img.show()
    print_labels_in_batch(etiqueta_img, 3)
    
