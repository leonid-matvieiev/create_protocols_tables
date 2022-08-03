0<1# :: ^
""" Со след строки bat-код до последнего :: и тройных кавычек
@setlocal enabledelayedexpansion & py -3 -x "%~f0" %*
@(IF !ERRORLEVEL! NEQ 0 echo ERRORLEVEL !ERRORLEVEL! & pause)
@exit /b !ERRORLEVEL! :: Со след строки py-код """

# print(dir())
ps_ = '__cached__' not in dir() or not __doc__

import re, os, sys
from time import localtime, sleep, strftime
from pathlib import Path
from json import dumps, loads
from pprint import pformat
from copy import deepcopy
# import pyexcel
import csv
from decimal import Decimal

XX = ''
import create_tables_mb
import create_tables_103
import create_tables_104
create_tables_mb.XX = XX
create_tables_103.XX = XX
create_tables_104.XX = XX
from create_tables_mb import create_rows_mb, create_htm_table_mb
from create_tables_103 import create_rows_103, create_htm_table_103
from create_tables_104 import create_rows_104, create_htm_table_104

# ============================================================================
debug = False  # True  #
mit_files_save = False  # True  #
ALL_DEVS = False  # True  #
ALL_FILDS = False  # True  #
DB_NAME = 'dbPCSapr'
DB_TABLE_TEMPLATE = '[%s].[dbo].[%%s]' % DB_NAME
DIR_TABLES = Path(r'tables')
specsyms = '?¶'
exe_7zip = r'"C:\Program Files\7-Zip\7z.exe"'

# language = 'Ru'
# alt_dev_names = {
#     'PC83AB3F1': {'Ru': 'PC83AB3F1', 'Ntr': 'HTP_B02F1'},
#     'PC83B3F1' : {'Ru': 'PC83B3F1' , 'Ntr': 'HTP_H02F1'},
#     'PC83BC3F1': {'Ru': 'PC83BC3F1', 'Ntr': 'HTP_B03F1'},
#     'PC83A3F1' : {'Ru': 'PC83A3F1' , 'Ntr': 'HTP_B01F1'},
# }

dev_code_names = {
    44: 'PC83-AB3      F1'.replace(' ', '').replace('-', ''),
    46: 'PC83-B3       F1'.replace(' ', '').replace('-', ''),
    47: 'PC83-BC3      F1'.replace(' ', '').replace('-', ''),
    51: 'PC83-A3       F1'.replace(' ', '').replace('-', ''),
#    48: 'Prj9Fx_CPU4x20  '.replace(' ', '').replace('-', ''),
}

need_tables_filds = {# Имена первого кортежа ключевые, второго - значения
    'tblBounds': (('typePrm',), ('uBoundPrm', 'lBoundPrm', 'stepPrm')),
    'tblType': (('typePrm',), ('typeBase', 'i', 'f', 'remTypePrm')),
    'tblFilds': (('typePrm', 'fildName',), ('fildType',
        'lehgthIX', 'formatIX', 'firstIX', 'npp', 'txtFild', 'remFild')),
}

need_dev_parts = {
    'GlobalState': ('Mems', 'vCurState', 'vAcce', 'vAPV', 'vAPV1'),
    'MapSetingsB': ('UST', ),
    'MapRamAIRx': ('vrIOAI_RX', ),
    'MapStatic': ('EROtherData', ),
}
'''
need_parts = {
    'MapRamPlatform': ('vDI', ),  # 'vIOBufurs',
    'MapEEPROM': ('EEPROM', ),
}
'''
# ----------------------------------------------------------------------------

# ============================================================================
def db_close():
    cursor.close()
    cnxn.close()
    print('Базу закрито %s-%02i-%02i %02i:%02i:%02i\n' % localtime()[:6])
# ----------------------------------------------------------------------------

