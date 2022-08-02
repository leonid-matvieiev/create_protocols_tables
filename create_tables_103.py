from pprint import pprint
from copy import deepcopy

# ============================================================================
def create_rows_103(dev, all_devs, devs_ad_const):
#    global content_103
    global table_AD_103
    dev_dict = deepcopy(all_devs[dev])

    table_AD_103 = []
    for dct in devs_ad_const:
        if dct['103\n'+dev[4:]]:
            ts = [dct[k] for k in ('103\n' + dev[4: ],
                                    '103\ncod', 'path', '103\nnorm', 'txt')]
            ts[0] = int(ts[0])
            ts[1] = int(ts[1])
            ts[-2] = ',' in ts[-2] and float(
                            ts[-2].replace(',', '.')) or int(ts[-2])
            table_AD_103.append(ts)
    table_AD_103.sort()

    content_103 = []
    rows_103 = []
    adr_AI_RX_begin = dev_dict["vrIOAI_RX"][XX]["adr"]
    line_103 = 0

    # --------------------------------------------------------------------------
    lines_103 = 0

    # DI
    adr_103 = 0xA0
    dict_bits = dev_dict["vCurState"]["DIs"]
    adr_103, rows = get_bits_table_103_3_maps(dict_bits,
                                adr_103, 0x83, "Состояние DI")
    rows_103 += rows
    lines_103 += len(rows)

    # KLs
    dict_bits = dev_dict["vCurState"]["KLs"]
    adr_103, rows = get_bits_table_103_3_maps(dict_bits,
                                adr_103, 0x83, "Состояние KL")
    rows_103 += rows
    lines_103 += len(rows)

    rows_103.append(separ_103)
    content_103.append([len(content_103) + 1, 255, line_103, 0, lines_103])
    line_103 += lines_103 + 1

    # --------------------------------------------------------------------------
    lines_103 = 0

    # Откл ВВ по ТУ
    adr_103 = 0x28
    adr_103, rows = get_codes_table_103_3_opis(['Откл ВВ по ТУ'],
                                adr_103, 0x42, 0xFB, 1)
    rows_103 += rows
    lines_103 += len(rows)

    # Телеуправление реле
    adr_103 = 0xC8
    adr_103, rows = get_codes_table_103_3_opis('ТУ на откл KL',
                                adr_103, 0x42, 0xF6, 0, 40)
    rows_103 += rows
    lines_103 += len(rows)

    rows_103.append(separ_103)
    content_103.append([len(content_103) + 1, 255, line_103, 0, lines_103])
    line_103 += lines_103 + 1

    # --------------------------------------------------------------------------
    lines_103 = 0

    # Квитирование и пуск осциллографа по ТУ
    adr_103 = 0x13
    adr_103, rows = get_codes_table_103_3_opis(['Квит по ТУ'],
                                adr_103, 0x42, 0xF9, 1)
    rows_103 += rows
    lines_103 += len(rows)

    # Вкл ВВ по ТУ
    adr_103 = 0x28
    adr_103, rows = get_codes_table_103_3_opis(['Вкл ВВ по ТУ'],
                                adr_103, 0x42, 0xFB, 0)
    rows_103 += rows
    lines_103 += len(rows)

    # пуск осциллографа по ТУ
    adr_103, rows = get_codes_table_103_3_opis(['Пуск осц по ТУ'],
                                adr_103, 0x42, 0xF9, 2)
    rows_103 += rows
    lines_103 += len(rows)

    # Телеуправление реле
    adr_103 = 0xC8
    adr_103, rows = get_codes_table_103_3_opis('ТУ на вкл KL',
                                adr_103, 0x42, 0xF6, 0, 40)
    rows_103 += rows
    lines_103 += len(rows)

    rows_103.append(separ_103)
    content_103.append([len(content_103) + 1, 255, line_103, 0, lines_103])
    line_103 += lines_103 + 1

    # --------------------------------------------------------------------------
    lines_103 = 0

    # Аналоговые данные
    dict_vars = {**dev_dict["vrIOAI_RX"]["Meas"],
                 **dev_dict["vrIOAI_RX"].get("MeasCalc", {})}
    rows, nots_ad = get_table_103_7_maps(dict_vars, 0x82, adr_AI_RX_begin)
    rows_103 += rows
    lines_103 += len(rows)

    rows_103.append(separ_103)
    content_103.append([len(content_103) + 1, 255, line_103, 0, lines_103])

    content_103 = [ds[:2] + [ds[2] + len(content_103) + 1] + ds[3:] +
                            [255, 255, 255, '', '', ''] for ds in content_103]
