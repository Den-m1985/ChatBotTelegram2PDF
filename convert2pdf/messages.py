ANSWER_MESSAGE = '''Основные команды:
/start - Приветствие
/help - Список поддерживаемых конверсий, подсказки по использованию бота
/info - Пояснения о работе бота'''

HELP_MESSAGE = '''Список поддерживаемых конверсий:
Поддерживаемые кодировки текста: ANSI, UTF-8
* .txt -> .pdf
* .csv -> .pdf

Поддерживаемые форматы фото:
* .jpg -> .pdf
* .png -> .pdf
* .tiff -> .pdf
* .jpeg -> .pdf
* .jp2(JPEG2000) -> .pdf
* .heif -> .pdf
* .heic -> .pdf

Поддерживаемые форматы документов:
* .doc -> .pdf
* .docx -> .pdf
* .odt -> .pdf
* .xls -> .pdf
* .xlsx -> .pdf
* .ods -> .pdf
'''

START_MESSAGE = '''Этот бот конвертирует файлы с различными расширениями в pdf.\n
Чтобы посмотреть список поддерживаемых конверсий используйте /help'''

INFO_MESSAGE = '''converToPDF - это некоммерческий проект.
Создан исключительно на энтузиазме и любви к разработке.\n
Бот принимает файл, конвертирует его в PDF и отправляет обратно пользователю.
После чего удаляет ваш файл с сервера и очищает директорию.
Мы уважаем конфиденциальность информации пользователей и поддерживаем политику telegram в отношении приватности.\n
Если вам нравится converToPDF, то вы можете поддержать нашу команду (:
Купить нам кофе с печеньками можно на https://boosty.to/convertopdf
Мы сделали этот проект для вас и для наших друзей и близких! Приятного использования 😇
Avatar by César Castro on dribbble
https://dribbble.com/shots/18423562-Love-Death-Robots-K-VRC'''

CONVERT_MESSAGE = 'Конвертирую, это может занять некоторое время ⚙️⚙'

UNSUPPORTED_MESSAGE = '''Конверсия этого формата не поддерживается 😇\n
/help - поддерживаемые форматы'''

HTML_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="$enc">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
'''

HTML_TAIL = '''
</body>
</html>
'''