# ============================================================================
def db_open():
    global cursor, cnxn
    import pyodbc
    cnxn = pyodbc.connect(
        r'DRIVER={SQL Server};'
        r'SERVER=WS_KBU\SQLEXPRESS;' +
        r'DATABASE=%s;' % DB_NAME +
        r'UID=pcs_reader;'
        r'PWD=123'
        , autocommit=True)
    # Create a cursor from the connection
    cursor = cnxn.cursor()
    print('Базу відкрито %s-%02i-%02i %02i:%02i:%02i' % localtime()[:6])
# ----------------------------------------------------------------------------

# ============================================================================
def table_from_db(tbl_name):
    """     Получение таблицы из базы
        На входе
    - tbl_name - имя таблицы
    - dev_code_names - условные номера устройств
        На выходе
    - список кортежей (списков) полей, в первом имена полей       """
    if ALL_FILDS:
        cols = set()
    if tbl_name == 'tblDevces':
        cols = {'idDev','nameDev','remDev','LCD_Lines',
                'LCD_LineLenth','defHomeConst','defHomeConstList'}
    else:
        cols = set(sum(need_tables_filds.get(tbl_name, ()), ()))

    sql_first = '''
    select name
      from syscolumns
      where id=OBJECT_ID('%s')
    ''' % (DB_TABLE_TEMPLATE % tbl_name)

    cursor.execute(sql_first)
    head = tuple(t[0] for t in cursor.fetchall()
                        if not cols or t[0] in (cols | {'idDev'}))

    sql_next = '''
    SELECT %s
      FROM %s
        ''' % (cols and ','.join(head) or '*',
                DB_TABLE_TEMPLATE % tbl_name)
    sql_where = []

    # Для tblDevces все устройства, для других интересующие
    if tbl_name != 'tblDevces' and not ALL_DEVS:
        sql_where.append("[idDev] IN(%s)" % ",".join(map(str, dev_code_names)))

    # Для tblFilds к тому же без задействий
    if tbl_name == 'tblFilds':
        sql_where.append("[lehgthIX] <> 0")

    if sql_where:
        sql_next += f'WHERE {" AND ".join(sql_where)}\n'
    cursor.execute(sql_next)

    return [list(row) for row in [head] + cursor.fetchall()]
# ----------------------------------------------------------------------------

# ============================================================================
def tables_from_db():
    db_open()
    tbls = {}
    for tbl_name in sorted(set(need_tables_filds) | {'tblDevces'}):
        print(end=f'{tbl_name} ...', flush=True)
        tbl = table_from_db(tbl_name)
        print(' таблицю сформовано')
        tbls[tbl_name] = tbl
    db_close()
    return tbls
# ----------------------------------------------------------------------------

# ============================================================================
def db_table_to_htm(tbl_name, tbl):
    """     Сохранение таблицы в файл
        На входе
    - tbl_name - имя таблицы
    - tbl - таблица - список кортежей (списков) полей, в первом имена полей
        На выходе - None и файл tbl_name в формате pprint   """

    db_table_htm = [f'''\
<!DOCTYPE html>
<HTML>
  <HEAD>
    <META charset="windows-1251">
    <TITLE>{tbl_name}</TITLE>
  </HEAD>
  <BODY>
    <TABLE cellspacing="0" cellpadding="2" border="1" align="center">''']
    for i, cels in enumerate(tbl):
        if i == 0:  # Шапка
            db_table_htm.append(f'<TR><TH>{"<TH>".join(cels)}')
            db_table_htm.append('<TR height=7>' + '<TD>' * len(cels))
            continue
        cels = map(lambda cel: str(float(cel)) if isinstance(cel, Decimal)
                            else str(cel), cels)
        db_table_htm.append(f'<TR><TD>{"<TD>".join(cels)}')
    db_table_htm.append('''\
    </TABLE>
  </BODY>
</HTML>''')
    return db_table_htm
# ----------------------------------------------------------------------------

