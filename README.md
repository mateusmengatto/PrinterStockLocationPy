# Gerador de Etiquetas com PySide6

Este projeto é uma aplicação desktop em Python para geração e impressão de etiquetas personalizadas, com interface gráfica feita em PySide6. O sistema permite selecionar dois modos de formatação ("Normal" e "Colméia"), configurar códigos de localização via combos, gerar imagens das etiquetas com QR Code e enviá-las para a impressora padrão do Windows.

---

## Funcionalidades

* Interface gráfica amigável com PySide6
* Seleção entre modo **Normal** e **Colméia**
* Configuração dos campos R, B, N e L via ComboBoxes
* Para o campo **L**, seleção de intervalo (início e fim) com números (modo Normal) ou letras (modo Colméia)
* Geração dinâmica da imagem da etiqueta com texto formatado e QR Code
* Impressão direta para a impressora padrão do Windows usando Win32 API
* Visualização da etiqueta gerada antes da impressão (em modo de testes)

---

## Requisitos

* Python 3.8+
* PySide6
* Pillow (PIL)
* qrcode
* pywin32 (para impressão no Windows)

Instale as dependências com:

```bash
pip install PySide6 Pillow qrcode pywin32
```

---

## Como usar

1. Execute o script principal:

```bash
python nome_do_script.py
```

2. Na janela que abrir:

* Escolha o modo: **Normal** ou **Colméia**
* Selecione os valores para R, B, N
* Defina o intervalo para L (início e fim)
* Clique em **Imprimir** para gerar e enviar as etiquetas para a impressora padrão

O programa irá gerar e imprimir etiquetas para todos os valores no intervalo escolhido (de L início até L fim).

---

## Estrutura do Código

* `format_loc_code`: função que interpreta o código de localização conforme o modo
* `create_label_image`: gera a imagem da etiqueta (com texto e QR code)
* `print_image`: envia a imagem para impressão via API Windows
* `LabelWindow`: classe PySide6 com a interface gráfica e lógica de geração/impressão

---

## Personalização

* O estilo visual da interface é definido em `style.py` (arquivo `style_window`), onde você pode customizar o tema via QSS.
* Você pode ajustar tamanhos, fontes e posicionamento da etiqueta na função `create_label_image`.

---

## Observações

* Este projeto funciona apenas no Windows devido à dependência do Win32 para impressão.
* Para testar a imagem da etiqueta sem imprimir, pode-se usar `img.show()` no lugar da impressão.
* Certifique-se de que a impressora padrão esteja configurada corretamente no sistema.

---

## Licença

Projeto open source para uso pessoal e comercial. Sinta-se à vontade para contribuir ou adaptar conforme suas necessidades.

---

Se precisar de ajuda para adaptar, estender ou integrar este código, pode me chamar!
