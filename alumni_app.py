import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import os

# Configure page
st.set_page_config(
    page_title="Database Alumni Matematika FMIPA UI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2563eb;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    .feature-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2563eb;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .alumni-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'alumni_data' not in st.session_state:
        st.session_state.alumni_data = load_excel_data()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'

@st.cache_data
def load_excel_data():
    """Load alumni data from uploaded Excel file"""
    try:
        # Try to read the uploaded Excel file
        df = pd.read_excel('C:/Users/Aliya Dwi Karina/Pictures/gui/Database_Alumni S1 Departemen Matematika FMIPA UI.xlsx', sheet_name='Data ')
        
        # Data cleaning and formatting
        df['NPM'] = df['NPM'].astype(str)
        df['Angkatan'] = df['Angkatan'].astype(str)
        df['Tahun Lulus'] = df['Tahun Lulus'].astype(str)
        
        # Remove any rows with missing critical data
        df = df.dropna(subset=['Nama', 'NPM'])
        
        return df
        
    except Exception as e:
        st.error(f"Error loading Excel file: {str(e)}")
        return create_fallback_data()

def create_fallback_data():
    """Create fallback sample data if Excel file can't be loaded"""
    sample_data = {
        'No': [1, 2, 3, 4, 5],
        'Nama': ['Sari Gita Fitri', 'Natasha Rosaline', 'Fadel Muhammad', 'Rina Susanti', 'Ahmad Fauzi'],
        'NPM': ['1606829390', '1606889793', '1606824540', '1606825441', '1606826542'],
        'Program Studi': ['Matematika', 'Matematika', 'Matematika', 'Statistika', 'Ilmu Aktuaria'],
        'Angkatan': ['2016', '2016', '2016', '2017', '2017'],
        'Peminatan': ['Matematika Komputasi', 'Matematika Komputasi', 'Matematika Komputasi', 'Statistika Komputasi', 'Aktuaria'],
        'Judul Skripsi': [
            'Implementasi Algoritma Kernel K-Means based Co-clustering untuk Memprediksi Penyakit Kanker Paru-paru',
            'Fuzzy C-Means Clustering dengan Reduksi Dimensi Deep Autoencoders untuk Pendeteksian Topik pada Data Tekstual Twitter',
            'Prediksi Insiden DBD di DKI Jakarta Menggunakan Radial Basis Function Neural Network',
            'Analisis Survival pada Data Pasien Kanker Menggunakan Model Cox Proportional Hazard',
            'Valuasi Premi Asuransi Jiwa Menggunakan Metode Stokastik'
        ],
        'Tahun Lulus': ['2020', '2020', '2020', '2021', '2021'],
        'Pekerjaan': ['Data Analyst', 'Senior Analyst Specialist System Infrastructure', 'Data Platform Engineer', 'Statistician', 'Actuarial Analyst'],
        'Id Karyawan': ['KI202001', 'BC202049', 'BR202070', 'GO202071', 'AL202072'],
        'Nama Perusahaan': ['Kimbo', 'PT Bank Central Asia Tbk', 'PT Bank Raya Indonesia', 'Google Indonesia', 'Allianz Indonesia'],
        'Alamat Perusahaan': [
            'Ruko Harco Mangga Dua, Jakarta',
            'Menara BCA lantai LG. Jl. MH. Thamrin no. 1 Jakarta Pusat 10310',
            'Jl. Jenderal Sudirman Kav.44-46, Jakarta 10210',
            'Equity Tower, SCBD Jakarta',
            'Allianz Tower, Jl. HR Rasuna Said Jakarta'
        ],
        'Rata-rata Gaji': [8000000, 15000000, 12000000, 18000000, 16000000]
    }
    return pd.DataFrame(sample_data)

def format_currency(amount):
    """Format currency to Rupiah"""
    if pd.isna(amount) or amount == '':
        return 'Tidak tersedia'
    try:
        if isinstance(amount, str) and amount.startswith('Rp'):
            return amount
        num_amount = int(float(amount))
        return f"Rp{num_amount:,}".replace(',', '.') + ",00"
    except:
        return str(amount)

def show_welcome_page():
    """Display welcome page"""
    st.markdown('<h1 class="main-header">🎓 Database Alumni</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Departemen Matematika FMIPA UI</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <p style="font-size: 1.2rem; color: #6b7280;">
        Sistem informasi terintegrasi untuk mengelola data alumni<br>
        Sarjana Matematika, Statistika, dan Ilmu Aktuaria
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    data = st.session_state.alumni_data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎓 Total Alumni", len(data))
    with col2:
        st.metric("📚 Program Studi", data['Program Studi'].nunique())
    with col3:
        st.metric("🏢 Perusahaan", data['Nama Perusahaan'].nunique())
    with col4:
        avg_salary = data['Rata-rata Gaji'].mean() if 'Rata-rata Gaji' in data.columns else 0
        st.metric("💰 Rata-rata Gaji", format_currency(avg_salary))
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Pencarian Alumni</h3>
            <p>Cari dan filter data alumni berdasarkan berbagai kriteria seperti nama, program studi, perusahaan, dan gaji</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Analisis Statistik</h3>
            <p>Visualisasi data karir alumni, distribusi program studi, dan tren gaji dengan grafik interaktif</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>➕ Manajemen Data</h3>
            <p>Tambah data alumni baru, upload file Excel/CSV, dan download laporan data</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Start button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Mulai Eksplorasi Data", type="primary"):
            st.session_state.current_page = 'search'
            st.rerun()

def show_search_page():
    """Display search and data page"""
    st.markdown('<h1 class="main-header">🔍 Pencarian Alumni</h1>', unsafe_allow_html=True)
    
    data = st.session_state.alumni_data
    
    # Search filters
    with st.expander("🔍 Filter Pencarian", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nama_filter = st.text_input("Nama Alumni")
            pekerjaan_filter = st.text_input("Pekerjaan")
        
        with col2:
            program_options = ["Semua"] + sorted(data['Program Studi'].dropna().unique().tolist())
            program_filter = st.selectbox("Program Studi", program_options)
            
            perusahaan_filter = st.text_input("Nama Perusahaan")
        
        with col3:
            npm_filter = st.text_input("NPM")
            
            col3a, col3b = st.columns(2)
            with col3a:
                gaji_min = st.number_input("Gaji Min (Rp)", min_value=0, step=1000000, format="%d")
            with col3b:
                gaji_max = st.number_input("Gaji Max (Rp)", min_value=0, step=1000000, format="%d")
    
    # Apply filters
    filtered_data = data.copy()
    
    if nama_filter:
        filtered_data = filtered_data[filtered_data['Nama'].str.contains(nama_filter, case=False, na=False)]
    
    if program_filter != "Semua":
        filtered_data = filtered_data[filtered_data['Program Studi'] == program_filter]
    
    if npm_filter:
        filtered_data = filtered_data[filtered_data['NPM'].str.contains(npm_filter, na=False)]
    
    if pekerjaan_filter:
        filtered_data = filtered_data[filtered_data['Pekerjaan'].str.contains(pekerjaan_filter, case=False, na=False)]
    
    if perusahaan_filter:
        filtered_data = filtered_data[filtered_data['Nama Perusahaan'].str.contains(perusahaan_filter, case=False, na=False)]
    
    if gaji_min > 0:
        filtered_data = filtered_data[filtered_data['Rata-rata Gaji'] >= gaji_min]
    
    if gaji_max > 0:
        filtered_data = filtered_data[filtered_data['Rata-rata Gaji'] <= gaji_max]
    
    # Results
    st.markdown(f"### 📋 Hasil Pencarian ({len(filtered_data)} dari {len(data)} alumni)")
    
    if len(filtered_data) > 0:
        # Show summary stats for filtered data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Alumni Ditemukan", len(filtered_data))
        with col2:
            if len(filtered_data) > 0:
                avg_gaji_filtered = filtered_data['Rata-rata Gaji'].mean()
                st.metric("💰 Rata-rata Gaji", format_currency(avg_gaji_filtered))
        with col3:
            if len(filtered_data) > 0:
                top_program = filtered_data['Program Studi'].mode().iloc[0] if not filtered_data['Program Studi'].mode().empty else "N/A"
                st.metric("📚 Program Terpopuler", top_program)
        
        # Format display data
        display_data = filtered_data.copy()
        display_data['Rata-rata Gaji Formatted'] = display_data['Rata-rata Gaji'].apply(format_currency)
        
        # Show data table
        st.dataframe(
            display_data[['Nama', 'NPM', 'Program Studi', 'Angkatan', 'Pekerjaan', 'Nama Perusahaan', 'Rata-rata Gaji Formatted']],
            use_container_width=True,
            hide_index=True,
            column_config={
                'Nama': 'Nama Alumni',
                'NPM': 'NPM',
                'Program Studi': 'Program Studi',
                'Angkatan': 'Angkatan',
                'Pekerjaan': 'Pekerjaan',
                'Nama Perusahaan': 'Perusahaan',
                'Rata-rata Gaji Formatted': 'Gaji'
            }
        )
        
        # Alumni detail selection
        st.markdown("### 👤 Detail Alumni")
        selected_name = st.selectbox(
            "Pilih alumni untuk melihat detail lengkap:",
            ["Pilih alumni..."] + filtered_data['Nama'].tolist()
        )
        
        if selected_name != "Pilih alumni...":
            show_alumni_detail(selected_name)
    else:
        st.warning("Tidak ada data alumni yang sesuai dengan filter pencarian.")
        st.info("💡 Tip: Coba kurangi atau hapus beberapa filter untuk memperluas hasil pencarian.")

def show_alumni_detail(nama):
    """Show detailed information for selected alumni"""
    alumni = st.session_state.alumni_data[st.session_state.alumni_data['Nama'] == nama].iloc[0]
    
    st.markdown(f"#### 🎓 {alumni['Nama']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 Informasi Pribadi**")
        st.write(f"📝 **NPM:** {alumni['NPM']}")
        st.write(f"🎯 **Program Studi:** {alumni['Program Studi']}")
        st.write(f"📅 **Angkatan:** {alumni['Angkatan']}")
        st.write(f"🔬 **Peminatan:** {alumni['Peminatan']}")
        st.write(f"🎓 **Tahun Lulus:** {alumni['Tahun Lulus']}")
        
        with st.expander("📖 Judul Skripsi"):
            st.write(alumni['Judul Skripsi'])
    
    with col2:
        st.markdown("**💼 Informasi Karir**")
        st.write(f"💼 **Pekerjaan:** {alumni['Pekerjaan']}")
        st.write(f"🏢 **Perusahaan:** {alumni['Nama Perusahaan']}")
        st.write(f"🆔 **ID Karyawan:** {alumni['Id Karyawan']}")
        st.write(f"💰 **Gaji:** {format_currency(alumni['Rata-rata Gaji'])}")
        
        with st.expander("📍 Alamat Perusahaan"):
            st.write(alumni['Alamat Perusahaan'])

def show_statistics_page():
    """Display statistics page"""
    st.markdown('<h1 class="main-header">📊 Statistik Alumni</h1>', unsafe_allow_html=True)
    
    data = st.session_state.alumni_data
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎓 Total Alumni", len(data))
    
    with col2:
        st.metric("📚 Program Studi", data['Program Studi'].nunique())
    
    with col3:
        st.metric("🏢 Total Perusahaan", data['Nama Perusahaan'].nunique())
    
    with col4:
        avg_salary = data['Rata-rata Gaji'].mean()
        st.metric("💰 Rata-rata Gaji", format_currency(avg_salary))
    
    # Additional metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        min_salary = data['Rata-rata Gaji'].min()
        st.metric("💵 Gaji Terendah", format_currency(min_salary))
    
    with col2:
        max_salary = data['Rata-rata Gaji'].max()
        st.metric("💎 Gaji Tertinggi", format_currency(max_salary))
    
    with col3:
        angkatan_range = f"{data['Angkatan'].min()}-{data['Angkatan'].max()}"
        st.metric("📅 Rentang Angkatan", angkatan_range)
    
    with col4:
        avg_tahun_lulus = int(data['Tahun Lulus'].astype(int).mean())
        st.metric("🎓 Rata-rata Lulus", avg_tahun_lulus)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Distribusi Program Studi")
        program_counts = data['Program Studi'].value_counts()
        fig1 = px.pie(
            values=program_counts.values,
            names=program_counts.index,
            title="Distribusi Alumni per Program Studi",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### 📅 Distribusi Angkatan")
        angkatan_counts = data['Angkatan'].value_counts().sort_index()
        fig2 = px.bar(
            x=angkatan_counts.index,
            y=angkatan_counts.values,
            title="Jumlah Alumni per Angkatan",
            labels={'x': 'Angkatan', 'y': 'Jumlah Alumni'},
            color=angkatan_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Salary analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Distribusi Gaji")
        fig3 = px.histogram(
            data,
            x='Rata-rata Gaji',
            title="Distribusi Gaji Alumni",
            nbins=15,
            labels={'Rata-rata Gaji': 'Gaji (Rp)', 'count': 'Jumlah Alumni'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Gaji per Program Studi")
        fig4 = px.box(
            data,
            x='Program Studi',
            y='Rata-rata Gaji',
            title="Distribusi Gaji per Program Studi"
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Top companies
    st.markdown("### 🏆 Top Perusahaan")
    company_counts = Counter(data['Nama Perusahaan'].dropna())
    top_companies = company_counts.most_common(10)
    
    if top_companies:
        companies_df = pd.DataFrame(top_companies, columns=['Perusahaan', 'Jumlah Alumni'])
        companies_df['Persentase'] = (companies_df['Jumlah Alumni'] / len(data) * 100).round(1)
        
        fig5 = px.bar(
            companies_df,
            x='Jumlah Alumni',
            y='Perusahaan',
            orientation='h',
            title="Top 10 Perusahaan dengan Alumni Terbanyak",
            text='Jumlah Alumni'
        )
        fig5.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig5, use_container_width=True)
        
        # Show detailed table
        st.dataframe(companies_df, use_container_width=True, hide_index=True)
    
    # Peminatan analysis
    st.markdown("### 🔬 Analisis Peminatan")
    peminatan_counts = data['Peminatan'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig6 = px.bar(
            x=peminatan_counts.values,
            y=peminatan_counts.index,
            orientation='h',
            title="Distribusi Alumni per Peminatan"
        )
        fig6.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        # Salary by peminatan
        peminatan_salary = data.groupby('Peminatan')['Rata-rata Gaji'].mean().sort_values(ascending=False)
        fig7 = px.bar(
            x=peminatan_salary.values,
            y=peminatan_salary.index,
            orientation='h',
            title="Rata-rata Gaji per Peminatan"
        )
        fig7.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig7, use_container_width=True)

def show_add_form():
    """Show form to add new alumni data"""
    st.markdown('<h1 class="main-header">➕ Tambah Data Alumni</h1>', unsafe_allow_html=True)
    
    with st.form("add_alumni_form"):
        st.markdown("### 👤 Informasi Pribadi")
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Lengkap*", placeholder="Contoh: Sari Gita Fitri")
            npm = st.text_input("NPM*", placeholder="Contoh: 1606829390")
        
        with col2:
            program_studi = st.selectbox("Program Studi*", ["Matematika", "Statistika", "Ilmu Aktuaria"])
            angkatan = st.text_input("Angkatan", placeholder="Contoh: 2016")
        
        st.markdown("### 📚 Informasi Pendidikan")
        col1, col2 = st.columns(2)
        
        with col1:
            # Get unique peminatan options from existing data
            existing_peminatan = st.session_state.alumni_data['Peminatan'].dropna().unique().tolist()
            peminatan_options = sorted(set(existing_peminatan + ["Matematika Komputasi", "Matematika Murni", "Matematika Statistik", "Operational Research", "Aktuaria"]))
            peminatan = st.selectbox("Peminatan", peminatan_options)
            tahun_lulus = st.text_input("Tahun Lulus", placeholder="Contoh: 2020")
        
        with col2:
            judul_skripsi = st.text_area("Judul Skripsi", placeholder="Masukkan judul skripsi...")
        
        st.markdown("### 💼 Informasi Karir")
        col1, col2 = st.columns(2)
        
        with col1:
            pekerjaan = st.text_input("Pekerjaan", placeholder="Contoh: Data Analyst")
            nama_perusahaan = st.text_input("Nama Perusahaan", placeholder="Contoh: PT XYZ")
            id_karyawan = st.text_input("ID Karyawan", placeholder="Contoh: KI202001")
        
        with col2:
            alamat_perusahaan = st.text_area("Alamat Perusahaan", placeholder="Alamat lengkap perusahaan...")
            gaji = st.number_input("Rata-rata Gaji (Rp)", min_value=0, step=100000)
        
        # Submit button
        submitted = st.form_submit_button("💾 Simpan Data Alumni", type="primary")
        
        if submitted:
            # Validate required fields
            if not nama or not npm or not program_studi:
                st.error("❌ Harap isi semua field yang wajib (*)")
            else:
                # Create new alumni record
                new_alumni = {
                    'No': len(st.session_state.alumni_data) + 1,
                    'Nama': nama,
                    'NPM': npm,
                    'Program Studi': program_studi,
                    'Angkatan': angkatan,
                    'Peminatan': peminatan,
                    'Judul Skripsi': judul_skripsi,
                    'Tahun Lulus': tahun_lulus,
                    'Pekerjaan': pekerjaan,
                    'Id Karyawan': id_karyawan,
                    'Nama Perusahaan': nama_perusahaan,
                    'Alamat Perusahaan': alamat_perusahaan,
                    'Rata-rata Gaji': gaji
                }
                
                # Add to dataframe
                new_row = pd.DataFrame([new_alumni])
                st.session_state.alumni_data = pd.concat([st.session_state.alumni_data, new_row], ignore_index=True)
                
                st.success("✅ Data alumni berhasil ditambahkan!")
                st.balloons()

def main():
    """Main application function"""
    init_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/150x100/2563eb/ffffff?text=FMIPA+UI", use_column_width=True)
        st.markdown("### 🎓 Database Alumni")
        st.markdown("**Matematika FMIPA UI**")
        
        st.markdown("---")
        
        # Navigation menu
        menu_options = {
            "🏠 Beranda": "welcome",
            "🔍 Pencarian Alumni": "search", 
            "📊 Statistik": "statistics",
            "➕ Tambah Data": "add_form"
        }
        
        for label, page in menu_options.items():
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # Data management
        st.markdown("### 📁 Manajemen Data")
        
        # Download data as CSV
        if st.button("📥 Download Data CSV", use_container_width=True):
            csv = st.session_state.alumni_data.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv,
                file_name="alumni_data.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Download data as Excel
        if st.button("📊 Download Data Excel", use_container_width=True):
            # This would create an Excel file download
            st.info("💡 Feature Excel download sedang dalam pengembangan")
        
        # File upload
        uploaded_file = st.file_uploader("📤 Upload Excel/CSV", type=['xlsx', 'csv'])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file, sheet_name='Data ')
                else:
                    df = pd.read_csv(uploaded_file)
                
                st.session_state.alumni_data = df
                st.success("✅ Data berhasil diupload!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Show current data info
        st.markdown("### 📊 Info Data Saat Ini")
        data = st.session_state.alumni_data
        st.metric("Total Alumni", len(data))
        st.metric("Program Studi", data['Program Studi'].nunique())
        
        # Quick stats
        if len(data) > 0:
            st.markdown("**📈 Statistik Cepat:**")
            st.write(f"• Angkatan: {data['Angkatan'].min()}-{data['Angkatan'].max()}")
            st.write(f"• Rata-rata Gaji: {format_currency(data['Rata-rata Gaji'].mean())}")
            
            # Top company
            top_company = data['Nama Perusahaan'].mode().iloc[0] if not data['Nama Perusahaan'].mode().empty else "N/A"
            st.write(f"• Perusahaan Populer: {top_company}")
    
    # Main content
    if st.session_state.current_page == "welcome":
        show_welcome_page()
    elif st.session_state.current_page == "search":
        show_search_page()
    elif st.session_state.current_page == "statistics":
        show_statistics_page()
    elif st.session_state.current_page == "add_form":
        show_add_form()

if __name__ == "__main__":
    main()