# ============================================================================
def tables_to_7z(tbls):
    """     Сохранение таблиц в файлы
        На входе
    - tbls - таблицы - словарь (с именами таблиц в качестве ключей)
                списков кортежей (списков) полей (в первом имена полей)
        На выходе - None и файлы в формате pprint   """
    fpn7z = 'db_tables_xls.7z'
    print(end=f'{fpn7z} ...', flush=True)
    for tbl_name, tbl in tbls.items():
        db_table_htm = db_table_to_htm(tbl_name, tbl)
        Path(f'{tbl_name}.xls').write_text('\n'.join(db_table_htm), encoding='cp1251')
    if Path(f'.\\{fpn7z}').exists():
        os.system(f'del /Q .\\{fpn7z} > nul')
    k = os.system(f'{exe_7zip} a -mx5 -sdel -y .\\{fpn7z} %s > nul' %
                ' '.join(f'.\\{tbl_name}.xls' for tbl_name in tbls.keys()))
    if k:
        print(f' помилка {k} при створенні')
    else:
        print(' створено, записано')
# ----------------------------------------------------------------------------

# ============================================================================
def to_dev_tabless(tbls):

    devs_tmp = ', '.join(f'{dev}:{idDev}' for idDev, dev in dev_code_names.items())
    print(end=f'\tФормування словників для\n'
              f'пристроїв: {devs_tmp}\n'
              f'з таблиць:')
    dev_tabless = {}
    for table, col_names in need_tables_filds.items():
        print(end=f' {table},', flush=True)
        tbl = tbls[table]
        head = None
        dct = {}
        for cels in tbl:
            if not head:
                head = cels
                continue
            tmp = dict(zip(head, cels))
            if tmp['idDev'] not in dev_code_names:
                continue
            if len(col_names[1]) == 1:  # Значение единственное
                tmp2 = tmp[col_names[1][0]]  # так и будет значением
            else:  # Значений несколько
                tmp2 = {k: tmp[k] for k in col_names[1]}  # пакуем в словарь
            if len(col_names[0]) == 1:  # ключ один
                # добавляем в словарь idDev: table: ключ0: tmp2-Значение
                dev_tabless.setdefault(dev_code_names[tmp['idDev']], {}
                        ).setdefault(table, {}
                        )[tmp[col_names[0][0]]] = tmp2
            elif len(col_names[0]) == 2:
                # добавляем в словарь idDev: table: ключ0: ключ1: tmp2-Значение
                dev_tabless.setdefault(dev_code_names[tmp['idDev']], {}
                        ).setdefault(table, {}
                        ).setdefault(tmp[col_names[0][0]], {}
                        )[tmp[col_names[0][1]]] = tmp2
            else:
                raise Exception("Не передбачена кількість ключів")
    print()
    return dev_tabless
#-------------------------------------------------------------------------------

#===============================================================================
def tblFilds_addition(dev_tabless):

    print(end='\tДоповнення головних словників tblFilds\n'
                                            'пристроїв: ')
    for dev, dtbls in dev_tabless.items():
        print(end=f'{dev}  ')
        for typePrm, fildNames in dtbls['tblFilds'].items():
            for fildName, params in fildNames.items():
                del params['firstIX']  # всюди == 1
                if params['remFild'] is None:
                    del params['remFild']
                else:  # Удаление лишних пробелов из текстов
                    params['remFild'] = re.sub(r'\s+', ' ',
                                                params['remFild'].strip())
                params['txtFild'] = re.sub(r'\s+', ' ',
                                                params['txtFild'].strip())
                fildType = params['fildType']
                if fildType not in dtbls['tblType'] and fildType.lower(
                        ) in tuple(x.lower() for x in dtbls['tblType']):
                    # возможно в названии регистр букв не совпал, подгонка
                    print(f'\t{fildType} not in "tblType"')  # !!!
                    fildType = {x.lower(): x for x in dtbls['tblType']}[
                                                            fildType.lower()]
                if fildType in dtbls['tblType']:
                    # Получение и добавление размеров поля и дробной части
                    tmp = dtbls['tblType'][fildType]
                    if tmp['typeBase'] == 'bits':
                        params['size'] = tmp['i']
                    elif tmp['typeBase'] == 'list':
                        params['size'] = tmp['i']
                    elif tmp['typeBase'] == 'numeric':
                        if tmp['f']:
                            params['f'] = tmp['f']
                        params['size'] = tmp['i'] + tmp['f']
                    else:  # 'struct' 'map'
                        pass
                    params['typeBase'] = tmp['typeBase']

                if fildType not in dtbls['tblBounds'] and fildType.lower(
                        ) in tuple(x.lower() for x in dtbls['tblBounds']):
                    # возможно в названии регистр букв не совпал, подгонка
                    print(f'\t{fildType} not in "tblBounds"')  # !!!
                    fildType = {x.lower(): x for x in dtbls['tblBounds']}[
                                                            fildType.lower()]
                if fildType in dtbls['tblBounds']:
                    # Получение и добавление диаппазонов
                    tmp = dtbls['tblBounds'][fildType]
                    if params.get('f', 0):
                        params.update((k, float(v)) for k, v in tmp.items())
                    else:
                        params.update((k, int(v)) for k, v in tmp.items())
    print()
