from GVector import *
from GVector_dict import *  # если словарь пустой для импорта
from bottle import Bottle, static_file, run, route, template, request  # , get, post
import re

strn = '_Tib_Txt.txt'

def input_strn(data=strn):
    global strn
    print("input_strn run")
    if '.txt' in data:
        with open(data, 'r', encoding='utf-8') as f:
            strn = f.read()
    elif '་' in data:
        strn = data
    else:
        print('введите тибетский текст')
        #strn=input()
    return strn

def format_txt(strn):
    print("format_txt run")
    strn += ' '

    strn = re.sub(f'༌', '་', strn, 0)

    #0.Предложение ч1
    strn = re.sub(f'([༄༅\s\n\t༈།]*)(\S*[༔།/s]*)', '\\1@\\2&', strn, 0)
    strn = re.sub(f'@&', '', strn, 0)

    # 0.1. Название
    strn = re.sub(r'([༄༅།\s@]+\S+?ལས[།༔]&)\s+(\S+?་བཞུགས\S*[།༔]*&)',
                  '<h1 class="Toc">\\1 \\2</h1> <br>\\n', strn, 0)

    # 0.2. Тема - подзаголовок
    strn = re.sub(
        r'(\S+?ནི[།༔]&)', '\\n<br><h4 class="Topic">\\1</h4> <br>\\n', strn, 0)

    # 0.3. Новая глава
    strn = re.sub(r'(༈)', '\\n\\n<br><br>\\1', strn)

    # 0.4. Цитата до первого окончания
    strn = re.sub(r'([།])@(\S+?ལས[༔།]+)&\s+(.+?[༔།་]*)\s([།]([@]ཞེས|ཅེས).+?[༔།&]+)',
                  '\\n<br><snt class=\"cite_src\">\\1\\2</snt> <div class=\"cite\">\\3</div> <br>\\n\\4<br>\\n', strn, 0)

    # 0.4. Цитата продолжение
    strn = re.sub(r'([།]@(ཞེས|ཅེས).+?དང[༔།་]*&)(<br>\n)*\s*(.+?[༔།་&]*)\s([།]@(ཞེས|ཅེས).+?[༔།&]+)',
                  '</div>\\1 <div class="cite">\\4</div> <br>\\n\\5<br>\\n', strn, 0)

    #0.5 Конец абзаца (заключающий помощник གོ ངོ དོ ནོ བོ མོ རོ ལོ སོ ཏོ после второго суффикса ད་; འོ་ - после слога без суффикса)
    strn = re.sub(
        f'((ག་གོ|ང་ངོ[་]*|ད་དོ|ན་ནོ|བ་བོ|མ་མོ|ར་རོ|ལ་ལོ|ས་སོ|ད་ཏོ|འོ)([༔།{1,2}&\s\t])+)[།\s]', '\\1<br><br>\\n\\n ', strn)
    strn = re.sub(
        f'(ག་གོ|ང་ངོ[་]*|ད་དོ|ན་ནོ|བ་བོ|མ་མོ|ར་རོ|ལ་ལོ|ས་སོ|ད་ཏོ)([༔།&\s\t])', '\\1#\\2', strn)
    strn = re.sub(f'(འོ)([༔།&\s\t])', '་\\1#\\2', strn)

    #  \\1-приставка    \\2-корневая         \\3-1й суффикс      \\4-2й суфф
    # ([ག|བ|ད|མ|འ]?)([\w+?ཱཱཱིིུུྲྀཷླྀཹེཻོཽཾཱྀྀྂྃྐྑྒྒྷྔྕྖྗྙྚྛྜྜྷྞྟྠྡྡྷྣྤྥྦྦྷྨྩྪྫྫྷྭྮྯྰྱྲླྴྵྶྷྸྐྵྺྻྼ]+?)([ག|ང|ད|ན|བ|མ|འ|ར|ལ|ས]?)([ས|ད]?)

    #0.6 Разделительные частицы - не выполняем
    #strn=re.sub(f'(་)(གི|ཀྱི|གྱི|ཡི|གིས|ཀྱིས|གྱིས|ཡིས|སུ|རུ|ཏུ|ན|ལ|དུ|ཏེ|དེ|སྟེ|དང|ཞིང|ཅིང|ཤིང|ཀྱང|ཡང)([་།༔&])', '\\1<a class="cc">\\2</a>\\3',strn)
    #strn=re.sub(f'(འི|འིས|འང|འམ)|འང([་།༔&])', '<a class="cc">\\1\\2</a>',strn)

    #0.7 Предложение ч2
    lst = strn.split('@')

    strng = ''
    strng = lst[0]
    i = 1
    while i in range(len(lst)):
        strng += f'<snt class="sent" id="s{i}">{lst[i]}'
        i += 1

    strn = strng.replace('&', '</snt>')
    strn = re.sub(r'@(.+?)&', f'<snt class="sent" id="{i}">\\1</snt>', strn, 0)

    #print(strn)
    return strn

