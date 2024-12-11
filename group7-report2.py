import streamlit as st
import cv2
import numpy as np
import base64

# Fungsi untuk mengompres gambar
@st.cache_data
def compress_image(image, max_size=(800, 800)):
    """Mengompres gambar dengan menjaga rasio aspek"""
    h, w = image.shape[:2]
    ratio = min(max_size[0]/w, max_size[1]/h)
    new_size = (int(w*ratio), int(h*ratio))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

# Fungsi untuk mengkonversi gambar ke base64
def image_to_base64(image):
    """Konversi gambar OpenCV ke base64"""
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')

# CSS Kustom
def get_custom_css():
    return """
    <style>
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .transform-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #f4f4f4;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .image-wrapper {
        flex: 1;
        margin: 0 10px;
        text-align: center;
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .image-wrapper img {
        max-width: 100%;
        height: auto;
        border-radius: 5px;
    }
    .slider-container {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
    """

def main():
    # Tambahkan CSS Kustom
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Judul dengan HTML
    st.markdown('<h1 class="main-title">🖼️ Aplikasi Transformasi Gambar</h1>', unsafe_allow_html=True)

    # Sidebar untuk pengaturan
    with st.sidebar:
        st.header("📝 Pilih Transformasi")
        transform_type = st.radio(
            "Jenis Transformasi",
            ['Translasi', 'Rotasi', 'Skala', 'Distorsi']
        )

    # Unggah file
    unggah_file = st.file_uploader(
        "Unggah gambar dalam format JPEG atau PNG", 
        type=["jpg", "jpeg", "png"]
    )

    if unggah_file is not None:
        # Baca dan kompres gambar
        file_bytes = np.asarray(bytearray(unggah_file.read()), dtype=np.uint8)
        gambar_asli = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        gambar_asli = compress_image(gambar_asli)

        # Konversi gambar ke base64 untuk HTML
        base64_asli = image_to_base64(cv2.cvtColor(gambar_asli, cv2.COLOR_BGR2RGB))

        # HTML untuk menampilkan gambar dengan CSS
        html_content = f"""
        <div class="transform-container">
            <div class="image-wrapper">
                <h3>Gambar Asli</h3>
                <img src="data:image/png;base64,{base64_asli}" alt="Gambar Asli">
            </div>
        """

        # Transformasi dinamis
        if transform_type == 'Translasi':
            dx = st.slider("Translasi Horizontal (dx)", -200, 200, 50)
            dy = st.slider("Translasi Vertikal (dy)", -200, 200, 30)
            
            # Transformasi
            matriks_translasi = np.float32([[1, 0, dx], [0, 1, dy]])
            gambar_transformasi = cv2.warpAffine(gambar_asli, matriks_translasi, (gambar_asli.shape[1], gambar_asli.shape[0]))
            
            # Konversi gambar transformasi
            base64_transformasi = image_to_base64(cv2.cvtColor(gambar_transformasi, cv2.COLOR_BGR2RGB))
            
            # Tambahkan gambar transformasi ke HTML
            html_content += f"""
            <div class="image-wrapper">
                <h3>Gambar Translasi</h3>
                <img src="data:image/png;base64,{base64_transformasi}" alt="Gambar Translasi">
            </div>
        </div>
        """

        elif transform_type == 'Rotasi':
            sudut = st.slider("Sudut Rotasi (derajat)", -180, 180, 45)
            
            # Transformasi
            tengah = (gambar_asli.shape[1] // 2, gambar_asli.shape[0] // 2)
            matriks_rotasi = cv2.getRotationMatrix2D(tengah, sudut, 1.0)
            gambar_transformasi = cv2.warpAffine(gambar_asli, matriks_rotasi, (gambar_asli.shape[1], gambar_asli.shape[0]))
            
            # Konversi gambar transformasi
            base64_transformasi = image_to_base64(cv2.cvtColor(gambar_transformasi, cv2.COLOR_BGR2RGB))
            
            # Tambahkan gambar transformasi ke HTML
            html_content += f"""
            <div class="image-wrapper">
                <h3>Gambar Rotasi</h3>
                <img src="data:image/png;base64,{base64_transformasi}" alt="Gambar Rotasi">
            </div>
        </div>
        """

        elif transform_type == 'Skala':
            skala_x = st.slider("Skala Horizontal", 0.5, 3.0, 1.5)
            skala_y = st.slider("Skala Vertikal", 0.5, 3.0, 1.5)
            
            # Transformasi
            gambar_transformasi = cv2.resize(gambar_asli, None, fx=skala_x, fy=skala_y, interpolation=cv2.INTER_LINEAR)
            
            # Konversi gambar transformasi
            base64_transformasi = image_to_base64(cv2.cvtColor(gambar_transformasi, cv2.COLOR_BGR2RGB))
            
            # Tambahkan gambar transformasi ke HTML
            html_content += f"""
            <div class="image-wrapper">
                <h3>Gambar Skala</h3>
                <img src="data:image/png;base64,{base64_transformasi}" alt="Gambar Skala">
            </div>
        </div>
        """

        elif transform_type == 'Distorsi':
            skew_x = st.slider("Distorsi Horizontal", 0.0, 2.0, 1.5)
            skew_y = st.slider("Distorsi Vertikal", 0.0, 2.0, 0.5)
            
            # Transformasi
            h, w = gambar_asli.shape[:2]
            pts1 = np.float32([[0,0], [w-1,0], [0,h-1], [w-1,h-1]])
            pts2 = np.float32([[0,0], 
                               [w-1,0], 
                               [skew_x*w,h-1], 
                               [(1+skew_y)*w-1,h-1]])
            matriks_distorsi = cv2.getPerspectiveTransform(pts1, pts2)
            gambar_transformasi = cv2.warpPerspective(gambar_asli, matriks_distorsi, (w, h))
            
            # Konversi gambar transformasi
            base64_transformasi = image_to_base64(cv2.cvtColor(gambar_transformasi, cv2.COLOR_BGR2RGB))
            
            # Tambahkan gambar transformasi ke HTML
            html_content += f"""
            <div class="image-wrapper">
                <h3>Gambar Distorsi</h3>
                <img src="data:image/png;base64,{base64_transformasi}" alt="Gambar Distorsi">
            </div>
        </div>
        """

        # Tampilkan HTML
        st.markdown(html_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
