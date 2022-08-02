from pprint import pprint
from copy import deepcopy

# ============================================================================
def create_rows_104(dev, all_devs, devs_ad_const):
    global content_104, table_AD_103, table_AD_104
    dev_dict = deepcopy(all_devs[dev])

    table_AD_103 = []
    table_AD_104 = []
    for dct in devs_ad_const:
        if dct['103\n'+dev[4:]]:
            ts = [dct[k] for k in ('103\n'+dev[4:],'path','103\nnorm','txt')]
            ts[0] = int(ts[0])
            ts[2] = ','in ts[2]and float(ts[2].replace(',','.'))or int(ts[2])
            table_AD_103.append(ts)
        if dct['104\n'+dev[4:]]:
            ts = [dct[k] for k in ('104\n'+dev[4:],'path','104\ndivmul','txt')]
            ts[0] = int(ts[0])
            table_AD_104.append(ts)
    table_AD_103.sort()
    table_AD_104.sort()

    content_104 = []
    rows_104 = []
    adr_AI_RX_begin = dev_dict["vrIOAI_RX"][XX]["adr"]
    line_104 = 0

    # --------------------------------------------------------------------------
    lines_104 = 0

    # DI
    adr_104 = 0xA0
    dict_bits = deepcopy(dev_dict["vCurState"]["DIs"])
    adr_104, rows = get_bits_table_104_3_maps(dict_bits,
                                adr_104, 0, 0x83, "Состояние DI")
    rows_104 += rows
    lines_104 += len(rows)

    # KLs
    dict_bits = deepcopy(dev_dict["vCurState"]["KLs"])
    adr_104, rows = get_bits_table_104_3_maps(dict_bits,
                                adr_104, 0, 0x83, "Состояние KL")
    rows_104 += rows
    lines_104 += len(rows)

    rows_104.append(separ_104)
    content_104.append([len(content_104), line_104, lines_104, 10])
    line_104 += lines_104 + 1

    # --------------------------------------------------------------------------
    lines_104 = 0

    # Телеуправление реле
    adr_104 = 0xC8
    adr_104, rows = get_codes_table_104_3_opis('ТУ на откл KL',
                                adr_104, 0, 0x42, 0xF6, 0, 40)
    rows_104 += rows
    lines_104 += len(rows)

    rows_104.append(separ_104)
    content_104.append([len(content_104), line_104, lines_104, 10])
    line_104 += lines_104 + 1

    # --------------------------------------------------------------------------
    lines_104 = 0

    # Квитирование и пуск осциллографа по ТУ
    adr_104 = 0x13
    adr_104, rows = get_codes_table_104_3_opis(['Квит по ТУ'],
                                adr_104, 0, 0x42, 0xF9, 1)
    rows_104 += rows
    lines_104 += len(rows)

    # пуск осциллографа по ТУ
    adr_104, rows = get_codes_table_104_3_opis(['Пуск осц по ТУ'],
                                adr_104, 0, 0x42, 0xF9, 2)
    rows_104 += rows
    lines_104 += len(rows)

    # Телеуправление реле
    adr_104 = 0xC8
    adr_104, rows = get_codes_table_104_3_opis('ТУ на вкл KL',
                                adr_104, 0, 0x42, 0xF6, 0, 40)
    rows_104 += rows
    lines_104 += len(rows)

    rows_104.append(separ_104)
    content_104.append([len(content_104), line_104, lines_104, 10])
    line_104 += lines_104 + 1

    # --------------------------------------------------------------------------
    lines_104 = 0

    # Аналоговые данные
    dict_vars = {**dev_dict["vrIOAI_RX"]["Meas"],
                 **dev_dict["vrIOAI_RX"].get("MeasCalc", {})}
    adr_104 = 500
    adr_104, rows, nots_ad = get_table_104_7_maps(dict_vars, adr_104, 0,
                                                    0x82, adr_AI_RX_begin)
    rows_104 += rows
    lines_104 += len(rows)

    rows_104.append(separ_104)
    content_104.append([len(content_104), line_104, lines_104, 10])
    line_104 += lines_104 + 1

    # --------------------------------------------------------------------------
    lines_104 = 0

    # Аналоговые данные с плав точкой
    dict_vars = {**dev_dict["vrIOAI_RX"]["Meas"],
                 **dev_dict["vrIOAI_RX"].get("MeasCalc", {})}
    adr_104 = 1000
    adr_104, rows, nots_ad = get_table_104_17_maps(dict_vars, adr_104, 0,
                                                    0x82, adr_AI_RX_begin)
    rows_104 += rows
    lines_104 += len(rows) // 2  # 2 строки на одну запись

    rows_104.append(separ_104)
    content_104.append([len(content_104), line_104, lines_104, 20])
    line_104 += lines_104 + 1 + len(rows) // 2  # 2 строки на одну запись

    # --------------------------------------------------------------------------
    lines_104 = 0

    # Парные DI
    adr_104 = 300
    dict_bits = dev_dict["vCurState"]["DIs"]
    adr_104, rows = get_bits_table_104_6_maps(dict_bits,
                                adr_104, 0, 0x83, "Состояние DI")
    rows_104 += rows
    lines_104 += len(rows)

    # Парные KLs
    dict_bits = dev_dict["vCurState"]["KLs"]
    adr_104, rows = get_bits_table_104_6_maps(dict_bits,
                                adr_104, 0, 0x83, "Состояние KL")
    rows_104 += rows
    lines_104 += len(rows)

    rows_104.append(separ_104)
    content_104.append([len(content_104), line_104, lines_104, 10])
    line_104 += lines_104 + 1

    # --------------------------------------------------------------------------
    lines_104 = 0

    # Откл ВВ по ТУ
    adr_104 = 40
    adr_104, rows = get_codes_table_104_6_opis(['Вкл/Откл ВВ по ТУ'],
                                adr_104, 0, 0x42, 0xFB, 0)
    rows_104 += rows
    lines_104 += len(rows)

    # Телеуправление реле
    adr_104 = 400
    adr_104, rows = get_codes_table_104_6_opis('ТУ на Вкл KL',
                                adr_104, 0, 0x42, 0xF6, 0, 40)
    rows_104 += rows
    lines_104 += len(rows)

    rows_104.append(separ_104)
    content_104.append([len(content_104), line_104, lines_104, 10])
    line_104 += lines_104 + 1

    # --------------------------------------------------------------------------
    content_104.append([len(content_104), -10, 0, 20])
    content_104.append([len(content_104), -10, 0, 10])

    # --------------------------------------------------------------------------
    # Дополнение инф о таблицах к 10 байтам
    content_104 = [[ds[0] + 1, 255, 255, 255,
                    *(ds[1] + len(content_104) + 1).to_bytes(2, 'little')] +
                    ds[2:] + [255, 255, '', '', ''] for ds in content_104]
    content_104.append(separ_104)

    # Помещение перед остальными таблицами
    rows_104 = content_104 + rows_104

    # Завершающий таблицы повторный сепаратор
    rows_104.append(separ_104)
    return rows_104, nots_ad