def cut_particle(strn):
    print("cut_particle run")
    #1. отлепляем ->འི от слога
    for syl in ['འིས', 'འང', 'འམ', 'འུ', 'འི']:  # исключил доп.строк - 'འུ'
        strn = re.sub(f'([་\S])({syl})([་།༔])', r"\1་\2\3", strn)

    # ПРАВИЛО: в слоге, состоящем из двух букв, при отсутствие надписных, подписных и огласовок
    # 1я буква считается корневой, а 2я суффиксом.
    # Чтобы 2я буква превратилась в корневую, её необходимо завершить суффиксом འ་, который не читается
    # и замещается འི
    # отлепляем འི заменяя его на འ
    for word in ['གཉ', 'གཏ', 'གད', 'གན', 'གཞ', 'གཟ', 'གཡ', 'གཤ', 'དཀ', 'དག', 'དགེ', 'དཔ', 'དབ', 'དམ', 'བཀ',
                 'བཅ', 'བད', 'བཙ', 'བཟ', 'བརྡ', 'བཤ', 'མཀ', 'མཁ', 'མག', 'མང', 'མཐ', 'མད', 'མན', 'མཛ', 'མཟ',
                 'འག', 'འཆ', 'འཇ', 'འད', 'འབ', 'འཛ']:
        strn = re.sub(f'({word})(་འི)', r"\1འ\2", strn)

    strn = re.sub(f'([་\S])(མོ|པ|པོ|བོ|དེ|འདི)(ར)', r"\1\2་\3", strn)
    strn = re.sub(f'([>་?])(པ|པོ|བ|བོ|ཏེ|དེ|འདི)(ས་)', r"\1\2་\3", strn)

    #print(strn)
    return strn

def Dict_DB_load():
    print('Dict_DB_load')
    pathSave = "C:/DICT_SCRIPT/"  # путь к локальным файлам основной программы словаря
    #pathSave="/MainYagpoOCR/RETREAT/DICT_SCRIPT/"   #путь к локальным файлам основной программы словаря

    pUnionData = pathSave+"XML_DICT/_LotsavaUnion.txt"
    pUnionIndex = pathSave+"XML_DICT/_LotsavaUnionIndex.txt"

    # путь к подключаемым словарям (техт)
    pDictData = pathSave+"XML_DICT/MAIN_DICT_TAB/"

    pDictTranslMemoData = pathSave + \
        "XML_DICT/Memo_Translate_Dict/Lotsava_MemoTranslate.txt"  # словарь памяти переводов

    #открываем файлы базы данных основного словаря
    print("init Union dictionary")
    v = GVector()
    # объединенный словарь _LotsavaUnion.txt пишем в бинарн файл строк переменной длины
    v.openData(pUnionData)

    dbU = dictBase()
    # noSQL база,  ключи объединенного словаря _LotsavaUnionIndex.txt
    dbU.openData(v, pUnionIndex)

    #если словарь пустой, импортируем текстовые файлы словаря в базу данных
    if(dbU.dictSize == 0):
        print("From MAIN_DICT_TAB import All dictionary in Union dictionary")
        print(dbU.dictSize)
        loadDB(dbU, pDictData)
    return dbU