#-------------------------------------------------------------------------------

#===============================================================================
def expand_tblFilds(dev_tabless, need_dev_parts):  # 'MapSetingsB'  # 'GlobalState'

    # рекурс функция разворачивания вложеных структур
    def expand(dct_in, adr_in, type_in):
        dct_out = {}
        adr_out = adr_in
        for fildName, params in sorted(dct_in.items(),
                                        key=lambda x: x[1]['npp']):
            fildType = params['fildType']
            lst_tmp = []
            for i in range(params['lehgthIX']):
                size = -1
                dct_tmp = {XX: deepcopy(params)}
                del dct_tmp[XX]['formatIX']
                del dct_tmp[XX]['lehgthIX']
                if fildType not in typePrms and type_in == 'bits':
                    del dct_tmp[XX]['size']
                    del dct_tmp[XX]['uBoundPrm']
                    size = 0
                else:
                    del dct_tmp[XX]['npp']
                    dct_tmp[XX]['adr'] = adr_out
                    if fildType in typePrms:
                        dct, size = expand(typePrms[fildType], adr_out,
                                                        params['typeBase'])
                        dct_tmp.update(dct)
                        if params['typeBase'] == 'bits':
                            size = params['size']
#                    elif params['typeBase'] != 'struct':
#                    elif 'size' not in params:
#                        a=5
#                        pass
                    else:
                        size = params['size']
                    if params['typeBase'] == 'struct':
                        dct_tmp[XX]['size'] = size
#                if params['typeBase'] != 'list':
                del dct_tmp[XX]['fildType']
                if 'stepPrm' in params:
                    if params['stepPrm'] == 1:
                        del dct_tmp[XX]['stepPrm']
                    elif params['stepPrm'] < 1:
                        dct_tmp[XX]['stepPrm_prec'] = len(
                                    str(params['stepPrm']).split('.')[-1])
                if 'lBoundPrm' in params and params['lBoundPrm'] == 0:
                    del dct_tmp[XX]['lBoundPrm']
#                del dct_tmp[XX]['typeBase']
                adr_out += size
                if size < 0:
                    a=5
                lst_tmp.append(dct_tmp if len(dct_tmp) > 1 else dct_tmp[XX])
            dct_out[fildName] = lst_tmp if len(lst_tmp) > 1 else lst_tmp[0]
        return dct_out, adr_out - adr_in

    print(end='\tРозгортання головних словників tblFilds\nпристроїв: ')
    devs0 = {}
    for dev, dtbls in dev_tabless.items():
        print(end=f'{dev}  ', flush=True)
        devs0[dev] = {}
        for typePrm0, parts in need_dev_parts.items():
            adrMap = dtbls['tblType'][typePrm0]['i']  # Нач адрес памяти
            if adrMap < 0: adrMap = 0
            typePrms = dtbls['tblFilds']
            dctMap, sizeMap = expand(typePrms[typePrm0], adrMap, 'struct')
            devs0[dev].update({k: dctMap[k] for k in parts if k in dctMap})
    print()
    return devs0
