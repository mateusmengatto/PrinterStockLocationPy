style_window = """/* --- General Window Background --- */
QWidget {
    background-color: #f9fafb;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    font-size: 12pt;
    color: #2c3e50;
}

/* --- ComboBox --- */
QComboBox {
    background-color: #ffffff;
    border: 2px solid #d1d9e6;
    border-radius: 8px;
    padding: 5px 15px 5px 10px;
    min-height: 28px;
    selection-background-color: #3498db;
    selection-color: white;
}

QComboBox:hover {
    border-color: #2980b9;
}

QComboBox:focus {
    border-color: #1abc9c;
    outline: none;
}

/* Drop-down arrow styling */
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #d1d9e6;
    border-radius: 0 8px 8px 0;
    background-color: #eaf2f8;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;utf8,<svg fill='%233498db' height='12' viewBox='0 0 24 24' width='12' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/></svg>);
}

/* --- QPushButton --- */
QPushButton {
    background-color: #1abc9c;
    border: none;
    border-radius: 10px;
    color: white;
    padding: 8px 25px;
    font-weight: 600;
    transition: background-color 0.3s ease;
}

QPushButton:hover {
    background-color: #16a085;
}

QPushButton:pressed {
    background-color: #148f77;
}

/* --- QLabel --- */
QLabel {
    color: #34495e;
}

/* --- QGroupBox --- */
QGroupBox {
    border: 2px solid #d1d9e6;
    border-radius: 10px;
    margin-top: 15px;
    padding: 10px;
    font-weight: 600;
    color: #34495e;
    background-color: #ffffff;
}

QGroupBox:title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}

/* --- Scrollbars (optional, if you use any) --- */
QScrollBar:vertical {
    background: #f0f3f7;
    width: 12px;
    margin: 0px 0px 0px 0px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #1abc9c;
    min-height: 30px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #16a085;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

/* --- Tooltip --- */
QToolTip {
    background-color: #1abc9c;
    color: white;
    border: none;
    padding: 5px;
    border-radius: 6px;
    font-size: 10pt;
}
"""