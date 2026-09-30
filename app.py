
import streamlit as st
st.image("logo.jpg")
# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 Ứng dụng tính lãi tiền gửi tiết kiệm")
st.write("Tính tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin tiền gửi")

so_tien = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

loai_lai = st.selectbox(
    "🔢 Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# ==============================
# NÚT TÍNH
# ==============================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r = lai_suat / 100

    # Thời gian tính theo năm
    so_nam = ky_han / 12

    # ==============================
    # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
    # ==============================
    if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
        so_ky = ky_han
        lai_suat_ky = r / 12
        ten_ky = "tháng"

    elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
        so_ky = ky_han / 3
        lai_suat_ky = r / 4
        ten_ky = "quý"

    else:
        so_ky = 1
        lai_suat_ky = r
        ten_ky = "kỳ hạn"

    # ==============================
    # TÍNH LÃI
    # ==============================
    if loai_lai == "Lãi đơn":

        # Công thức:
        # I = P * r * t
        tong_tien_lai = so_tien * r * so_nam

        # Lãi của mỗi kỳ
        lai_dinh_ky = tong_tien_lai / so_ky

        # Với lãi đơn, tiền gốc không cộng dồn vào kỳ sau
        tong_goc_lai = so_tien + tong_tien_lai

        cong_thuc = "I = P × r × t"

    else:

        # Lãi kép
        # FV = P × (1 + r)^n
        tong_goc_lai = so_tien * (1 + lai_suat_ky) ** so_ky

        tong_tien_lai = tong_goc_lai - so_tien

        # Lãi của kỳ đầu tiên
        lai_dinh_ky = so_tien * lai_suat_ky

        cong_thuc = "FV = P × (1 + r)ⁿ"

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.success("✅ Đã tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Tiền lãi định kỳ",
            f"{lai_dinh_ky:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            f"{tong_tien_lai:,.0f} VNĐ"
        )

    st.metric(
        "💵 Tổng tiền gốc + lãi",
        f"{tong_goc_lai:,.0f} VNĐ"
    )

    st.divider()

    # ==============================
    # CHI TIẾT
    # ==============================
    st.subheader("📝 Chi tiết khoản tiền gửi")

    st.write(f"**Số tiền gửi:** {so_tien:,.0f} VNĐ")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức tính:** {loai_lai}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_lanh}")
    st.write(f"**Số kỳ:** {so_ky:g} {ten_ky}")

    st.info(f"📐 **Công thức:** {cong_thuc}")

    # ==============================
    # BẢNG KẾT QUẢ
    # ==============================
    st.subheader("📋 Bảng tổng hợp")

    ket_qua = {
        "Nội dung": [
            "Tiền gốc",
            "Tiền lãi định kỳ",
            "Tổng tiền lãi",
            "Tổng gốc + lãi"
        ],
        "Số tiền (VNĐ)": [
            f"{so_tien:,.0f}",
            f"{lai_dinh_ky:,.0f}",
            f"{tong_tien_lai:,.0f}",
            f"{tong_goc_lai:,.0f}"
        ]
    }

    st.table(ket_qua)

    # ==============================
    # LƯU Ý
    # ==============================
    if loai_lai == "Lãi kép":
        st.caption(
            "ℹ️ Với lãi kép, tiền lãi của mỗi kỳ được cộng vào vốn "
            "để tiếp tục tính lãi cho kỳ tiếp theo."
        )
    else:
        st.caption(
            "ℹ️ Với lãi đơn, tiền lãi được tính trên số tiền gốc ban đầu "
            "và không cộng dồn vào vốn."
        )

