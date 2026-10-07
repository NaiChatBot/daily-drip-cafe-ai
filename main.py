from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Daily Drip Cafe AI API")

# โหลดโมเดลที่เทรนไว้จากขั้นตอนที่ 1
model = joblib.load('daily_drip_sales_model.pkl')

# กำหนดโครงสร้างข้อมูลอินพุตที่รับเข้ามาจากภายนอก
class WeatherInput(BaseModel):
    rainfall_mm: float      # ปริมาณฝน (มม.)
    temperature_c: float    # อุณหภูมิ (°C)
    is_weekend: int         # 1 = วันเสาร์-อาทิตย์, 0 = วันธรรมดา
    is_holiday: int         # 1 = วันหยุดนักขัตฤกษ์, 0 = ไม่ใช่

@app.get("/")
def home():
    return {"message": "Daily Drip Cafe AI API พร้อมทำงานแล้ว!"}

@app.post("/predict")
def predict_delivery_supplies(data: WeatherInput):
    # นำข้อมูลอินพุตมาจัดลง DataFrame ให้ตรงกับที่ AI เคยเรียนรู้
    input_df = pd.DataFrame([{
        'Rainfall_mm': data.rainfall_mm,
        'Temperature_C': data.temperature_c,
        'Weekend_Num': data.is_weekend,
        'Holiday_Num': data.is_holiday
    }])
    
    # AI พยากรณ์จำนวนแก้ว Delivery
    predicted_delivery = int(model.predict(input_df)[0])
    
    # คำนวณวัตถุดิบและบรรจุภัณฑ์ที่ต้องสั่งตุนตามสูตร
    suggested_milk_l = round(predicted_delivery * 0.12, 1)  # นมสดเฉลี่ย 120ml/แก้ว
    suggested_cups = predicted_delivery                    # จำนวนแก้ว Delivery
    
    return {
        "predicted_delivery_cups": predicted_delivery,
        "suggested_milk_liters": suggested_milk_l,
        "suggested_delivery_cups": suggested_cups,
        "status": "Success"
    }