#    content_104.append([len(content_104) + 1, *line_104.to_bytes(2,'little'), lines_104])
#
#    content_104 = [[ds[0], 255, ds[1] + len(content_104) + 1] + ds[2:] +
#                            [255, 255, 255, '', '', ''] for ds in content_104]
    content_103.append(separ_103)

    rows_103 = content_103 + rows_103

    rows_103.append(separ_103)
    return rows_103, nots_ad
#-------------------------------------------------------------------------------

# ============================================================================
def get_table_103_7_maps(dict_vars, fun2, adr_begin=0):
    """ Выдаёт все данные как надо """
    dict_vars['']
    nots_ad = []
    rows = []
    for ds in table_AD_103:
        params_in = dict_vars
        for k in ds[-3].split('/'):
            if k not in params_in:
                nots_ad.append(f'\t103 без {ds[-3]}  ; {ds[-1]}')
                break
            params_in = params_in[k]
        else:
            frac = params_in.get("f", 0)
            size = params_in["size"]
            val = round(256 ** frac * ds[-2]).to_bytes(4,'little')
            dtype = f'F{size - frac}.{frac}'
            if ds[-1][0] == '±':
                size |= 0x80
            tmp = [ds[1], fun2, params_in["adr"] - adr_begin, size,
                                            *val, dtype, str(ds[-2]), ds[-1]]
            rows.append(tmp)
    return rows, nots_ad
#-------------------------------------------------------------------------------

# ============================================================================
def create_htm_table_103(dev, rows_103, n):  # n=10=2
    htm_table_103 = [f'''\
<!DOCTYPE html>
<HTML>
  <HEAD>
    <META charset="utf-8">
    <TITLE>{dev}</TITLE>
  </HEAD>
  <BODY>
    <TABLE cellspacing="0" cellpadding="2" border="1" align="center">''', ('''\
      <TR>
        <TH>Ном<br>обл<br>/INF
        <TH>Фор-<BR>мат
        <TH>Знач<BR>норм
        <TH>Описание''', '''\
      <TR>
        <TH rowspan=2>Ном<br>обл<br>/INF
        <TH rowspan=2>Спос<br>дост
        <TH colspan=2>Адр инф<br>/бита
        <TH rowspan=2>Колич<br>зап<br>/Байт<br>норм
        <TH rowspan=2 colspan=3>Байты норм
        <TH rowspan=2>Фор-<BR>мат
        <TH rowspan=2>Знач<BR>норм
        <TH rowspan=2>Описание
      <TR><TH>Смещ<TH>Колич''')[n // 8], '''\
      <TR height=7>''' + '<TD>' * n]

    for cels in rows_103[5 * (1 - n // 8):-2]:
        if cels[:8] == [255] * 8:
            if n == 4:
                htm_table_103.append('      <TR height=7>' + '<TD>' * 4)
            else:
                htm_table_103.append('      <TR height=7>' + '<TD>' * n)
            continue
        try:
            row = "<TD>".join([f"&nbsp;{ds:02X}" for ds in cels[:1]] + (
                          [f"&nbsp;{ds:02X}" for ds in cels[1:-3]]
                          ) * (n // 8) + cels[-3:])
        except:
            print()
            print(cels)
            a=5
        htm_table_103.append(f'      <TR><TD>{row}')
    htm_table_103.append('''\
    </TABLE>
  </BODY>
</HTML>''')
    return htm_table_103
#-------------------------------------------------------------------------------

# ============================================================================
def get_bits_table_103_3_maps(dict_bits, adr_103, fun2, prefix='',
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
        tmp = [adr_103, fun2,
                adr - adr_begin + npp // 8, npp % 8, 255, 255, 255, 255, 'Bit', '',
                ' '.join((prefix, txtFild.replace('_', ' '), suffix)).strip()]
        rows.append(tmp)
        adr_103 += 1
    return adr_103, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_codes_table_103_3_opis(opis, adr_103, fun2, code, num_begin, count=-1):
    if isinstance(opis, list):
        txtFilds = [s.strip() for s in opis]
    elif isinstance(opis, str):
        f = count > 9 and '02' or ''
        txtFilds = [f'{opis.strip()} {i + 1:{f}}' for i in range(count)]
    rows = []
    for i, txtFild in enumerate(txtFilds):
        tmp = [adr_103, fun2, code, i + num_begin, 255, 255, 255, 255,
                                                    'Bit', '', txtFild]
        rows.append(tmp)
        adr_103 += 1
    return adr_103, rows
#-------------------------------------------------------------------------------

# ============================================================================
# Общие для устройств таблицы
separ_103 = [255] * 8 + [''] * 3

# ============================================================================
if __name__ == '__main__':
    import os
    os.system('start create_protocols_tables.bat debug')
# ----------------------------------------------------------------------------