def find_phrase(strn):
    print("find_phrase run")
    #phrase=strn_lst[0]
    #res_strn
    res_dct = {}
    not_in_dict = []

    # взяли в список все предложения
    strn_lst = re.findall(f'\d+\">(\S+?)་?[<#༔།\s]', strn)
    #print(strn_lst)

    dbU = Dict_DB_load()

    for sentence in strn_lst:
        #print(sentence)
        phrase = sentence
        while phrase != '':  # '་' in phrase:
            value = dbU.get(phrase)
            if value != '':  # НАШЛИ. отрезаем найденную фразу с начала предлож
                #print("prh ",phrase)
                #print("val - ", value)  # REPORT
                # заменили в тексте
                #strn=re.sub(f'([་།༽༼ ༿\s>]+)({str(phrase)})([་༽༈།༔༾\s<]+)', r'\1|\3', strn)
                #'སྐྱེས་བུ:|:nnn, личность:|:YP'
                if phrase not in res_dct:  # если нет в словаре, записываем фраза : значение
                    res_dct[phrase] = str(value).split(':|:')[1].split(', ')
                # отрезаем найденную фразу с начала предлож
                sentence = re.sub(f'^({phrase}[་]*)', '', sentence)
                phrase = sentence   # уменьшенное на найденную фразу предложение

            else:   # НЕ НАШЛИ фразу
                if '་' not in phrase:  # если последний слог во фразе отрезаем ненайденную фразу с начала предлож
                    sentence = re.sub(f'^({phrase}[་]*)', '', sentence)
                    not_in_dict.append(phrase+'\txxx, \n')
                    phrase = sentence
                else:   # уменьшаем фразу, отрезая слог с конца
                    #print("prh ",phrase)
                    phrase = phrase.split('་')
                    phrase = "་".join(phrase[0:-1])

    #print(not_in_dict)
    #with open(new_Words_Dict, 'a+', encoding='utf-8') as wf:
    #    wf.write(''.join(set(not_in_dict)))

    return strn, res_dct

def bracket_res_strn(strn, res_dct):
    print("bracket_res_strn run")
    res_strn = strn
    #lst=list(dict.fromkeys(re.findall(r'_\d+_(\S+?)\]', res_strn)))
    #В.Поиск по strn каждого уник из sent_lst в строке
    for key in sorted(res_dct, key=len, reverse=True):
        # из исход строки убираем найденное sent
        #print(key)
        strn = re.sub(
            f'([་།༽༼ ༿\s>]+)({str(key)})([་༽༈།༔༾\s<]+)', r'\1|\3', strn)

        k = str(key).replace('་', '_')
        # в дубль_строке заменяем sent
        res_strn = re.sub(
            f'([་།༽༼\s༿>]+)({str(key)})([་༽༈།༔༾\s<]+)', f'\\1[{k}]\\3', res_strn, 0, re.MULTILINE)
        #res_strn=re.sub(f'([་།༽༼\s༿>]+)({str(key)})', '\\1[\\2]', res_strn, 0, re.MULTILINE) #в дубль_строке заменяем sent
        #print ("res_strn1:   ", res_strn)
    res_strn = res_strn.replace('_', '་')
    #print ("strn:   ", strn)
    #print ("res_strn2:   ", res_strn)
    return res_strn

def join_particles(res_strn):
    print("join_particles")
    # Присоединяем оторванные частицы обратно
    res_strn = re.sub(f'((མོ|པ|པོ|བ|བོ|དེ|འདི)\])་(\[ར\])', r'\1\3', res_strn)
    res_strn = re.sub(f'((པ|པོ|བ|བོ|ཏེ|དེ|འདི)\])་(\[ས\])', r'\1\3', res_strn)

    for syl in ['འིས', 'འང', 'འམ', 'འི', 'འུ']:
        res_strn = re.sub(f'་(\[?{syl}\]?)', r"\1", res_strn)

    res_strn = re.sub(f'(གོ|ངོ[་]*|དོ|ནོ|བོ|མོ|རོ|ལོ|སོ|ཏོ)#',
                      '<a def="¶" class="cc">\\1</a>', res_strn)
    res_strn = re.sub(f'་(འོ)#', '<a def="¶" class="cc">\\1</a>', res_strn)
    res_strn = res_strn.replace('#', '')

    #print ('strn:  ',strn)
    #print ('res_strn2:  ', res_strn)
    #print(*res_dct.items(), sep="\n")
    #print('res_dct', res_dct)

    return res_strn

