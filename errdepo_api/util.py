from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
import markdown
import re

LEXERS = [item for item in get_all_lexers() if item[1]]
LANG_DICT = {} 
for item in LEXERS:
    LANG_DICT[item[0]]=item[1][0] 

def toMD(text, lang='typescript'):
    """
    """
    print(LANG_DICT['JavaScript+Django/Jinja'])
    # MarcDown化
    md = markdown.Markdown()
    md_text = md.convert(text)

    # code要素の取り出し
    arr_code = re.findall('(<code(.|\s)*?</code>)',md_text)
    arr_unit_code = re.findall('<code.*</code>', md_text)
    
    # コードフォーマッターの作成
    lexer = get_lexer_by_name(LANG_DICT[lang])
    formatter = HtmlFormatter(style='solarized-light', linenos='table', full=False, noclasses=True)

    # code要素の置換 todo:複数行は今まで通り、単行は行番号非表示
    for code in arr_code:
        print(code[0])
        if code[0] in arr_unit_code:
            unit_format_code = code[0].replace('<code>','<code style="background-color: #fdf6e3;color: #657b83;">')
            md_text = md_text.replace(code[0],unit_format_code)
        else :
            format_code = highlight(code[0][6:-7], lexer, formatter)
            md_text = md_text.replace(code[0],format_code)
    
    return md_text

    