#-------------------------------------------------------------------------------

# ============================================================================
def get_all_devs(devs0, dev_tabless):
    print('\tФормування остаточного словника пристроїв')
    devs = {}
    for dev, dev_dicts in devs0.items():
        if 'UST' in dev_dicts:
            dev_dicts['UST'] = {k: dev_dicts['UST'][k] for k in (XX, 'ToAI')}
        devs[dev] = dev_dicts
    return devs
#-------------------------------------------------------------------------------

# ============================================================================
def tables_to_py(tbls, fname='tbls.py'):
    print(end=f'{fname} ...', flush=True)
    txt_py = ('from decimal import Decimal\n'
                f'{fname.rsplit(".", 1)[0]} = ') + pformat(tbls)
    Path(fname).write_text(txt_py, encoding="utf8")
    print(' файл створено, записано')
#-------------------------------------------------------------------------------

# ============================================================================
def tables_to_json(tbls, fname):
    print(end=f'{fname} ...', flush=True)
    txt_json = dumps(tbls, indent=1, ensure_ascii=False, default=float)
#    txt_json0 = Path(fname).read_text(encoding="utf8")
#    if txt_json == txt_json0:
#        print(' файл не змінений')
#        return
    Path(fname).write_text(txt_json, encoding="utf8")
    print(' файл створено, записано')
#-------------------------------------------------------------------------------

# ============================================================================
def tables_from_json(fname):
    print(end=f'{fname} ...', flush=True)
    objs = loads(Path(fname).read_text(encoding="utf8"))
    print(' файл зчитано')
    return objs
#-------------------------------------------------------------------------------

# ============================================================================
def main():

    if debug and Path('devs.json').exists():
        devs = tables_from_json('devs.json')
    else:
        '''
        if debug and Path('tbls.json').exists():
            tbls = tables_from_json('tbls.json')
#            from tbls import tbls  # файл получается длиннее
        else:
            tbls = tables_from_db()
            if mit_files_save:
                tables_to_7z(tbls)
                tables_to_json(tbls, 'tbls.json')
#            tables_to_py(tbls, 'tbls.py')  # файл получается длиннее
        '''
        tbls = tables_from_db()
        dev_tabless = to_dev_tabless(tbls)
        tblFilds_addition(dev_tabless)
        devs = expand_tblFilds(dev_tabless, need_dev_parts)
        devs = get_all_devs(devs, dev_tabless)
        '''
        if mit_files_save:
            tables_to_json(devs, 'devs.json')
            sleep(1)
        '''
        tables_to_json(devs, 'devs.json')
        sleep(1)

    dt_rez = strftime('%Y-%m-%d_%H%M', localtime())

    with open('devs_ad_const.csv', 'r', encoding='cp1251') as fx:
        devs_ad_const = list(csv.DictReader(fx, delimiter=';'))

    # Создание всех необходимых файлов-таблиц для всех устройств
    for dev, dev_dict in devs.items():
        print(end=f'Архив ...', flush=True)

        fpn = f'{dev}_table'
        fpn_tmp2 = f'tmp2\\{fpn}'
        fpn_arx = f'{fpn}s_{dt_rez}_0.7z'

        if Path('tmp2').exists():
            os.system(r'rmdir /s /q tmp2 > nul')
        Path('tmp2').mkdir()

        rows_mb = create_rows_mb(dev, devs, devs_ad_const)
        rows_103, nots_ad_103 = create_rows_103(dev, devs, devs_ad_const)
        rows_104, nots_ad_104 = create_rows_104(dev, devs, devs_ad_const)

        create_files_mb(dev, rows_mb, fpn_tmp2)
        create_files_103(dev, rows_103, fpn_tmp2)
        create_files_104(dev, rows_104, fpn_tmp2)

