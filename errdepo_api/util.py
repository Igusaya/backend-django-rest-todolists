from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
import markdown
import re

LEXERS = [item for item in get_all_lexers() if item[1]]
LANG_DICT = {} 
for item in LEXERS:
    LANG_DICT[item[0]]=item[1][0] 

def toMD(text, lang):
    """
    """
    # ```で括られた部分を取得
    arr_code_notation = re.findall('(```\n(.|\s)*?\n```)', text)

    # 行頭に空白4文字挿入 & ```削除したlist作成
    code_list = []
    replace_code_list = []
    for code in arr_code_notation:
        code_list.append(code[0])

        replace_code = code[0].replace('\n', '\n    ')
        replace_code = replace_code.replace('```','')
        replace_code_list.append(replace_code)

    # ```で括られた部分を置換
    i = 0
    while i < len(code_list):
        text = text.replace(code_list[i], replace_code_list[i])
        i += 1

    # MarkDown化
    md = markdown.Markdown()
    md_text = md.convert(text)

    # code要素の取り出し
    arr_code = re.findall('(<code(.|\s)*?</code>)',md_text)
    arr_unit_code = re.findall('<code.*</code>', md_text)
    
    # コードフォーマッターの作成
    if(lang not in LANG_DICT):
        # 登録外の言語の場合、癖のなさそうなTwigを設定
        lang = 'Twig'
    lexer = get_lexer_by_name(LANG_DICT[lang])
    formatter = HtmlFormatter(style='solarized-light', linenos='Table', full=False, noclasses=True)

    # code要素の置換 todo:複数行は今まで通り、単行は行番号非表示
    for code in arr_code:
        if code[0] in arr_unit_code:
            unit_format_code = code[0].replace('<code>','<code style="background-color: #fdf6e3;color: #657b83;">')
            md_text = md_text.replace(code[0],unit_format_code)
        else :
            format_code = '<div style="overflow: auto;">' + highlight(code[0][6:-7], lexer, formatter) + '</div>'
            print('\n--- format_code ---\n',format_code)
            # <div style="overflow: auto;"></div>
            md_text = md_text.replace(code[0],format_code)
    
    # preタグの除去
    md_text = md_text.replace('<pre>','')
    md_text = md_text.replace('</pre>','')
    return md_text

    