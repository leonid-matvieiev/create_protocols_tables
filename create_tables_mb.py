from copy import deepcopy

# ============================================================================
def create_rows_mb(dev, all_devs, devs_ad_const):
    dev_dict = deepcopy(all_devs[dev])

    rows_mb = []
    adr_AI_RX_begin = dev_dict["vrIOAI_RX"][XX]["adr"]

    # --------------------------------------------------------------------------
    adr_mb = 0x0000
    # KLs
    dict_bits = dev_dict["vCurState"]["KLs"]
    adr_mb, rows = get_bits_table_mb_3_maps(dict_bits,
                                0x01, adr_mb, 0x83, "Bit", "Состояние KL")
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0050
    # Пуски
    dict_bits = dev_dict["vCurState"]["Pusks"]
    adr_mb, rows = get_bits_table_mb_3_maps(dict_bits,
                                0x01, adr_mb, 0x83, "Bit", 'Пуск')
    rows_mb += rows

    # Работы
    dict_bits = dev_dict["vCurState"]["Works"]
    adr_mb, rows = get_bits_table_mb_3_maps(dict_bits,
                                0x01, adr_mb, 0x83, "Bit", 'Работа')
    rows_mb += rows

    # VV
    if "VV" in dev_dict["vCurState"]:
        dict_bits = dev_dict["vCurState"]["VV"]
        adr_mb, rows = get_bits_table_mb_3_maps(dict_bits,
                                0x01, adr_mb, 0x83, "Bit", bit_end=7)
        rows_mb += rows

    # Ускорения
    dict_bits = dev_dict["vAcce"]
    adr_mb, rows = get_bits_table_mb_3_maps(dict_bits,
                                0x01, adr_mb, 0x83, "Bit", 'Работа', 'с ускор')
    rows_mb += rows

    # APV
    if 'vAPV1' in dev_dict and isinstance(dev_dict['vAPV1'], dict):  #Один АПВ
        var_adr = dev_dict["vAPV1"][XX]["adr"]
