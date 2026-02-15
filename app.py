import os
from flask import Flask, render_template, request
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import PyPDF2
import docx

app = Flask(__name__)

# 1. Load Model
model_path = r"C:\Users\BINTANG\Desktop\WEB Programming\Mini Project\Text Summarization Web\pegasus_model"
print("Load AI Model...")
tokenizer = PegasusTokenizer.from_pretrained(model_path)
model = PegasusForConditionalGeneration.from_pretrained(model_path)

# --- FUNGSI EKSTRAKSI TEKS ---
def extract_text_from_file(file):
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    elif filename.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    return ""

# --- FUNGSI GENERATE (DENGAN CHUNKING) ---
def generate_summary(text):
    # Tentukan batas karakter per bagian (misal 3000 karakter agar tidak overload)
    chunk_size = 3000 
    # Pecah teks menjadi potongan-potongan kecil
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    partial_summaries = []
    
    for chunk in chunks:
        # Tokenisasi tiap chunk
        inputs = tokenizer(chunk, truncation=True, padding="longest", return_tensors="pt")
        
        # Generate ringkasan untuk chunk tersebut
        summary_ids = model.generate(
            inputs["input_ids"], 
            max_length=150,
            min_length=30, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )
        
        # Decode dan simpan
        decoded = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        partial_summaries.append(decoded)
    
    # Gabungkan semua potongan ringkasan menjadi satu paragraf utuh
    return " ".join(partial_summaries)


@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    original_text = ""
    
    if request.method == "POST":
        # Cek apakah ada file yang diunggah
        file = request.files.get('file_input')
        
        if file and file.filename != '':
            # Jika ada file, ekstrak teksnya
            original_text = extract_text_from_file(file)
        else:
            # Jika tidak ada file, ambil dari input text area
            original_text = request.form.get("content", "")

        if original_text.strip():
            # Jalankan fungsi ringkasan (yang sudah mendukung chunking)
            summary = generate_summary(original_text)
            
    return render_template("index.html", original_text=original_text, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)