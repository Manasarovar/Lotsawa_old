from GVector import *
from GVector_dict import *  # если словарь пустой для импорта
from bottle import Bottle, static_file, run, route, template, request  # , get, post

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

app = Bottle(__name__)

# Static CSS Files
@app.route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/css')

@app.route('/')
def result():
    return template('!_JS_lotsawa13') 


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


