from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import joblib

# 1. ปรับแต่ง Swagger UI Description เป็น HTML สะอาดๆ
app = FastAPI(
    title="☕ Daily Drip Cafe - AI Forecasting API",
    description="""
    <b style="color: #6b4e3d; font-size: 16px;">ระบบพยากรณ์ยอดขายและบริหารจัดการวัตถุดิบอัตโนมัติด้วย Machine Learning 🚀</b><br><br>
    <b>วัตถุประสงค์:</b> วิเคราะห์แพทเทิร์นสภาพอากาศ (ปริมาณฝน/อุณหภูมิ/วันหยุด) เพื่อคำนวณยอดขาย Delivery คาดการณ์ 
    และแนะนำจำนวนสั่งซื้อวัตถุดิบสด (นมสด, แก้ว/ฝาบรรจุภัณฑ์) ล่วงหน้า เพื่อลดปัญหา Food Waste และสินค้าขาดสต็อก<br><br>
    💡 <b>วิธีทดลองใช้งานสำหรับอาจารย์:</b><br>
    1. คลิกที่แถบสีเขียว <code>POST /predict</code> ด้านล่าง<br>
    2. กดปุ่ม <b>Try it out</b> มุมขวาบน<br>
    3. กดปุ่ม <b>Execute</b> สีน้ำเงินเพื่อดูผลลัพธ์พยากรณ์ทันที!
    """,
    version="1.0.0"
)

# โหลดโมเดล
BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "daily_drip_sales_model.pkl")

class WeatherInput(BaseModel):
    rainfall_mm: float = Field(
        default=20.0, 
        description="ปริมาณฝนตก (มิลลิเมตร)",
        example=20.0
    )
    temperature_c: float = Field(
        default=32.0, 
        description="อุณหภูมิเฉลี่ยประจำวัน (°C)",
        example=32.0
    )
    is_weekend: int = Field(
        default=1, 
        description="วันเสาร์-อาทิตย์หรือไม่ (1 = ใช่, 0 = ไม่ใช่)",
        example=1
    )
    is_holiday: int = Field(
        default=0, 
        description="วันหยุดนักขัตฤกษ์หรือไม่ (1 = ใช่, 0 = ไม่ใช่)",
        example=0
    )

