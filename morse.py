from Packages.consoleutil import choice_in_options, input, format_text, putchars, putnewline
try:
    from winsound import Beep
except:
    Beep = None
else:
    from time import sleep
MORSE_CODES_L = {
    'A': '.-',
    'Ä': '.-.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'Ö': '---.',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'Ş': '----',
    'T': '-',
    'U': '..-',
    'Ü': '..--',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    '.': '.-.-.-',
    ',': '--..--',
    '?': '..--..',
    ':': '---...',
    ';': '-.-.-.',
    '-': '-....-',
    '/': '-..-.',
    '"': '.-..--.',
    "'": '.----.',
    '(': '-.--.',
    ')': '-.--.-',
    '=': '-...-',
    '+': '.-.-.',
    '$': '...-..-',
    '¶': '.-.-..',
    '—': '..--.-'
}
MORSE_CODES_C = {k: v for v, k in MORSE_CODES_L.items()}
putchars("Morse Code Utility V0.0.1", newline=True)
while True:
    try:
        i = choice_in_options(['Query by Morse Code', 'Query by Letter', 'Translate Morse Code sentence', 'Convert sentence to Morse Code sentence', 'Exit'])
    except KeyboardInterrupt:
        break
    else:
        if i == 0:
            try:
                n = input('Code: ', filter=lambda k: k in '.-', min=1, max=7)
            except:
                putnewline()
                continue
            else:
                if n not in MORSE_CODES_C:
                    putchars(format_text('ERROR: ', fg='red', bold=True), 'Code not found', for_color=True, newline=True)
                else:
                    putchars(
                        '"',
                        format_text(n, fg='bright_white', bold=True),
                        '" means "',
                        format_text(MORSE_CODES_C[n], fg='bright_white', bold=True),
                        '"',
                        for_color=True,
                        newline=True
                    )
        elif i == 1:
            try:
                n = input('Letter: ', filter=lambda k: k.upper() in MORSE_CODES_L, min=1, max=1)
            except:
                putnewline()
                continue
            else:
                putchars(
                    '"',
                    format_text(n, fg='bright_white', bold=True),
                    '" means "',
                )
                if Beep is not None:
                    for i in MORSE_CODES_L[n.upper()]:
                        putchars(format_text(i, fg='bright_white', bold=True), for_color=True)
                        if i == '.':
                            Beep(3000, 100)
                            sleep(0.1)
                        elif i == '-':
                            Beep(3000, 300)
                else:
                    putchars(format_text(MORSE_CODES_L[n.upper()], fg='bright_white', bold=True), for_color=True)
                putchars('" in Morse Code.', newline=True)
        elif i == 2:
            try:
                putchars(format_text("Note: ", fg='bright_white', bold=True), 'Use 2 or more spaces in the sentence to refer a space in the translated sentence.', for_color=True, newline=True)
                n = input('Sentence  : ', filter=lambda k: k in '.- ', min=1)
            except:
                putnewline()
                continue
            else:
                words = ''
                for i in n.strip().split(' '):
                    if i == '':
                        if words[-1:] != ' ':
                            words += ' '
                    elif i not in MORSE_CODES_C:
                        putchars(format_text('ERROR: ', fg='red', bold=True), 'Code not found: "%s"' % format_text(i, rg='bright_write', bold=True), for_color=True, newline=True)
                    else:
                        words += MORSE_CODES_C[i]
                putchars('Translated: ', format_text(words, fg='bright_white', bold=True), for_color=True, newline=True)
        elif i == 3:
            try:
                n = input('Sentence  : ', filter=lambda k: k.upper() in tuple(MORSE_CODES_L) + (' ', ), min=1)
            except:
                putnewline()
                continue
            else:
                result = ''
                words = n.strip().split()
                for i in words:
                    for j in i:
                        result += MORSE_CODES_L[j.upper()]
                        result += ' '
                    result += ' '
                result = result.strip()
                if Beep is not None:
                    putchars('*Translated*: ')
                    for i in result:
                        putchars(format_text(i, fg='bright_white', bold=True), for_color=True)
                        if i == '.':
                            Beep(3000, 100)
                            sleep(0.1)
                        elif i == '-':
                            Beep(3000, 300)
                        elif i == ' ':
                            sleep(0.4)
                    sleep(0.1)
                    putnewline()
                else:
                    putchars('Translated: ', format_text(result, fg='bright_white', bold=True), for_color=True, newline=True)
        elif i == 4:
            break