#        adr_mb, rows = get_bits_table_mb_3_txtFilds('Готовность АПВ',
        adr_mb, rows = get_bits_table_mb_3_opis(['Готовность АПВ'],
                                0x01, adr_mb, 0x83, var_adr, 0x02, 'Bit')
        rows_mb += rows
    elif 'vAPV' in dev_dict and isinstance(dev_dict['vAPV'], list):  # Два АПВ
        var_adr = dev_dict["vAPV"][0][XX]["adr"]
        adr_mb, rows = get_bits_table_mb_3_opis(['Готовность АПВ 1'],
                                0x01, adr_mb, 0x83, var_adr, 0x02, 'Bit')
        rows_mb += rows
        var_adr = dev_dict["vAPV"][1][XX]["adr"]
        adr_mb, rows = get_bits_table_mb_3_opis(['Готовность АПВ 2'],
                                0x01, adr_mb, 0x83, var_adr, 0x02, 'Bit')
        rows_mb += rows

    # Инф АИ
    dict_bits = dev_dict["vrIOAI_RX"]["BData"]["Inf"]
    adr_mb, rows = get_bits_table_mb_3_maps(dict_bits,
                                0x01, adr_mb, 0x82, "Bit", 'Инф комп',
                                adr_begin=adr_AI_RX_begin)
    rows_mb += rows
    rows_mb.append(separ_mb)

    # --------------------------------------------------------------------------
    adr_mb = 0x0600
    # Состояния светодиодов
    adr_mb, rows = get_bits_table_mb_3_opis(txtFilds_VDs,
                                0x01, adr_mb, 0x84, 0x52, 0, 'Bit')
    rows_mb += rows
    rows_mb.append(separ_mb)

    # --------------------------------------------------------------------------
    adr_mb = 0x0028
    # DI
    dict_bits = dev_dict["vCurState"]["DIs"]
    adr_mb, rows = get_bits_table_mb_3_maps(dict_bits,
                                0x02, adr_mb, 0x83, "Bit", "Состояние DI")
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0300
    # Вирт DI
    adr_mb, rows = get_bits_table_mb_3_opis('Сост вирт DI',
                                0x02, adr_mb, 0x81, 0x00, 0, 'Bit', 40)
    rows_mb += rows
    rows_mb.append(separ_mb)

    # --------------------------------------------------------------------------
    adr_mb = 0x0100
    # Коэфф трансформации
    dict_vars = dev_dict["UST"]["ToAI"]["StDataAI"]["KT"]
    adr_mb, rows = get_bytes_table_mb_5_maps(dict_vars,
                                0x03, adr_mb, 0x44, "F2.0")
    rows_mb += rows
    rows_mb.append(separ_mb)

    # --------------------------------------------------------------------------
    adr_mb = 0x0000
    # Дата-время
    dict_vars = dev_dict["vrIOAI_RX"]["DT"]
    adr_mb, rows = get_table_mb_3_maps(dict_vars,
                                0x04, adr_mb, 0x82, "F2.0", adr_AI_RX_begin)
    rows_mb += rows

    # Фрагменты акт состояния

    # Номер тек гр уставок
    adr = dev_dict["vCurState"]["NUst"]["adr"]
    adr_mb, rows = get_bytes_table_mb_3_opis(['Номер тек гр уставок'],
                                0x04, adr_mb, 0x83, adr, 'F2.0')
    rows_mb += rows

    # Сост дискр выходов KL
    adr = dev_dict["vCurState"]["KLs"][XX]["adr"]
    size = dev_dict["vCurState"]["KLs"][XX]["size"]
    adr_mb, rows = get_bytes_table_mb_3_opis('Сост дискр выходов KL',
                                0x04, adr_mb, 0x83, adr, 'Bits16', size)
    rows_mb += rows

    # Сост дискр входов DI
    adr = dev_dict["vCurState"]["DIs"][XX]["adr"]
    size = dev_dict["vCurState"]["DIs"][XX]["size"]
    adr_mb, rows = get_bytes_table_mb_3_opis('Сост дискр входов DI',
                                0x04, adr_mb, 0x83, adr, 'Bits16', size)
    rows_mb += rows

    # Аналоговые данные
    dict_vars = {**dev_dict["vrIOAI_RX"]["Meas"],
                 **dev_dict["vrIOAI_RX"].get("MeasCalc", {})}
    adr_mb, rows = get_table_mb_3_maps(dict_vars,
                                0x04, adr_mb, 0x82, "F2.0", adr_AI_RX_begin)
    rows_mb += rows
    rows_mb.append(separ_mb)

    # --------------------------------------------------------------------------
    adr_mb = 0x0200
    # Код спец и серийный номер
    adr_mb, rows = get_bytes_table_mb_5_opis(txtFilds_CSP_SN,
                                0x04, adr_mb, 0x44, 0x800011, 'Chr2')
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x020B
    # Защёлки квитирования
    adr = dev_dict["EROtherData"]["vKvt"][XX]["adr"]
    size = dev_dict["EROtherData"]["vKvt"][XX]["size"]
    adr_mb, rows = get_bytes_table_mb_5_opis('Защёлки квитирования',
                                0x04, adr_mb, 0x44, adr, 'Bits16', size)
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0400
    # Состояния светодиодов
    adr_mb, rows = get_bytes_table_mb_3_opis('Состояния светодиодов',
                                0x04, adr_mb, 0x84, 0x52, 'Bits16', 6)
    rows_mb += rows
    rows_mb.append(separ_mb)

    # --------------------------------------------------------------------------
    adr_mb = 0x0000
    # Телеуправление реле
    adr_mb, rows = get_codes_table_mb_3_opis('ТУ на вкл KL',
                                0x05, adr_mb, 0x42, 0xF6, 0, 'Bit', 40)
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0100
    # Квитирование и пуск осциллографа по ТУ
    adr_mb, rows = get_codes_table_mb_3_opis(['Квит по ТУ', 'Пуск осц по ТУ'],
                                0x05, adr_mb, 0x42, 0xF9, 1, 'Bit', 2)
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0200
    # Вкл/Откл ВВ по ТУ
    adr_mb, rows = get_codes_table_mb_3_opis(['Вкл ВВ по ТУ', 'Откл ВВ по ТУ'],
                                0x05, adr_mb, 0x42, 0xFB, 0, 'Bit', 2)
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0300
    # Установка значения вирт ДИ
    adr_mb, rows = get_bits_table_mb_3_opis('Уст вирт DI',
                                0x05, adr_mb, 0x81, 0, 0, 'Bit', 40)
    rows_mb += rows
    rows_mb.append(separ_mb)

    # --------------------------------------------------------------------------
    adr_mb = 0x0000
    # Телеуправление реле
    adr_mb, rows = get_codes_table_mb_3_opis('ТУ на вкл KL',
                                0x0F, adr_mb, 0x42, 0xF6, 0, 'Bit', 40)
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0100
    # Квитирование и пуск осциллографа по ТУ
    adr_mb, rows = get_codes_table_mb_3_opis(['Квит по ТУ', 'Пуск осц по ТУ'],
                                0x0F, adr_mb, 0x42, 0xF9, 1, 'Bit', 2)
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0200
    # Вкл/Откл ВВ по ТУ
    adr_mb, rows = get_codes_table_mb_3_opis(['Вкл ВВ по ТУ', 'Откл ВВ по ТУ'],
                                0x0F, adr_mb, 0x42, 0xFB, 0, 'Bit', 2)
    rows_mb += rows
    rows_mb.append(separ_mb)

    adr_mb = 0x0300
    # Установка значения вирт ДИ
    adr_mb, rows = get_bits_table_mb_3_opis('Уст вирт DI',
                                0x0F, adr_mb, 0x81, 0, 0, 'Bit', 40)
    rows_mb += rows
    rows_mb.append(separ_mb)