#-------------------------------------------------------------------------------

# ============================================================================
def get_table_104_17_maps(dict_vars, adr_104, grp, fun2, adr_begin=0):
    """ Выдаёт все данные как надо """
    dict_vars['']
    nots_ad = []
    rows = []
    for ds in table_AD_104:
        params_in = dict_vars
        for k in ds[-3].split('/'):
            if k not in params_in:
                nots_ad.append(f'\t104 без {ds[-3]}  ; {ds[-1]}')
                break
            params_in = params_in[k]
        else:
            frac = params_in.get("f", 0)
            size = params_in["size"]
            dtype_i = f'F{size - frac}.{frac}'
            dtype_f = 'Float'
            if ds[-1][0] == '±':
                size |= 0x80
            tmp1 = [*adr_104.to_bytes(2, 'little'), grp, fun2,
                    params_in["adr"] - adr_begin, size, 17, 255, 255, 255,
                    dtype_f, str(ds[-2]), ds[-1]]
            tmp2 = [0, 0, 0x80, 0x3F, 255, 255, 255, 255, 255, 255, '', '', '']
            if ds[-2][-1:]:  # есть множитель
                tmp1[7:10] = [0xF0, int(ds[-2][-1:]), 0x20]
            if ds[-2][-2:-1]:  # есть делитель
                tmp2[7:10] = [0xF0, int(ds[-2][-2:-1]), 0x20]
            for x in ('(°)', '(%)', '±', '(Гц)', '(кВА)'):
                if x in ds[-1]:
                    tmp1[10] = dtype_i
                    break
            if '(°)' in ds[-1]:
                tmp1[6: 10] = [32, 255, 255, 255]
                tmp2[4: 6] = int.to_bytes(360, 2, 'little')
            rows.append(tmp1)
            rows.append(tmp2)
            adr_104 += 1
    return adr_104, rows, nots_ad
