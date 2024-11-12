from PyDAQmx import Task
import numpy as np
# import PyDAQmx
import PyDAQmx.DAQmxConstants as const
import CoolProp.CoolProp as cp
import pandas as pd
import time

# tenka je T type, ostatni jsou E
# cervena minus krome cinskych shitu


class ThermocoupleTReader(Task):
    def __init__(self):
        Task.__init__(self)
        self.CreateAIThrmcplChan("Dev1/ai0", "", -200.0, 400,
                                 const.DAQmx_Val_DegC,
                                 const.DAQmx_Val_T_Type_TC,
                                 const.DAQmx_Val_BuiltIn, 0.0,
                                 None)
        self.CreateAIThrmcplChan("Dev1/ai1", "", -200.0, 900,
                                 const.DAQmx_Val_DegC,
                                 const.DAQmx_Val_E_Type_TC,
                                 const.DAQmx_Val_BuiltIn, 0.0,
                                 None)
        self.CreateAIThrmcplChan("Dev1/ai2", "", -200.0, 900,
                                 const.DAQmx_Val_DegC,
                                 const.DAQmx_Val_E_Type_TC,
                                 const.DAQmx_Val_BuiltIn, 0.0,
                                 None)
        self.CreateAIThrmcplChan("Dev1/ai3", "", -200.0, 900,
                                 const.DAQmx_Val_DegC,
                                 const.DAQmx_Val_E_Type_TC,
                                 const.DAQmx_Val_BuiltIn, 0.0,
                                 None)
        self.CfgSampClkTiming("", 1.0, const.DAQmx_Val_Rising, const.DAQmx_Val_FiniteSamps, 10)

    def read_temperature(self):
        data = np.zeros(4)
        self.ReadAnalogF64(1, 10.0, const.DAQmx_Val_GroupByChannel, data, 4, None, None)
        return data


def mereni(cas, nazov):
    Z = 273.15
    timing = cas

    tc1 = np.empty(timing)
    tc2 = np.empty(timing)
    tc3 = np.empty(timing)
    tc4 = np.empty(timing)
    rel_hum = np.empty(timing)
    x_hum = np.empty(timing)
    h_da = np.empty(timing)

    all_data = [tc1, tc2, tc3, tc4, rel_hum, x_hum, h_da]

    nazev = nazov

    readerT = ThermocoupleTReader()
    for i in range(timing):
        temperature = readerT.read_temperature()
        print("Aktualne merene teploty:", temperature)
        tc1[i] = temperature.item(0)
        tc2[i] = temperature.item(1)
        tc3[i] = temperature.item(2)
        tc4[i] = temperature.item(3)
        try:
            rel_hum[i] = cp.HAPropsSI('RH', 'Twb', temperature.item(1)+Z, 'T', temperature.item(2)+Z, 'P', 101325)*100
        except ValueError:
            rel_hum[i] = 1
            print('Zcekujte si termoclanky, vas mokry teplomer je teplejsi nez suchy xd')
        x_hum[i] = cp.HAPropsSI('W', 'Twb', temperature.item(1)+Z, 'T', temperature.item(2)+Z, 'P', 101325)*1000
        h_da[i] = cp.HAPropsSI('H', 'Twb', temperature.item(1)+Z, 'T', temperature.item(2)+Z, 'P', 101325)/1000
        time.sleep(0.5)

    header_df = pd.DataFrame(['Termoclanek_1', 'Termoclanek_2', 'Termoclanek_3', 'Termoclanek_4', 'Relativni_vlhkost', 'Merna_vlhkost', 'Entalpie'])
    sub_header = pd.DataFrame(['Chudak [°C]', 'Mokry_teplomer [°C]', 'Suchy_teplomer [°C]', 'Teplota_mimo [°C]', '[%]', '[g_H2O/kg_sv]', '[kJ/kg_sv]'])
    df = pd.DataFrame(all_data)
    df = pd.concat([header_df, sub_header, df], axis=1)
    df = df.transpose()
    print('Mereni dokonceno')
    jmeno_excelu = f'{nazev}.xlsx'
    df.to_excel(jmeno_excelu, index=False)
    print(f'Data byla vyexportovana do {jmeno_excelu}')
