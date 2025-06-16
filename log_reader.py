import json
import tkinter as tk
from tkinter import filedialog
import cv2
from pyzbar.pyzbar import decode

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="請選擇含 QR Code 的圖片",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    return file_path

def extract_qrcode_raw(image_path):
    img = cv2.imread(image_path)
    qr_codes = decode(img)
    if not qr_codes:
        return None
    return qr_codes[0].data.decode("utf-8")  # 直接取 QR 原始字串

def find_log_by_med_bag_sn(log_file_path, med_bag_sn):
    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                if log_entry.get("藥袋編號") == med_bag_sn:
                    return log_entry
            except json.JSONDecodeError:
                continue
    return None

def main():
    image_path = select_image()
    if not image_path:
        print("❌ 未選擇圖片")
        return

    med_bag_sn = extract_qrcode_raw(image_path)
    if not med_bag_sn:
        print("❌ 無法從 QR Code 中解析出原始內容")
        return

    print(f"🔍 掃描到藥袋編號（原始內容）：{med_bag_sn}")

    log_entry = find_log_by_med_bag_sn("log_output.txt", med_bag_sn)
    if log_entry:
        print("\n✅ 對應 log 資料如下：\n")
        print(json.dumps(log_entry, ensure_ascii=False, indent=2))
    else:
        print("❌ 查無對應藥袋編號的 log 記錄")

if __name__ == "__main__":
    main()