# 2. หน้าหลัก (Homepage) เป็น Dashboard ภาษาไทย ธีมร้านกาแฟ สวยระดับพรีเมียม
@app.get("/", response_class=HTMLResponse, summary="หน้าเว็บ UI Dashboard สำหรับใช้งาน")
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Drip Cafe - AI Forecasting System</title>
        <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Kanit', sans-serif; }
            body { background: #f4efe9; color: #3e2723; min-height: 100vh; padding: 20px; display: flex; justify-content: center; align-items: center; }
            .container { background: #ffffff; border-radius: 20px; padding: 30px; width: 100%; max-width: 600px; box-shadow: 0 10px 30px rgba(62, 39, 35, 0.1); border: 1px solid #d7ccc8; }
            .header { text-align: center; margin-bottom: 25px; }
            .header i { font-size: 3rem; color: #6d4c41; margin-bottom: 10px; }
            .header h1 { font-size: 1.8rem; color: #4e342e; font-weight: 600; }
            .header p { font-size: 0.95rem; color: #8d6e63; }
            .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
            .input-group { display: flex; flex-direction: column; }
            .input-group label { font-size: 0.9rem; margin-bottom: 5px; color: #5d4037; font-weight: 500; }
            .input-group input, .input-group select { padding: 12px; border: 1.5px solid #d7ccc8; border-radius: 10px; font-size: 1rem; outline: none; background: #faf8f5; }
            .input-group input:focus, .input-group select:focus { border-color: #8d6e63; background: #fff; }
            button { width: 100%; padding: 14px; background: #6d4c41; color: white; border: none; border-radius: 10px; font-size: 1.1rem; font-weight: 500; cursor: pointer; transition: 0.3s; box-shadow: 0 4px 12px rgba(109, 76, 65, 0.2); }
            button:hover { background: #4e342e; }
            .results { margin-top: 25px; display: none; grid-template-columns: 1fr 1fr 1fr; gap: 10px; animation: fadeIn 0.4s ease-in-out; }
            .card { background: #efebe9; padding: 15px 10px; border-radius: 12px; text-align: center; border: 1px solid #d7ccc8; }
            .card i { font-size: 1.5rem; color: #6d4c41; margin-bottom: 5px; }
            .card h4 { font-size: 0.8rem; color: #795548; font-weight: 500; }
            .card .num { font-size: 1.4rem; font-weight: 600; color: #3e2723; margin-top: 5px; }
            .footer-link { text-align: center; margin-top: 20px; font-size: 0.85rem; }
            .footer-link a { color: #8d6e63; text-decoration: none; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <i class="fa-solid fa-mug-hot"></i>
                <h1>Daily Drip Cafe</h1>
                <p>ระบบ AI พยากรณ์ยอดขาย & แนะนำการสั่งวัตถุดิบ</p>
            </div>

            <div class="form-grid">
                <div class="input-group">
                    <label><i class="fa-solid fa-cloud-rain"></i> ปริมาณฝน (mm):</label>
                    <input type="number" id="rainfall" value="20.0" step="0.5">
                </div>
                <div class="input-group">
                    <label><i class="fa-solid fa-temperature-high"></i> อุณหภูมิ (°C):</label>
                    <input type="number" id="temp" value="32.0" step="0.5">
                </div>
                <div class="input-group">
                    <label><i class="fa-solid fa-calendar-day"></i> ประเภทวัน:</label>
                    <select id="weekend">
                        <option value="1">วันเสาร์ - อาทิตย์</option>
                        <option value="0">วันธรรมดา (จันทร์-ศุกร์)</option>
                    </select>
                </div>
                <div class="input-group">
                    <label><i class="fa-solid fa-star"></i> วันหยุดนักขัตฤกษ์:</label>
                    <select id="holiday">
                        <option value="0">ไม่ใช่ผันหยุด</option>
                        <option value="1">วันหยุดนักขัตฤกษ์</option>
                    </select>
                </div>
            </div>

            <button onclick="predictSales()"><i class="fa-solid fa-wand-magic-sparkles"></i> พยากรณ์ยอดขายและวัตถุดิบ</button>

            <div id="results" class="results">
                <div class="card">
                    <i class="fa-solid fa-motorcycle"></i>
                    <h4>ยอดขาย Delivery</h4>
                    <div id="cups" class="num">0 แก้ว</div>
                </div>
                <div class="card">
                    <i class="fa-solid fa-bottle-droplet"></i>
                    <h4>นมสดที่ต้องสั่ง</h4>
                    <div id="milk" class="num">0 ลิตร</div>
                </div>
                <div class="card">
                    <i class="fa-solid fa-box"></i>
                    <h4>แก้วบรรจุภัณฑ์</h4>
                    <div id="containers" class="num">0 ชุด</div>
                </div>
            </div>

            <div class="footer-link">
                <a href="/docs" target="_blank"><i class="fa-solid fa-code"></i> เข้าสู่หน้า Interactive API (Swagger UI)</a>
            </div>
        </div>

        <script>
            function predictSales() {
                const payload = {
                    rainfall_mm: parseFloat(document.getElementById('rainfall').value),
                    temperature_c: parseFloat(document.getElementById('temp').value),
                    is_weekend: parseInt(document.getElementById('weekend').value),
                    is_holiday: parseInt(document.getElementById('holiday').value)
                };

                fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById('cups').innerText = data.predicted_delivery_cups + ' แก้ว';
                    document.getElementById('milk').innerText = data.suggested_milk_liters + ' ลิตร';
                    document.getElementById('containers').innerText = data.suggested_delivery_cups + ' ชุด';
                    document.getElementById('results').style.display = 'grid';
                })
                .catch(err => alert('เกิดข้อผิดพลาดในการคำนวณ'));
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post(
    "/predict", 
    summary="☕ พยากรณ์ยอดขายและวัตถุดิบประจำวัน (Predict Sales & Ingredients)",
    description="ยิงข้อมูลสภาพอากาศเข้าโมเดลเพื่อคำนวณยอดขายแก้วคาดการณ์ ปริมาณนมสด (ลิตร) และบรรจุภัณฑ์ที่ต้องเตรียม"
)
def predict_supplies(data: WeatherInput):
    features = [[
        data.rainfall_mm,
        data.temperature_c,
        data.is_weekend,
        data.is_holiday
    ]]

    predicted_cups = float(model.predict(features)[0])
    predicted_cups_rounded = round(predicted_cups)

    suggested_milk = round(predicted_cups_rounded * 0.15, 1)
    suggested_containers = predicted_cups_rounded

    return {
        "predicted_delivery_cups": predicted_cups_rounded,
        "suggested_milk_liters": suggested_milk,
        "suggested_delivery_cups": suggested_containers,
        "status": "success",
        "message": "คำนวณพยากรณ์ยอดขายและคำแนะนำสั่งวัตถุดิบเรียบร้อยแล้ว"
    }