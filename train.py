import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. อ่านข้อมูลประวัติยอดขาย 30 วัน
df = pd.read_excel('Daily_Drip_Cafe_Historical_Data_30_Days.xlsx', sheet_name='Daily_History')

# 2. แปลงข้อมูลวันหยุดและเสาร์-อาทิตย์เป็นตัวเลข (1 = ใช่, 0 = ไม่ใช่)
df['Weekend_Num'] = df['Weekend'].apply(lambda x: 1 if x == 'ใช่' else 0)
df['Holiday_Num'] = df['Holiday'].apply(lambda x: 1 if x == 'ใช่' else 0)

# 3. กำหนดตัวแปรต้น (Features) และตัวแปรเป้าหมาย (Target: ยอดขาย Delivery)
X = df[['Rainfall_mm', 'Temperature_C', 'Weekend_Num', 'Holiday_Num']]
y = df['Delivery_Cups']

# 4. สร้างและเทรนโมเดล Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. บันทึกโมเดลที่เทรนเสร็จแล้วไว้ใช้งาน
joblib.dump(model, 'daily_drip_sales_model.pkl')
print("✅ เทรนโมเดลเรียบร้อย! ได้ไฟล์ 'daily_drip_sales_model.pkl' สำหรับไปใช้งานต่อ")