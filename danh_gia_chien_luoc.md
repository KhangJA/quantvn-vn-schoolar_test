# Đánh giá chiến lược

## Mô tả về chiến lực
- **Thị Trường**: Cổ phiếu VN (Phái sinh VN30F) vào khung thời gian M5
- **Lý do**: Theo như tìm hiểu thì thị trường:
  - **Thứ nhất:** Thị trường có tính thanh khoản cao hơn so với thị trường chứng khoản cơ sở thông thường và giá thì luôn bám sát chỉ sổ VN30 cơ sở.
  - **Thứ hai:** Thị trường khung M5 không bị nhiễu nhiều tín hiệu và vừa đủ thời gian không quá ngắn cũng không quá dài để bot vào lệnh.

## Chiến lực Final_Strategy_J
- **Lúc đầu** em lên ý tưởng với việc cơ bản là sử dụng chỉ báo **RSI + RSI Phân kỳ + EMA** để đu theo sóng nhưng do hiệu suất không được tốt và gặp nhiều lỗi trong việc làm cho entry bị quá khắt khe nên bot bị treo và hiệu suất ko đạt được như mong muốn.

- **Hiệu suất chiến lược ban đầu lên ý tưởng**

<br>
<div align="center">
  <img src="https://res.cloudinary.com/deb0bx7dp/image/upload/v1780398097/16cf7df7-60bd-4469-8340-d3e5fbc479d8_bfdg7p.png" width="500">
</div> </br>

- **Cuối cùng**, sau khi tìm hiểu thử một số các chiến lược thì biết đến chiến lược **Momentum Strategy của Spencer Pao** là việc sử dụng 4 chỉ báo gồm có **RSI + MACD + ROC + Stochastic Oscillator**. Nhưng chiến lược của **Spencer Pao** được dùng cho cổ phiếu Mỹ và trong khung h lớn từ H1 trở lên nên chỉ báo có thể đưa ra những signal không phù hợp với phái sinh VN30 khung M5 nên phải điều chỉnh lại.

## Chi tiết và Logic của Chiến Lược
- Sử dụng **RSI + MACD + ROC + Stochastic Oscillator** + Hệ thống khi có 3/4 chỉ báo cùng chỉ hướng.
  - Tín hiệu **LONG**:
    - Khi **RSI** > **50**.
    - Khi **Stochastic %D** > **50** (%D chỉ báo làm mịn của %K).
    - Khi **ROC** > **0.05%**.
    - Khi **MACD** đưa ra tín hiệu **tăng**.
    - ⟹ Mỗi tín hiệu + 1 điểm chứa trong `df['Bull_Score']`.
  - Tín hiệu **SHORT**:
    -  Khi **RSI** < **50**.
    -  Khi **Stochastic %D** < **50** (%D chỉ báo làm mịn của %K).
    -  Khi  **ROC** < **0.05%**.
    -  Khi **MACD** đưa ra tín hiệu **giảm**.
  - ⟹ Mỗi tín hiệu + 1 điểm chứa trong `df['Bearish_Score']`
  - ⟹ Nếu **`df['Bull_Score']`** hoặc **`df['Bearish_Score']`** >= 3 thì tạo signal **LONG** hoặc **SHORT**, Ngược lại nếu chỉ có 2/4 hoặc nhỏ hơn thì ở ngoài.
## Hiệu suất
<div align="center">
  <img src="https://res.cloudinary.com/deb0bx7dp/image/upload/v1780481178/z7896625344660_3fe718d875569edd983220cff37b5275_ndpjsm.jpg" width="600">
</div>

## Điểm Mạnh:
- Ở khung thời gian M5 so với M15 trên dữ liệu backtest hiệu suất thì:
  + **1**: Max Drawdown tốt hơn nhiều với chỉ dưới **19%**.
  + **2**: Hệ số Calmar tốt hơn do Max Drawdown nhỏ nên giá trị lên tới gần trên **100**.
- **Winrate** có chiến lược tốt với winrate tỉ lệ trên **50%**.
- **Hiệu suất** trên data **out-of-sample** và **historical** tương đối cao và không có nhiều chênh lệch về lợi nhuận, drawdown và tỉ lệ Sharpe.
## Điểm Yếu & Rủi Ro:
- Chiến lược vẫn chưa tối ưu cho khung bé hơn như khung M1 để có thể đạt được hiệu suất cao, lý do:
  + **1**: Các chỉ báo đang sử dụng cho chiến thuật còn khá chậm không phù hợp cho những việc giá di chuyển nhanh và giật lên xuống liên tục.
  + **2**: Chênh lệch giữa lợi nhuận trên **Fees** và **Raw** lúc đầu thì không rõ rệt nhưng dần dần qua thời gian thì khoảng cách giữa 2 đồ thị dần xa càng lớn hơn (Vẫn còn rất yếu khi so chênh lệch lợi nhuận phí với QuantVN Team's Strategy và của top server leaderboard).
  + **3**: Chưa có logic để set **TP/SL** rõ ràng nên khi trade thực chiến có khả năng là bot giữ lệnh mãi mãi cho đến khi đóng phiên khả năng bị drawdown cao ().
  + **4**: Các chỉ số hiệu suất vẫn còn chưa ổn ở một số phần:
    + **Độ biến động** vẫn còn cao (±16%) có thể thấy đc nhiều đường gồ ghề trên đường lợi nhuận ⟹ cho thấy số lượng lệnh trade còn khá nhiều, khả năng có thể có nhiều lệnh thua trong ngày
    + **Xác xuất phá sản** vẫn còn khá cao trên 1%.

## Đề xuất cải thiện
+ Tìm hiểu thêm về các phương pháp tối ưu làm **giảm nhiễu tín hiệu** cho những khung h nhỏ hơn như **M1**.
+ Hoặc có thể tập trung tối ưu chiến lược cho khung thời gian lớn hơn như **M15** hay **H1**, và giảm được **Max Drawdown** xuống thấp nữa.
+ Có thể tìm hiểu thêm về những logic để set **TP/SL** và tỉ lệ R:R phù hợp để tối ưu được lợi nhuận.
+ Thêm các điều kiện để bot không bị quá **overtrade** ở các khung nhỏ hơn 
+ Nếu có đủ thời gian có thể tìm hiểu thêm về các mô hình **AI/ML** để giúp cải thiện hiệu suất lên cao nếu có một chiến lược hoàn chỉnh cần thay đổi tham số nhiều.
+ Chỉnh sửa lại việc đóng lệnh khi hết khung h hành chính, tránh việc bot giữ lệnh qua các ngày khác.
