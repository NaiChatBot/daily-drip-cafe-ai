from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

# 1. กำหนดรายละเอียดหน้าเว็บ Swagger UI เป็นภาษาไทย
app = FastAPI(
    title="☕ Daily Drip Cafe - AI Forecasting API",
    description="""
    ### ระบบพยากรณ์ยอดขายและบริหารจัดการวัตถุดิบอัตโนมัติด้วย Machine Learning 🚀
    
    **วัตถุประสงค์:** วิเคราะห์แพทเทิร์นสภาพอากาศ (ปริมาณฝน/อุณหภูมิ/วันหยุด) เพื่อคำนวณยอดขาย Delivery คาดการณ์ 
    และแนะนำจำนวนสั่งซื้อวัตถุดิบสด (นมสด, แก้ว/ฝาบรรจุภัณฑ์) ล่วงหน้า เพื่อลดปัญหา Food Waste และสินค้าขาดสต็อก
    
    ---
    💡 **วิธีทดลองใช้งานสำหรับอาจารย์:**
    1. คลิกที่แถบสีเขียว **`POST /predict`** ด้านล่าง
    2. กดปุ่ม **Try it out** มุมขวาบน
    3. กดปุ่ม **Execute** สีน้ำเงินเพื่อดูผลลัพธ์พยากรณ์ทันที!
    """,
    version="1.0.0"
)

# โหลดโมเดล
BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "daily_drip_sales_model.pkl")

# 2. กำหนดโครงสร้างข้อมูลพร้อมคำอธิบายภาษาไทยและค่าตัวอย่าง
class WeatherInput(BaseModel):
    rainfall_mm: float = Field(
        default=20.0, 
        description="ปริมาณฝนตก (มิลลิเมตร) เช่น 0.0 (ไม่มีฝน) หรือ 25.0 (ฝนตกหนัก)",
        example=20.0
    )
    temperature_c: float = Field(
        default=32.0, 
        description="อุณหภูมิเฉลี่ยประจำวัน (°C) เช่น 32.0",
        example=32.0
    )
    is_weekend: int = Field(
        default=1, 
        description="เป็นวันเสาร์-อาทิตย์หรือไม่ (1 = ใช่, 0 = ไม่ใช่)",
        example=1
    )
    is_holiday: int = Field(
        default=0, 
        description="เป็นวันหยุดนักขัตฤกษ์หรือไม่ (1 = ใช่, 0 = ไม่ใช่)",
        example=0
    )

@app.get("/", summary="ตรวจสอบสถานะเซิร์ฟเวอร์ (Health Check)")
def serve_index():
    return {
        "status": "online",
        "system": "Daily Drip Cafe AI Engine",
        "message": "ระบบ AI พร้อมใช้งาน กรุณาเข้าใช้งานที่ /docs"
    }

@app.post(
    "/predict", 
    summary="☕ พยากรณ์ยอดขายและวัตถุดิบประจำวัน (Predict Sales & Ingredients)",
    description="ยิงข้อมูลสภาพอากาศเข้าโมเดลเพื่อคำนวณยอดขายแก้วคาดการณ์ ปริมาณนมสด (ลิตร) และบรรจุภัณฑ์ที่ต้องเตรียม"
)
def predict_supplies(data: WeatherInput):
    # รวม Feature Vector
    features = [[
        data.rainfall_mm,
        data.temperature_c,
        data.is_weekend,
        data.is_holiday
    ]]

    # ทำนายยอดขายด้วย RandomForest Model
    predicted_cups = float(model.predict(features)[0])
    predicted_cups_rounded = round(predicted_cups)

    # คำนวณสูตรวัตถุดิบ (ตัวอย่าง: กาแฟนม 1 แก้วใช้นมสด ~0.15 ลิตร)
    suggested_milk = round(predicted_cups_rounded * 0.15, 1)
    suggested_containers = predicted_cups_rounded

    return {
        "predicted_delivery_cups": predicted_cups_rounded,
        "suggested_milk_liters": suggested_milk,
        "suggested_delivery_cups": suggested_containers,
        "status": "success",
        "message": "คำนวณพยากรณ์ยอดขายและคำแนะนำสั่งวัตถุดิบเรียบร้อยแล้ว"
    }