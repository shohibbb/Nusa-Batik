document.addEventListener('DOMContentLoaded', function () {
    var namabatik = document.getElementById('namabatik');
    var articleButton = document.getElementById('article-button');
    var backButton = document.getElementById('backButton');
    if (highestPercentage < 60) {
        articleButton.textContent = 'Coba Gambar Lain';
        backButton.textContent = 'Baca Artikel';
        namabatik.parentNode.removeChild(namabatik);
        document.getElementById('model-prediksi').innerHTML = "<h4>Gagal mendeteksi motif batik</h4>";
        document.getElementById('prediction-list').innerHTML = "<h5>Gambar tidak valid, persentase prediksi terlalu rendah</h5>";
        document.getElementById('percentage').innerHTML = "<p>maaf sepertinya, motif ini belum ada di pengembangan Nusa Batik. Untuk itu akan kami tambahkan sebagai upaya memperluas jangkauan edukasi</p>";

        document.getElementById("backButton").onclick = function () {
            window.location.href = "/article";
        };
        document.getElementById("article-button").onclick = function () {
            window.location.href = "/";
        };
    }
    else {
        document.getElementById("backButton").onclick = function () {
            window.location.href = "/";
        };
        document.getElementById("article-button").onclick = function () {
            window.location.href = "/article/" + prediction;
        };        
    }
});