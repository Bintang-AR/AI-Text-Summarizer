// Fungsi untuk membersihkan teks dan input file
function clearAll() {
    document.getElementById("textAreaInput").value = "";
    document.querySelector("input[type='file']").value = "";
    document.getElementById("outputBox").innerHTML = '<span class="placeholder-text">Hasil ringkasan akan muncul di sini...</span>';
}

// Fungsi copy to clipboard
function copyToClipboard() {
    const text = document.getElementById("summaryResult").innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert("Ringkasan berhasil disalin!");
    });
}

// Event saat form dikirim
document.getElementById("summaryForm").addEventListener("submit", function(e) {
    const btn = document.getElementById("submitBtn");
    const outputBox = document.getElementById("outputBox");
    
    // Ubah tampilan tombol menjadi loading
    btn.disabled = true;
    btn.innerHTML = "Sedang Memproses...";

    // Tampilkan loading di kotak output
    outputBox.innerHTML = `
        <div class="loading-text">
            <div class="loader"></div> 
            <span>AI sedang membaca & meringkas dokumenmu...</span>
        </div>
    `;
});