#        break

        dev_7zs = sorted(Path().glob(f'{fpn}s_*.7z'))
        while dev_7zs:
            if Path('tmp1').exists():
                os.system(r'rmdir /s /q tmp1 > nul')
            k = os.system(rf'{exe_7zip} e -otmp1 {dev_7zs[-1]} > nul')
            fpnes1 = sorted(Path().glob(f'tmp1\\*.*'))
            fpnes2 = sorted(Path().glob(f'tmp2\\*.*'))
            if len(fpnes1) != len(fpnes2):
                dev_7zs = False  # Если состав разный,
                continue  # создаём новый архив с новой ДТ
            diff = 0
            for fp1, fp2 in zip(fpnes1, fpnes2):
                file_diff = fp1.read_bytes() != fp2.read_bytes()
                if fp1.suffix == '.htm':
                    diff += file_diff  # отличие в комментариях
                elif file_diff:
                    diff = -1  # отличие в рабочей таблице
                    break
            if not diff:
                print(f' {dev_7zs[-1]} без змін')
                break
            if diff < 0:
                # отличия в рабочих таблицах, создаём новый архив с новой ДТ
                dev_7zs = False
                continue
            # отличия в комментариях, создаём новый архив с старой ДТ
            stem, num_rem = dev_7zs[-1].stem.rsplit('_', 1)
            fpn_arx = f'{stem}_{int(num_rem) + 1}.7z'
            dev_7zs = False
            continue
        else:
            os.chdir('tmp2')
            k = os.system(f'{exe_7zip} a -mx5 -sdel -y '
                                    f'..\\{fpn_arx} {fpn}*.* > nul')
            if k:
                print(f' {fpn_arx}, помилка {k} при створенні')
            else:
                print(f' {fpn_arx} створено, записано')
            os.chdir('..')

        os.system(r'rmdir /s /q tmp2 > nul')
        if Path('tmp1').exists():
            os.system(r'rmdir /s /q tmp1 > nul')

        nots_ad_103 and print('\n'.join(nots_ad_103))
        nots_ad_104 and print('\n'.join(nots_ad_104))
#-------------------------------------------------------------------------------

strhex = lambda d: f"0x{d:02X}"
fformats = {
    'dec_tab.txt': ('\t', str),
    'hex_tab.txt': ('\t', strhex),
}

# ============================================================================
def create_files_104(dev, rows_104, fpn):
    sss_mb = [ds[:10] for ds in rows_104]
    for k, v in fformats.items():
        txt = '\n'.join(v[0].join(map(v[1], ss)) for ss in sss_mb)
        Path(fpn + f'_104_{k}').write_text(txt, encoding='cp1251')
    htm_table_104 = create_htm_table_104(dev, rows_104, 6)
    Path(fpn + '_104.htm').write_text('\n'.join(htm_table_104),encoding='utf8')
    htm_table_104 = create_htm_table_104(dev, rows_104, 13)
    Path(fpn + '_104+.htm').write_text('\n'.join(htm_table_104),encoding='utf8')
#-------------------------------------------------------------------------------

# ============================================================================
def create_files_103(dev, rows_103, fpn):
    sss_mb = [ds[:8] for ds in rows_103]
    for k, v in fformats.items():
        txt = '\n'.join(v[0].join(map(v[1], ss)) for ss in sss_mb)
        Path(fpn + f'_103_{k}').write_text(txt, encoding='cp1251')
    htm_table_103 = create_htm_table_103(dev, rows_103, 4)
    Path(fpn + '_103.htm').write_text('\n'.join(htm_table_103),encoding='utf8')
    htm_table_103 = create_htm_table_103(dev, rows_103, 11)
    Path(fpn + '_103+.htm').write_text('\n'.join(htm_table_103),encoding='utf8')
#-------------------------------------------------------------------------------