#-------------------------------------------------------------------------------

    adr_mb = 0x1000
    # Установка значения Даты-Времени
    adr_mb, rows = get_time_table_mb_5_opis(txtFilds_DT,
                                0x10, adr_mb, 0x69, 0xF00100, 0x03, 'Byte6')
    rows_mb += rows
    rows_mb.append(separ_mb)

    rows_mb.append(separ_mb)
    return rows_mb
#-------------------------------------------------------------------------------

# ============================================================================
def create_htm_table_mb(dev, rows_mb, n=10):  # n=5
    htm_table_mb = [f'''\
<!DOCTYPE html>
<HTML>
  <HEAD>
    <META charset="windows-1251">
    <TITLE>{dev}</TITLE>
  </HEAD>
  <BODY>
    <TABLE cellspacing="0" cellpadding="2" border="1" align="center">
      <TR><TH colspan=3>Modbus-RTU%s<TH rowspan=2>Фор-<BR>мат<TH rowspan=2>Описание
      <TR><TH>Ф-я<TH colspan=2>Регистр
      <TR height=7>''' % ('<TH rowspan=2>' * (n - 5)) + '<TD>' * n]
    for cels in rows_mb[:-2]:
        if cels[:8] == [255] * 8:
            if n == 5:
                htm_table_mb.append('      <TR height=7>' + '<TD>' * 5)
            else:
                htm_table_mb.append('      <TR height=7>' + '<TD>' * n)
            continue
        row = "<TD>".join([f"&nbsp;{ds:02X}" for ds in cels[:3]] + (
                          [f"&nbsp;{ds:02X}" for ds in cels[3:-2]]
                          ) * (n // 8) + cels[-2:])
        htm_table_mb.append(f'      <TR><TD>{row}')
    htm_table_mb.append('''\
    </TABLE>
  </BODY>
</HTML>''')
    return htm_table_mb
#-------------------------------------------------------------------------------

# ============================================================================
def get_time_table_mb_5_opis(opis, fun1, adr_mb, fun2, adr, size, dtype, count=-1):
    if isinstance(opis, list):
        txtFilds = [s.strip() for s in opis]
    elif isinstance(opis, str):
        f = count > 9 and '02' or ''
        txtFilds = [f'{opis.strip()} {i + 1:{f}}' for i in range(count)]
    rows = []
    for i, txtFild in enumerate(txtFilds):
        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                adr // 0x10000, adr // 0x100 % 0x100, adr % 0x100, size,
                dtype, txtFild]
        rows.append(tmp)
        adr_mb += 1
    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_bytes_table_mb_5_maps(dict_vars, fun1, adr_mb, fun2, dtype):
    rows = []
    prefix = dict_vars[XX]['txtFild']
    for var, params in dict_vars.items():
        if var == XX:
            continue
        adr = params['adr']
        size = params['size']
        txtFild = params['txtFild']
        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                adr // 0x10000, adr // 0x100 % 0x100, adr % 0x100, size,
                dtype, ' '.join((prefix, txtFild.replace('_', ' '))).strip()]
        rows.append(tmp)
        adr_mb += 1
    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_bytes_table_mb_3_opis(opis, fun1, adr_mb, fun2, adr, dtype, size=None):
    if isinstance(opis, str):
        f = size and size > 9 and '02' or ''
        txtFilds = [(2, f'{opis.strip()} (байты {i * 2 + 1:{f}} и {i * 2 + 2:{f}})')
                                            for i in range(0, size // 2)]
        if size % 2:  # Нечётное количество
            txtFilds += [(1, f'{opis.strip()} (байт {size})')]
    elif isinstance(opis, list):
        txtFilds = [(2, s.strip()) for s in opis]
    rows = []
    for size, txtFild in txtFilds:
        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                adr, size, 255, 255,
                dtype, txtFild]
        rows.append(tmp)
        adr += size
        adr_mb += 1
    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_bytes_table_mb_5_opis(opis, fun1, adr_mb, fun2, adr, dtype, size=None):
    if isinstance(opis, str):
        f = size and size > 9 and '02' or ''
        txtFilds = [(2, f'{opis.strip()} (байты {i * 2 + 1:{f}} и {i * 2 + 2:{f}})')
                                            for i in range(0, size // 2)]
        if size % 2:  # Нечётное количество
            txtFilds += [(1, f'{opis.strip()} (байт {size})')]
    elif isinstance(opis, list):
        txtFilds = [(2, s.strip()) for s in opis]
    rows = []
    for size, txtFild in txtFilds:
        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                adr // 0x10000, adr // 0x100 % 0x100, adr % 0x100, size,
                dtype, txtFild]
        rows.append(tmp)
        adr += size
        adr_mb += 1
    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_codes_table_mb_3_opis(opis, fun1, adr_mb, fun2, code, num_begin, dtype, count=-1):
    if isinstance(opis, list):
        txtFilds = [s.strip() for s in opis]
    elif isinstance(opis, str):
        f = count > 9 and '02' or ''
        txtFilds = [f'{opis.strip()} {i + 1:{f}}' for i in range(count)]
    rows = []
    for i, txtFild in enumerate(txtFilds):
        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                code, i + num_begin, 255, 255,
                dtype, txtFild]
        rows.append(tmp)
        adr_mb += 1
    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_table_mb_3_maps(dict_vars, fun1, adr_mb, fun2, dtype, adr_begin=0):

    def recurs(params_in):
        nonlocal adr_mb
        if XX in params_in:
            names.append(params_in[XX]["txtFild"])
            for k, params_out in params_in.items():
                if k == XX:
                    continue
                recurs(params_out)
            names.pop()
            return

        vmax = params_in["uBoundPrm"]
        vmin = params_in.get("lBoundPrm", 0)
        vstep = params_in.get("stepPrm", 1)
        diapp = f' [{vmin}-{vmax}:{vstep}]'
        rem_fild = params_in.get("remFild", '').strip()
        rem = ', '.join([rem_struct or rem_fild])  # можно через запятую
        prec = params_in.get("stepPrm_prec", 0)
        frac = params_in.get("f", 0)
        size = params_in["size"]
        txtFild = ', '.join(names + [params_in["txtFild"]]) + diapp + (
            prec and f'.{"0" * prec}' or '') + (
            rem and f' ; {rem}' or '')

        if size <= 2:
            dtype = f'F{2 - frac}.{frac}'
            tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                    params_in["adr"] - adr_begin, size, 255, 255,
                    dtype, txtFild]
            rows.append(tmp)
            adr_mb += 1
            return

        dtype = f'F{4 - frac}.{frac}'

        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                params_in["adr"] + 2 - adr_begin, size - 2, 255, 255,
                dtype, txtFild]
        rows.append(tmp)
        adr_mb += 1

        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                params_in["adr"] - adr_begin, 2, 255, 255,
                '    ', '(мл слово)']
        rows.append(tmp)
        adr_mb += 1

    names = []
    rows = []
    for var, params in dict_vars.items():
        if var == XX:
            continue
        rem_struct = params.get("remFild", '').strip()
        recurs(params)

    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_bits_table_mb_3_opis(opis, fun1, adr_mb, fun2, adr, bit_begin, dtype, count=-1):
    if isinstance(opis, str):
        f = count > 9 and '02' or ''
        txtFilds = [f'{opis.strip()} {i + 1:{f}}' for i in range(count)]
    elif isinstance(opis, list):
        txtFilds = [s.strip() for s in opis]
    bit = adr * 8 + bit_begin
    rows = []
    for txtFild in txtFilds:
        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                bit // 8, bit % 8, 255, 255,
                dtype, txtFild]
        rows.append(tmp)
        bit += 1
        adr_mb += 1
    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