#-------------------------------------------------------------------------------

# ============================================================================
def get_table_104_7_maps(dict_vars, adr_104, grp, fun2, adr_begin=0):
    """ Выдаёт все данные как надо """
    dict_vars['']
    nots_ad = []
    rows = []
    for ds in table_AD_103:
        params_in = dict_vars
        for k in ds[-3].split('/'):
            if k not in params_in:
                nots_ad.append(f'\t104 без {ds[-3]}  ; {ds[-1]}')
                break
            params_in = params_in[k]
        else:
            frac = params_in.get("f", 0)
            size = params_in["size"]
            val = round(256 ** frac * ds[-2]).to_bytes(4, 'little')
            dtype = f'F{size - frac}.{frac}'
            if ds[-1][0] == '±':
                size |= 0x80
            tmp = [*adr_104.to_bytes(2, 'little'), grp, fun2,
                            params_in["adr"] - adr_begin, size, *val,
                            dtype, str(ds[-2]), ds[-1]]
            rows.append(tmp)
            adr_104 += 1
    return adr_104, rows, nots_ad
#-------------------------------------------------------------------------------

# ============================================================================
def get_bits_table_104_3_maps(dict_bits, adr_104, grp, fun2, prefix='',
                        suffix='', bit_begin=0, bit_end=999, adr_begin=0):
    rez_bits = {}
    if dict_bits[XX]["typeBase"] == "bits":
        dict_bits = {'null': dict_bits}
    for key, bits in dict_bits.items():
        if key == XX:
            continue
        for bit_name, bit_prop in bits.items():
            if bit_name == XX:
                adr = bit_prop["adr"]
                continue
            if bit_prop["txtFild"][:1] in ('\n', '?'):
                continue
            del bit_prop["typeBase"]
            bit_prop.pop("remFild", None)
            npp = bit_prop.pop("npp")
            rez_bits[(adr, npp)] = bit_prop["txtFild"]

    rows = []
    for (adr, npp), txtFild in sorted(rez_bits.items()):
        if not bit_begin <= npp <= bit_end:
            continue
        tmp = [*adr_104.to_bytes(2, 'little'), grp, fun2,
                adr - adr_begin + npp // 8, npp % 8, 255,255,255,255,'Bit','',
                ' '.join((prefix, txtFild.replace('_', ' '), suffix)).strip()]
        rows.append(tmp)
        adr_104 += 1
    return adr_104, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_bits_table_104_6_maps(dict_bits, adr_104, grp, fun2, prefix='',
                        suffix='', bit_begin=0, bit_end=999, adr_begin=0):
    rez_bits = {}
    if dict_bits[XX]["typeBase"] == "bits":
        dict_bits = {'null': dict_bits}
    for key, bits in dict_bits.items():
        if key == XX:
            continue
        for bit_name, bit_prop in bits.items():
            if bit_name == XX:
                adr = bit_prop["adr"]
                continue
            if bit_prop["txtFild"][:1] in ('\n', '?'):
                continue
            del bit_prop["typeBase"]
            bit_prop.pop("remFild", None)
            npp = bit_prop.pop("npp")
            rez_bits[(adr, npp)] = bit_prop["txtFild"]

    rows = []
    for (adr, npp), txtFild in sorted(rez_bits.items()):
        if not bit_begin <= npp <= bit_end:
            continue
        if rows and len(rows[-1]) < 10:  # Дописываем строку
            bit12_name = f'{bit1_name}-{txtFild}'.replace('_', ' ')
            tmp = [fun2, adr - adr_begin + npp // 8, npp % 8,255,'2 Bits', '',
                ' '.join((prefix, bit12_name, suffix)).strip()]
            rows[-1] += tmp
        else:  # Начинаем строку
            tmp = [*adr_104.to_bytes(2, 'little'), grp, fun2,
                adr - adr_begin + npp // 8, npp % 8]
            rows.append(tmp)
            adr_104 += 1
            bit1_name = txtFild
    if rows and len(rows[-1]) < 10:  # Дописываем строку
        tmp = [255, 255, 255,255,'Bit', '',
            ' '.join((prefix, bit1_name.replace('_', ' '), suffix)).strip()]
        rows[-1] += tmp
    return adr_104, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_codes_table_104_6_opis(opis,adr_104,grp,fun2,code,num_begin,count=-1):
    if isinstance(opis, list):
        txtFilds = [s.strip() for s in opis]
    elif isinstance(opis, str):
        txtFilds = [f'{opis.strip()} {i + 1:02}' for i in range(count)]
    rows = []
    for i, txtFild in enumerate(txtFilds):
        if rows and len(rows[-1]) < 10:  # Дописываем строку
            bit12_name = f'{bit1_name}-{txtFild.rsplit(None, 1)[-1]}'
            tmp = [255, 255, 255, 255, '2 Bits', '', bit12_name]
            rows[-1] += tmp
        else:  # Начинаем строку
            tmp = [*adr_104.to_bytes(2,'little'),grp, fun2,code, i + num_begin]
            rows.append(tmp)
            adr_104 += 1
            bit1_name = txtFild
    if rows and len(rows[-1]) < 10:  # Дописываем строку
        tmp = [255, 255, 255,255,'2 Bits', '', bit1_name]
        rows[-1] += tmp
    return adr_104, rows
#-------------------------------------------------------------------------------

# ============================================================================
def create_htm_table_104(dev, rows_104, n):  # n=10=2
    htm_table_104 = [f'''\
<!DOCTYPE html>
<HTML>
  <HEAD>
    <META charset="utf-8">
    <TITLE>{dev}</TITLE>
  </HEAD>
  <BODY>
    <TABLE cellspacing="0" cellpadding="2" border="1" align="center">''', ('''\
      <TR>
        <TH colspan=2>Ном инф<br>/Обл
        <TH rowspan=2>Ном<br>гр.
        <TH rowspan=2>Фор-<BR>мат
        <TH rowspan=2>Знач<BR>норм
        <TH rowspan=2>Описание
      <TR>
        <TH>LSB
        <TH>MSB''', '''\
      <TR>
        <TH colspan=2>Ном инф<br>/Обл
        <TH rowspan=2>Ном<br>гр.
        <TH rowspan=2>Спос<br>дост
        <TH colspan=2>Адр инф<br>/бита
        <TH rowspan=2>Колич<br>зап<br>/Байт<br>норм
        <TH rowspan=2>Разм<br>зап<br>/Байт<br>норм
        <TH rowspan=2 colspan=2>Байты<br>нормализации
        <TH rowspan=2>Фор-<BR>мат
        <TH rowspan=2>Знач<BR>норм
        <TH rowspan=2>Описание
      <TR>
        <TH>LSB
        <TH>MSB
        <TH>Смещ
        <TH>Колич''')[n // 8], '''\
      <TR height=7>''' + '<TD>' * n]

    for cels in rows_104[len(content_104) * (1 - n // 8):-2]:
        if cels[:10] == [255] * 10:
            if n == 6:
                htm_table_104.append('      <TR height=7>' + '<TD>' * 6)
            else:
                htm_table_104.append('      <TR height=7>' + '<TD>' * n)
            continue
        if n < 8 and cels[-3:] == [''] * 3:
            continue
        row = "<TD>".join([f"&nbsp;{ds:02X}" for ds in cels[:3]] + (
                          [f"&nbsp;{ds:02X}" for ds in cels[3:-3]]
                          ) * (n // 8) + cels[-3:])
        htm_table_104.append(f'      <TR><TD>{row}')
    htm_table_104.append('''\
    </TABLE>
  </BODY>
</HTML>''')
    return htm_table_104
#-------------------------------------------------------------------------------

# ============================================================================
def get_codes_table_104_3_opis(opis,adr_104,grp,fun2,code,num_begin,count=-1):
    if isinstance(opis, list):
        txtFilds = [s.strip() for s in opis]
    elif isinstance(opis, str):
        f = count > 9 and '02' or ''
        txtFilds = [f'{opis.strip()} {i + 1:{f}}' for i in range(count)]
    rows = []
    for i, txtFild in enumerate(txtFilds):
        tmp = [*adr_104.to_bytes(2, 'little'), grp, fun2, code, i + num_begin,
                                    255, 255, 255, 255, 'Bit', '', txtFild]
        rows.append(tmp)
        adr_104 += 1
    return adr_104, rows
#-------------------------------------------------------------------------------

# ============================================================================
# Общие для устройств таблицы
separ_104 = [255] * 10 + [''] * 3

# ============================================================================
if __name__ == '__main__':
    import os
    os.system('start create_protocols_tables.bat debug')
# ----------------------------------------------------------------------------
