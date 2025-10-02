import requests
import base64

# ⚠️ 替换为你自己的 API Key（在 https://aistudio.google.com/app/apikey 生成）
API_KEY = "YOUR_API_KEY_HERE"

# 1) 列出可用模型
def list_models():
    url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
    res = requests.get(url)
    if res.status_code == 200:
        models = [m["name"] for m in res.json().get("models", [])]
        print("✅ 可用模型:")
        for m in models:
            print("  -", m)
    else:
        print("❌ 获取模型列表失败:", res.text)

# 2) OCR 图片 → 提取文字
def ocr_image(image_path, model="models/gemini-1.5-pro"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

    # 读取图片并转 base64
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "请从这张图片中提取所有文字"},
                    {"inline_data": {"mime_type": "image/png", "data": image_b64}}
                ]
            }
        ]
    }

    res = requests.post(url, json=payload)
    if res.status_code == 200:
        data = res.json()
        output_text = data["candidates"][0]["content"]["parts"][0]["text"]
        print("📖 OCR 结果:\n", output_text)
    else:
        print("❌ 请求失败:", res.text)


if __name__ == "__main__":
    # Step 1: 列出模型
    list_models()

    # Step 2: OCR 测试
    # ocr_image("test.png", model="models/gemini-1.5-pro")
