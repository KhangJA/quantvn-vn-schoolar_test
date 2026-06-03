import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
from quantvn.vn.data.utils import client
from quantvn.vn.data import get_derivatives_hist
from quantvn.vn.metrics import Backtest_Derivates
from quantvn.vn.metrics import Metrics

# Lấy API_KEY từ file .env
load_dotenv()
client(apikey=os.getenv("API_KEY"))

def gen_position(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # ==========================================
    # LOGIC/XỬ LÝ
    # ==========================================
    
    # MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss.replace(0, np.nan)
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(50)

    # Stochastic
    low_14 = df['Low'].rolling(window=14).min()
    high_14 = df['High'].rolling(window=14).max()
    denom = high_14 - low_14
    df['Stoch_K'] = np.where(denom == 0, 50, 100 * ((df['Close'] - low_14) / denom))
    df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean() # Đường Smoothed nhằm lm giảm nhiễu.
    
    # ROC
    df['ROC'] = df['Close'].pct_change(periods=10) * 100

    # ==========================================
    # HỆ THỐNG TÍNH ĐIỂM XÁC NHẬN SIGNAL VÀO LỆNH
    # ==========================================
  
    df['Bull_Score'] = 0
    df['Bear_Score'] = 0

    # Logic Long cộng điểm cho từng chỉ báo
    df.loc[df['MACD'] > df['MACD_Signal'], 'Bull_Score'] += 1
    df.loc[df['RSI'] > 50, 'Bull_Score'] += 1
    df.loc[df['Stoch_D'] > 50, 'Bull_Score'] += 1  # Dùng %D thay vì %K
    df.loc[df['ROC'] > 0.05, 'Bull_Score'] += 1

    # Logic Short cộng điểm cho từng chỉ báo
    df.loc[df['MACD'] < df['MACD_Signal'], 'Bear_Score'] += 1
    df.loc[df['RSI'] < 50, 'Bear_Score'] += 1
    df.loc[df['Stoch_D'] < 50, 'Bear_Score'] += 1
    df.loc[df['ROC'] < -0.05, 'Bear_Score'] += 1

    # ==========================================
    # TẠO SIGNAL KHI CÓ ÍT NHẤT 3/4 CHỈ BÁO XÁC NHẬN
    # ==========================================
    df['position'] = 0
    df.loc[df['Bull_Score'] >= 3, 'position'] = 1  # Long
    df.loc[df['Bear_Score'] >= 3, 'position'] = -1 # Short
    
    # Dịch signal 1 nến để làm chậm signal vào cây nến tiếp theo (Chỉ vào signal theo data quá khứ).
    # nếu ko thì vào lệnh ngay khi ra xuất hiện có khả năng nến chưa đóng nhảy vào tín hiệu chưa đúng
    df['position'] = df['position'].shift(1).fillna(0)

    return df

df = get_derivatives_hist("VN30F1M", "15m")
df_pos = gen_position(df) # Sử dụng chiến lược

backtest = Backtest_Derivates(df_pos, pnl_type="after_fees")
metrics = Metrics(backtest)

# Các chỉ số hiệu suất
print(f"Sharpe Ratio: {metrics.sharpe():.3f}")
print(f"Sortino Ratio: {metrics.sortino():.3f}")
print(f"Calmar Ratio: {metrics.calmar():.3f}")
print(f"Max Drawdown: {metrics.max_drawdown()*100:.2f}%")
print(f"Win Rate: {metrics.win_rate()*100:.2f}%")
print(f"Profit Factor: {metrics.profit_factor():.3f}")
print(f"Average Win: {metrics.avg_win():,.0f} VND")
print(f"Average Loss: {metrics.avg_loss():,.0f} VND")
print(f"Risk of Ruin: {metrics.risk_of_ruin():.4f}")

# Value at Risk (95% confidence)
var_95 = metrics.value_at_risk(confidence_level=0.95)
print(f"VaR (95%): {var_95:,.0f} VND")