import requests
import json



# 設定要傳送的 API URL
# url = "https://www.kutech.tw:3000/medgpt"
url = "http://127.0.0.1:5000/medgpt"


payload = {
    "Data": {
        "eff_order": [
            {
                "MED_BAG_SN": "7;20250421;0001410815;1;STAT;IVD;1;0;20250421003843383",
                "DOC": "True",
                "PATNAME": "True",
                "SECTNO": "心臟科",
                "order": [
                    {
                        "CTYPE": "自費",
                        "NAME": "Moriamin-SN inj. 200ml",
                        "CODE": "OMIF",
                        "HI_CODE": "AC24029263",
                        "TYPE": "膜衣錠",
                        "ATC": "B05BA01",
                        "LICENSE": "",
                        "DIANAME": "Moriamin-SN 200ml",
                        "DRUGKIND": "4",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "21",
                        "SD": "3",
                        "DUNIT": "BTL"
                    },
{
                        "CTYPE": "自費",
                        "NAME": "Moriamin-SN inj. 200ml",
                        "CODE": "OMIF",
                        "HI_CODE": "AC24029263",
                        "TYPE": "膜衣錠",
                        "ATC": "B05BA01",
                        "LICENSE": "",
                        "DIANAME": "Moriamin-SN 200ml",
                        "DRUGKIND": "4",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "3",
                        "DUNIT": "BTL"
                    },
{
                        "CTYPE": "自費",
                        "NAME": "Moriamin-SN inj. 200ml",
                        "CODE": "OMIF",
                        "HI_CODE": "AC24029263",
                        "TYPE": "膜衣錠",
                        "ATC": "B05BA01",
                        "LICENSE": "",
                        "DIANAME": "Moriamin-SN 200ml",
                        "DRUGKIND": "4",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "3",
                        "DUNIT": "BTL"
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "Glutathione inj. 500mg",
                        "CODE": "IAGI2",
                        "HI_CODE": "",
                        "TYPE": "膜衣錠",
                        "ATC": "V03AB32",
                        "LICENSE": "",
                        "DIANAME": "Glutathione 500mg",
                        "DRUGKIND": "2",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "3",
                        "DUNIT": "MG"
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "Diphenhydramine 30mg 1ml",
                        "CODE": "IVEN",
                        "HI_CODE": "AC22049209",
                        "TYPE": "膜衣錠",
                        "ATC": "R06AA02",
                        "LICENSE": "",
                        "DIANAME": "Diphenhydramine 30mg 1ml",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "1",
                        "DUNIT": "MG"
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "(瓶裝) Sod. Chloride inj. 0.9% 500ml",
                        "CODE": "INS13",
                        "HI_CODE": "AA24516277",
                        "TYPE": "點滴",
                        "ATC": "B05XA03",
                        "LICENSE": "",
                        "DIANAME": "Sod. Chloride 0.9% 500ml(瓶裝)",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "1",
                        "DUNIT": "BTL"
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "KOP inj. 30mg/ml 1ml",
                        "CODE": "IKET3",
                        "HI_CODE": "AB47071209",
                        "TYPE": "注射藥",
                        "ATC": "M01AB15",
                        "LICENSE": "",
                        "DIANAME": "Ketorolac tromethamine 30mg/ml 1ml",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "30",
                        "DUNIT": "MG"
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "B-Complex inj. 1ml",
                        "CODE": "IBCO",
                        "HI_CODE": "NC00476209",
                        "TYPE": "注射藥",
                        "ATC": "B05XC",
                        "LICENSE": "",
                        "DIANAME": "Vit. B1/Vit. B2/Vit. B3/Vit. B6 60/3/30/3mg/ml 1ml",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "ST",
                        "DAYS": "1",
                        "SD": "1",
                        "DUNIT": "AMP"
                    }
                ]
            }
        ],
        "old_order": [
            {
                "MED_BAG_SN": "7;20250421;0001410815;1;STAT;IVD;1;0;20250421003843383",
                "DOC": "False",
                "PATNAME": "False",
                "CT_TIME": "2025/04/21 00:40:11",
                "SECTNO": "急診醫學科",
                "order": [
                    {
                        "CTYPE": "自費",
                        "NAME": "Diphenhydramine 30mg 1ml",
                        "CODE": "IVEN",
                        "HI_CODE": "AC22049209",
                        "TYPE": "注射藥",
                        "ATC": "R06AA02",
                        "LICENSE": "",
                        "DIANAME": "Diphenhydramine 30mg 1ml",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "",
                        "DUNIT": ""
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "(瓶裝) Sod. Chloride inj. 0.9% 500ml",
                        "CODE": "INS13",
                        "HI_CODE": "AA24516277",
                        "TYPE": "點滴",
                        "ATC": "B05XA03",
                        "LICENSE": "",
                        "DIANAME": "Sod. Chloride 0.9% 500ml(瓶裝)",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "",
                        "DUNIT": ""
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "KOP inj. 30mg/ml 1ml",
                        "CODE": "IKET3",
                        "HI_CODE": "AB47071209",
                        "TYPE": "注射藥",
                        "ATC": "M01AB15",
                        "LICENSE": "",
                        "DIANAME": "Ketorolac tromethamine 30mg/ml 1ml",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "",
                        "DUNIT": ""
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "Moriamin-SN inj. 200ml",
                        "CODE": "IAMI7",
                        "HI_CODE": "AC24029263",
                        "TYPE": "點滴",
                        "ATC": "B05BA01",
                        "LICENSE": "",
                        "DIANAME": "Moriamin-SN 200ml",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "",
                        "DUNIT": ""
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "Glutathione inj. 500mg",
                        "CODE": "IAGI2",
                        "HI_CODE": "",
                        "TYPE": "注射藥",
                        "ATC": "V03AB32",
                        "LICENSE": "",
                        "DIANAME": "Glutathione 500mg",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "STAT",
                        "DAYS": "1",
                        "SD": "",
                        "DUNIT": ""
                    },
                    {
                        "CTYPE": "自費",
                        "NAME": "B-Complex inj. 1ml",
                        "CODE": "IBCO",
                        "HI_CODE": "NC00476209",
                        "TYPE": "注射藥",
                        "ATC": "B05XC",
                        "LICENSE": "",
                        "DIANAME": "Vit. B1/Vit. B2/Vit. B3/Vit. B6 60/3/30/3mg/ml 1ml",
                        "DRUGKIND": "N",
                        "TXN_QTY": "1",
                        "FREQ": "ST",
                        "DAYS": "1",
                        "SD": "",
                        "DUNIT": ""
                    }
                ]
            }
        ]
    }
}

# 設定請求標頭
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

# 檢查回傳結果
if response.status_code == 200:
    # 解析回傳的 JSON 資料
    response_data = response.json()
    print("回傳資料：\n" + json.dumps(response_data, indent=4, ensure_ascii=False))
    print("response：\n" + response_data.get("response", "").replace("\\n", "\n"))

else:
    print("API 請求失敗，狀態碼：", response.status_code)
