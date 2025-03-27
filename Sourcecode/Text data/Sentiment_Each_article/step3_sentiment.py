import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ✅ Load model và tokenizer từ Hugging Face
model_name = "mr4/phobert-base-vi-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

df = pd.read_csv("data2.csv")
batch_size = 128
texts = df["processed_title"].astype(str).tolist()
sentiments = []  # Danh sách lưu kết quả dự đoán cảm xúc


for i in range(0, len(texts), batch_size):
    batch_texts = texts[i : i + batch_size]  # Chia batch
    inputs = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    labels = ["negative", "neutral", "positive"]
    batch_sentiments = [labels[i] for i in torch.argmax(probs, dim=-1).tolist()]
    sentiments.extend(batch_sentiments)
    df.loc[i:i + batch_size - 1, "sentiment"] = batch_sentiments
    df.to_csv("news_with_sentiment_temp.csv", index=False)  # Lưu tạm thời
    print(f"✅ Đã xử lý {min(i+batch_size, len(texts))}/{len(texts)} dòng...")

# ✅ Lưu file kết quả cuối cùng
df.to_csv("vietstock_sen.csv", index=False)

print("🎉 Hoàn thành! File kết quả đã được lưu vào 'news_with_sentiment.csv'.")
