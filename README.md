# QKD Key Rate Dashboard (BB84 vs Six-state)

這個專案是一個 Streamlit 互動式介面，用來視覺化量子金鑰分配 (QKD) 中：
- Shor-Preskill 邊界 (對應 BB84 / 各向異性通道)
- 六態協定邊界 (對應各向同性通道)

使用者可以透過 QBER 滑桿即時觀察兩種模型的安全金鑰率變化，並比較兩者在臨界錯誤率附近的差異。

## 功能

- 即時調整量子位元錯誤率 (QBER)
- 顯示兩條金鑰率曲線
- 顯示目前 QBER 對應的兩個速率值
- 顯示臨界線：
  - Shor-Preskill 約 11.0%
  - Six-state 約 12.6%
- 補充說明為何六態協定可容忍較高錯誤率

## 理論模型

二元熵函數：

h(x) = -x log2(x) - (1 - x) log2(1 - x)

1) 各向異性通道 (Shor-Preskill 邊界)

R_ani(e) = max(1 - 2h(e), 0)

2) 各向同性通道 (Six-state 對應)

令 e_adj = 1.5e，則

R_iso(e) = max(1 - h(e_adj) - e_adj log2(3), 0)

## 專案結構

- app.py: Streamlit 主程式
- requirements.txt: 部署與執行所需 Python 套件

## 本機執行

1. 安裝依賴

pip install -r requirements.txt

2. 啟動應用

streamlit run app.py

## 部署到 Streamlit Cloud

1. 將專案推送到 GitHub
2. 在 Streamlit Cloud 建立新 App，指向此 repository
3. Main file path 設為 app.py
4. 確認 repository 根目錄有 requirements.txt

若看到 ModuleNotFoundError (例如 plotly)，通常是依賴未安裝；重新部署並確保 requirements.txt 存在即可。

## 授權

可依課程或研究需求自行修改使用。