def get_bits_table_mb_3_maps(dict_bits, fun1, adr_mb, fun2, dtype, prefix='',
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
#            bit_prop.pop("typeBase", None)
            bit_prop.pop("remFild", None)
            npp = bit_prop.pop("npp")
            rez_bits[(adr, npp)] = bit_prop["txtFild"]

    rows = []
    for (adr, npp), txtFild in sorted(rez_bits.items()):
        if not bit_begin <= npp <= bit_end:
            continue
        tmp = [fun1, adr_mb // 256, adr_mb % 256, fun2,
                adr - adr_begin + npp // 8, npp % 8, 255, 255, dtype,
                ' '.join((prefix, txtFild.replace('_', ' '), suffix)).strip()]
        rows.append(tmp)
        adr_mb += 1
    return adr_mb, rows
#-------------------------------------------------------------------------------

# ============================================================================
# Общие для устройств таблицы
separ_mb = [255] * 8 + ['', '']

txtFilds_DT = '''\
Установка времени (bYY bMM)*
Установка времени (bDD bHH)*
Установка времени (bmm bSS)*
'''.strip().splitlines()

txtFilds_CSP_SN = '''\
Код специф (симв 1 и 2)
Код специф (симв 3 и 4)
Код специф (симв 5 и 6)
Код специф (симв 7 и 8)
Код специф (симв 9 и 10)
Код специф (симв 11 и 12)
Код специф (симв 13 и 14)
Код специф (симв 15 и 16)
Серийн ном (симв 1 и 2)
Серийн ном (симв 3 и 4)
Серийн ном (симв 5 и 6)
Серийн ном (симв 7 и 8)
'''.strip().splitlines()

txtFilds_VDs = '''\
Красн своб прогр светодиод (VD 01)
Красн своб прогр светодиод (VD 02)
Красн своб прогр светодиод (VD 03)
Красн своб прогр светодиод (VD 04)
Красн своб прогр светодиод (VD 05)
Красн своб прогр светодиод (VD 06)
Красн своб прогр светодиод (VD 07)
Красн своб прогр светодиод (VD 08)
Красн своб прогр светодиод (VD 09)
Красн своб прогр светодиод (VD 10)
Красн своб прогр светодиод (VD 11)
Красн своб прогр светодиод (VD 12)
Красн своб прогр светодиод (VD 13)
Красн своб прогр светодиод (VD 14)
Красн своб прогр светодиод (VD 15)
Красн своб прогр светодиод (VD 16)
Зелен своб прогр светодиод (VD 01)
Зелен своб прогр светодиод (VD 02)
Зелен своб прогр светодиод (VD 03)
Зелен своб прогр светодиод (VD 04)
Зелен своб прогр светодиод (VD 05)
Зелен своб прогр светодиод (VD 06)
Зелен своб прогр светодиод (VD 07)
Зелен своб прогр светодиод (VD 08)
Зелен своб прогр светодиод (VD 09)
Зелен своб прогр светодиод (VD 10)
Зелен своб прогр светодиод (VD 11)
Зелен своб прогр светодиод (VD 12)
Зелен своб прогр светодиод (VD 13)
Зелен своб прогр светодиод (VD 14)
Зелен своб прогр светодиод (VD 15)
Зелен своб прогр светодиод (VD 16)
Красн светодиод накладки F1 (VD17)
Красн светодиод накладки F2 (VD18)
Красн светодиод накладки F3 (VD19)
Красн светодиод накладки F4 (VD20)
Красн светодиод ВВ Вкл
Красн светодиод Батарея разряжена
Красн доп светодиод* (ВВ Откл)
Зелен доп светодиод* (ВВ Вкл)
Зелен светодиод накладки F1 (VD17)
Зелен светодиод накладки F2 (VD18)
Зелен светодиод накладки F3 (VD19)
Зелен светодиод накладки F4 (VD20)
Зелен светодиод ВВ Откл
Зелен светодиод местн упр
Зелен светодиод дист упр
Зелен светодиод Работа
'''.strip().splitlines()

# ============================================================================
if __name__ == '__main__':
    import os
    os.system('start create_protocols_tables.bat debug')
# ----------------------------------------------------------------------------