# ============================================================================
def create_files_mb(dev, rows_mb, fpn):
    sss_mb = [ds[:8] for ds in rows_mb]
    for k, v in fformats.items():
        txt = '\n'.join(v[0].join(map(v[1], ss)) for ss in sss_mb)
        Path(fpn + f'_mb_{k}').write_text(txt, encoding='cp1251')

#    for t in ('dec', 'hex'):
##        pyexcel.save_as(array=sss_mb, dest_file_name=fpn + f'_mb_{t}.xls',
##                                dest_sheet_name='Лист 1')
##        pyexcel.save_as(array=sss_mb, dest_file_name=fpn + f'_mb_{t}.xlsx',
##                                dest_sheet_name='Лист 1')
##        pyexcel.save_as(array=sss_mb, dest_file_name=fpn + f'_mb_{t}_def.csv',
##                                dest_encoding='cp1251')
##        pyexcel.save_as(array=sss_mb, dest_file_name=fpn + f'_mb_{t}_sem.csv',
##                                dest_encoding='cp1251', dest_delimiter=';')
##        pyexcel.save_as(array=sss_mb, dest_file_name=fpn + f'_mb_{t}_tab.csv',
##                                dest_encoding='cp1251', dest_delimiter='\t')
#        txt = '\n'.join('\t'.join(map(str, ss)) for ss in sss_mb)
#        Path(fpn + f'_mb_{t}_tab.txt').write_text(txt, encoding='cp1251')
#        break
#        sss_mb = [[f"'{d:02X}" for d in ds[:8]] for ds in rows_mb]

    htm_table_mb = create_htm_table_mb(dev, rows_mb, 5)
    Path(fpn + '_mb.htm').write_text('\n'.join(htm_table_mb), encoding='cp1251')
    htm_table_mb = create_htm_table_mb(dev, rows_mb, 10)
    Path(fpn + '_mb+.htm').write_text('\n'.join(htm_table_mb), encoding='cp1251')
##    with open(fpne, 'w', encoding="cp1251") as fp:
##        fp.write('\n'.join(htm_table_mb))
#-------------------------------------------------------------------------------

# ============================================================================
if __name__ == '__main__':
    if 'debug' in [arg.lower() for arg in sys.argv[1:]]:
        debug = True
    elif not ps_:
        debug = False

    main()

    if not (ps_ or '--waitendno' in sys.argv):
        os.system('timeout /t 60')
# ----------------------------------------------------------------------------

"""   ???  Признаки типов структур
- Наличие fildType, uBoundPr, adr, sbm без ХХ - список
- Наличие adr, sb без uBoundPrm в ХХ - битовая переменная/структура
- Наличие fildType, npp без ХХ, adr и т.п. - бит битовой переменной
- Наличие f, adr, sb, uBoundPrm, возможно lBoundPrm, stepPrm без ХХ - число
- Наличие adr, nb в ХХ без остального - структура
- Наличие adr, nb, uBoundPrm, возможно lBoundPrm без ХХ, sb и т.п. - байтмассив
"""
# ----------------------------------------------------------------------------

'''
DIR_DICTS = Path(r'dicts')
if not DIR_DICTS.exists():
    DIR_DICTS.mkdir()

    for dev, dev_dicts in devs.items():
        fpne = DIR_DICTS / (f'map_{dev}' + '.json')
        print(end=f'Файл {fpne.name} ... ', flush=True)
        txt_xml = dumps(dev_dicts, indent=2, ensure_ascii=False)
        fpne.write_text(txt_xml, encoding='utf8')
        print('створено, записано')

        fpne = DIR_DICTS / (f'map_{dev}' + '.xml')
        print(end=f'Файл {fpne.name} ... ', flush=True)
        txt_xml = dict2xml(dev_dicts, wrap=dev)
        fpne.write_text(txt_xml, encoding='utf8')
        print('створено, записано')
'''
#-------------------------------------------------------------------------------