def count_word_dict(res_strn):
    print("count_word_dict")
    # замена/уборка вложенных скобок
    res_strn = re.sub(
        f'(\[)([\w+?ཱཱཱིིུུྲྀཷླྀཹེཻོཽཾཱྀྀྂྃྐྑྒྒྷྔྕྖྗྙྚྛྜྜྷྞྟྠྡྡྷྣྤྥྦྦྷྨྩྪྫྫྷྭྮྯྰྱྲླྴྵྶྷྸྐྵྺྻྼ་]+)(\[)', '[\\2', res_strn, 0)

    res_strn = re.sub(
        f'(\])([་\w+?ཱཱཱིིུུྲྀཷླྀཹེཻོཽཾཱྀྀྂྃྐྑྒྒྷྔྕྖྗྙྚྛྜྜྷྞྟྠྡྡྷྣྤྥྦྦྷྨྩྪྫྫྷྭྮྯྰྱྲླྴྵྶྷྸྐྵྺྻྼ]+)(\])', '\\2]', res_strn, 0)

    cont_ = 1

    # исходная строка
    #res_strn

    # старая подстрока - заменяемая часть строки
    subStrOld = '['

    # длина старой подстроки
    lenStrOld = len(subStrOld)

    # Функция find() возвращает индекс первого символа
    # подстроки. Если подстроки нет, то возвращает -1.
    # Цикл используется на случай, если в строке
    # несколько одинаковых подстрок.
    while cont_ < res_strn.find(subStrOld):
        # новая подстрока
        subStrNew = '_'+str(cont_)+'_'
        # сохранить в переменную индекс первого элемента
        # старой подстроки
        i = res_strn.find(subStrOld)
        # Перезаписать строку: взять срез от начала до индекса,
        # добавить новую подстроки и соединить со срезом от конца
        # старой подстроки.
        res_strn = res_strn[:i] + subStrNew + res_strn[i+lenStrOld:]
        cont_ += 1

    #res_strn=re.sub(f'(\d+)({k})\]',
    #print(res_strn)
    return res_strn

def res_strn_dct_html(res_strn, res_dct):
    print("res_strn_dct_html")
    res_dct_html = ""
    #print(res_strn)
    #lst=list(dict.fromkeys(re.findall(r'_\d+_(\S+?)\]', res_strn)))
    lst = re.findall(r'_\d+_(\S+?)\]', res_strn)
    #print(lst)
    cnt = 1
    for ind, k in enumerate(lst):  # идем по строке
        #print(lst[ind])
        #part_speech='na'
        #print("1111 ", k)
        #print("222 ", res_dct[k])
        #if res_dct[k][0][0:2] == 'cc':
        #    part_speech='cc'
        # создаем тэги для строки
        #res_strn=res_strn.replace(f'[{k}]', f'<a id="{cnt}" def="{res_dct[k]}" class="{part_speech}" href="#h{cnt}">{k}</a>')
        res_strn = re.sub(
            f'_(\d+)_({k})\]', f'<a id="\\1_{k}" def="{res_dct[k][1]}" class="{res_dct[k][0]}" href="#h_{k}">{k}</a>', res_strn, 0)
        # собираем опции для списка значений
        add = ""
        num = 1
        for itm in res_dct[k]:
            add += f'<div class="option" id="o{num}"><div class="vote_line" style="width: 57%;"></div>{itm}</div>'
            num += 1

        #создаем тэги для словарика
        # завернуть в тиб тег
        res_dct_html += f'<a href="#" id="h_{k}">{add}</a>\n'
        cnt += 1

    #print(res_strn)
    #print(dct_str)
    #  འ заменяя его на འི
    for word in ['གཉ', 'གཏ', 'གད', 'གན', 'གཞ', 'གཟ', 'གཡ', 'གཤ', 'དཀ', 'དག', 'དགེ', 'དཔ', 'དབ', 'དམ', 'བཀ',
                 'བཅ', 'བད', 'བཙ', 'བཟ', 'བརྡ', 'བཤ', 'མཀ', 'མཁ', 'མག', 'མང', 'མཐ', 'མད', 'མན', 'མཛ', 'མཟ',
                 'འག', 'འཆ', 'འཇ', 'འད', 'འབ', 'འཛ']:
        res_strn_html = re.sub(f'({word})འ(<.*>འི)', r"\1\2", res_strn)

    return res_strn_html, res_dct_html

