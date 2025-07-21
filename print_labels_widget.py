from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont, ImageWin
import qrcode
import win32print
import win32ui
import sys
from style import style_window

# Seu código original (simplificado para o exemplo):
def format_loc_code(raw_code, location_type):
    parts = raw_code.strip().split()
    if location_type == 'normal':
        R = parts[0]
        B = parts[1]
        N = parts[2][0]
        L = parts[2][1:]
    else:
        R = parts[0]
        B = parts[1]
        N = parts[2][0:2]
        L = parts[2][2:]
    return R, B, N, L

def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return w, h

def create_label_image(code_text, location_type):
    DPI = 203
    mm_to_inch = 25.4
    width_mm = 75
    height_mm = 40

    width_px = int(DPI * width_mm / mm_to_inch)
    height_px = int(DPI * height_mm / mm_to_inch)

    img = Image.new('L', (width_px, height_px), 255)
    draw = ImageDraw.Draw(img)

    try:
        font_small = ImageFont.truetype("arial.ttf", 40)
        font_medium = ImageFont.truetype("arial.ttf", 68)
        font_big = ImageFont.truetype("arial.ttf", 250)
    except IOError:
        font_small = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_big = ImageFont.load_default()

    R, B, N, L = format_loc_code(code_text, location_type)

    loc_text = f"{R} - {B} - {N} - {L}"
    x_text, y_text = 20, 10
    w, h = get_text_size(draw, loc_text, font_medium)

    # Desenha a caixa (retângulo) com margem
    margin = 10
    box_coords = [x_text - margin, y_text, x_text + w + margin + 2, y_text + h + margin + 10]
    draw.rectangle(box_coords, outline=0, width=3)  # contorno preto e mais grosso

    # Desenha o texto dentro da caixa
    draw.text((x_text, y_text), loc_text, font=font_medium, fill=0)

    last_num_text = N + ' ' + L
    last_num_x = 20
    last_num_y = 70
    draw.text((last_num_x, last_num_y), last_num_text, font=font_big, fill=0)

    qr = qrcode.make(code_text)
    qr_size = 100
    qr = qr.resize((qr_size, qr_size))
    qr_x = 470
    qr_y = 5
    img.paste(qr, (qr_x, qr_y))

    return img

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

# --- Interface PySide6 ---

class LabelWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Etiquetas")
        self.setMinimumWidth(600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet(style_window)

        # Combo para escolher modo
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Normal", "Colméias"])
        self.mode_combo.currentTextChanged.connect(self.on_mode_change)
        layout.addWidget(QLabel("Selecione o modo:"))
        layout.addWidget(self.mode_combo)

        # Grupo para seleção R, B, N, L
        self.group = QGroupBox("Configurações")
        self.group_layout = QVBoxLayout()

        # R, B, N combos (com as opções R, B, N, L)
        self.combo_R = QComboBox()
        self.combo_B = QComboBox()
        self.combo_N = QComboBox()
        for c in ['00', '01', '02', '03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']:
            self.combo_R.addItem(c)
        
        for d in ['1', '2', '3', '4', '5', '6', '7', '8']:
            self.combo_B.addItem(d)

        hb_r = QHBoxLayout()
        hb_r.addWidget(QLabel("R:"))
        hb_r.addWidget(self.combo_R)
        hb_r.addWidget(QLabel("B:"))
        hb_r.addWidget(self.combo_B)
        hb_r.addWidget(QLabel("N:"))
        hb_r.addWidget(self.combo_N)
        self.group_layout.addLayout(hb_r)

        # Para L, dois combos para início e fim (números no normal, letras no colmeia)
        self.l_start_combo = QComboBox()
        self.l_end_combo = QComboBox()

        l_layout = QHBoxLayout()
        l_layout.addWidget(QLabel("L início:"))
        l_layout.addWidget(self.l_start_combo)
        l_layout.addWidget(QLabel("L fim:"))
        l_layout.addWidget(self.l_end_combo)
        self.group_layout.addLayout(l_layout)

        self.group.setLayout(self.group_layout)
        layout.addWidget(self.group)

        # Botão para gerar e imprimir
        self.print_btn = QPushButton("Imprimir")
        self.print_btn.clicked.connect(self.on_print)
        layout.addWidget(self.print_btn)

        self.setLayout(layout)

        # Inicializa combos para modo normal
        self.populate_l_combos('normal')

    def on_mode_change(self, text):
        if text == "Normal":
            self.populate_l_combos('normal')
        else:
            self.populate_l_combos('colmeia')

    def populate_l_combos(self, mode):
        self.l_start_combo.clear()
        self.l_end_combo.clear()
        self.combo_N.clear()

        if mode == 'normal':
            # números 1 a 99
            for i in range(1, 100):
                str_i = str(i).zfill(2)
                self.l_start_combo.addItem(str(str_i))
                self.l_end_combo.addItem(str(str_i))
            for c in range(ord('A'), ord('Z')+1):
                self.combo_N.addItem(chr(c))
        else:
            # letras A a Z
            for c in range(ord('A'), ord('Z')+1):
                letra = chr(c)
                self.l_start_combo.addItem(letra)
                self.l_end_combo.addItem(letra)
            for i in range(1, 100):
                str_i = str(i).zfill(2)
                self.combo_N.addItem(str_i)


    def on_print(self):
        mode_text = self.mode_combo.currentText().lower()
        R = self.combo_R.currentText()
        B = self.combo_B.currentText()
        N = self.combo_N.currentText()
        L_start = self.l_start_combo.currentText()
        L_end = self.l_end_combo.currentText()

        # Função auxiliar para gerar a lista de valores entre start e end
        def range_values(start, end, mode):
            if mode == 'normal':
                start_num = int(start)
                end_num = int(end)
                if start_num > end_num:
                    start_num, end_num = end_num, start_num  # inverter se necessário
                return [str(i).zfill(2) for i in range(start_num, end_num + 1)]
            else:
                # letras, converter para código ascii
                start_ord = ord(start.upper())
                end_ord = ord(end.upper())
                if start_ord > end_ord:
                    start_ord, end_ord = end_ord, start_ord
                return [chr(c) for c in range(start_ord, end_ord + 1)]

        for L_value in range_values(L_start, L_end, mode_text):
            if mode_text == 'normal':
                code_text = f"{R} {B}  {N}{L_value}"
            else:
                code_text = f"{R} {B}  {N}{L_value}"

            img = create_label_image(code_text, location_type=mode_text)
            print_image(img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LabelWindow()
    win.show()
    sys.exit(app.exec())