def save_html_result(res_strn_html, res_dct_html):
    print("save_html_result")
    with open('!_JS_lotsawa11.html', 'r', encoding='utf-8') as f:
        res_html = f.read()

        #пишем тэги для строки
        res_html = re.sub(r'<section lang="bo" id="Result">\n([\s\S]*?)</section>',
                          f'<section lang="bo" id="Result">\n{res_strn_html}\n</section>', res_html)
        #пишем тэги для словарика
        res_html = re.sub(r'<section id="Slovar" class="Dict">\n([\s\S]*?)</section>',
                          f'<section id="Slovar" class="Dict">\n{res_dct_html}</section>', res_html)

    with open('!_JS_lotsawa11.html', 'w', encoding='utf-8') as wf:
        wf.write(res_html)

app = Bottle(__name__)

# Static CSS Files
@app.route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/css')

'''@app.route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root=config.STATIC_PATH)
    '''
@app.route('/')
def result():
    # strn = input_strn('_Tib_Txt.txt')
    #strn = format_txt(strn)
    #strn = cut_particle(strn)
    #strn, res_dct = find_phrase(strn)
    #res_strn = bracket_res_strn(strn, res_dct)
    #res_strn = join_particles(res_strn)
    #res_strn = count_word_dict(res_strn)
    #res_strn_html, res_dct_html = res_strn_dct_html(res_strn, res_dct)
    #save_html_result(res_strn_html, res_dct_html)
    print("Lotsawa finished")
    return template('!_JS_lotsawa13') #render_template('!_JS_lotsawa11.html', title='Result')


@app.route('/getwrd')  # , methods    =['POST', 'GET'])  # DONE
def getwrd():
    tib = request.query.key
    dbU = Dict_DB_load()
    val = dbU.get(tib)
    return template('{{tib}} {{val}}', tib=tib, val=val)

@app.route('/prs2txt')#, methods    =['POST', 'GET'])  # DONE
def prs2txt():
    tib = request.query.key
    #print(tib)
    rus = request.query.ru
    rewrite = bool(request.query.rw)
    dbU = Dict_DB_load()
    #print(rewrite)
    if rewrite:
        #print('rw')
        dbU.rem(tib)
        if dbU.has_key(tib) < 0:
            print('add')
            dbU.add(tib, rus)
    else:
        #print('++')
        val = dbU.get(tib)
        dbU.put(tib, val + '; ' + rus)
        #print(val)
    dbU.saveInd()
    val=dbU.get(tib)
    print(val)
    path = 'XML_DICT/MAIN_DICT_TAB/00_NW.txt'
    with open(path, 'a+', encoding='utf-8') as wf:
        if rus[:3] in list(['adj', 'avd', 'avi', 'avm', 'avp', 'avt', 'clc', 'cag', 'cld', 'css', 'ccp', 'clc', \
        'cgn', 'clc', 'cnr', 'cld', 'clc', 'cfs', 'cqt', 'clc', 'cag', 'cld', 'cnr', 'css', 'clc', 'cfn', 'cgn', \
        'cim', 'clc', 'qst', 'csf', 'cld', 'det', 'dmf', 'dpl', 'uhh', 'nnn', 'nnn', 'nnn', 'nnn', 'nnn', 'nvf', \
        'nvi', 'nvn', 'nvd', 'nvc', 'num', 'num', 'num', 'num', 'prn', 'itr', 'prn', 'prn', 'vft', 'vim', 'vrb', \
        'vng', 'vps', 'vpr']): wf.write(tib + '\t' + rus + '\n')
        else: wf.write(tib + '\txxx, ' + rus + '\n')
    # tib, rus  # jsonify(key=tib, ru=rus) vals=list_vals
    # template('<div>{{tib}} {{val}}</div>', tib=tib, val=val)
    return template('{{tib}} {{val}}', tib=tib, val=val)

@app.route('/snt2txt')  # 
def snt2txt():
    sent_id = request.query.s_id
    tib_snt = request.query.s_tb
    rus_trv = request.query.s_ru
    with open('Transl_Bo_Ru.txt', 'a+', encoding='utf-8') as wf:
        wf.write(sent_id + '\t' + tib_snt + '\t' + rus_trv + '\n')
    return sent_id, tib_snt, rus_trv  # jsonify(result=sent_str)

if __name__ == '__main__':
    run(app, host='localhost', port=4445, debug=True)


