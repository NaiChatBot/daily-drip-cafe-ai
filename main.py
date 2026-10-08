from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import joblib

app = FastAPI(
    title="Daily Drip Cafe AI API",
    version="0.1.0"
)

BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "daily_drip_sales_model.pkl")

class WeatherInput(BaseModel):
    rainfall_mm: float = Field(default=20.0, example=20.0)
    temperature_c: float = Field(default=32.0, example=32.0)
    is_weekend: int = Field(default=1, example=1)
    is_holiday: int = Field(default=0, example=0)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Drip Cafe - AI Forecasting & Inventory Analytics</title>
        <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Kanit', sans-serif; }
            body { background: #f4efe9; color: #3e2723; padding: 25px 15px; }
            .dashboard-container { max-width: 1150px; margin: 0 auto; }
            
            /* Top Header */
            .header-card { background: #4e342e; color: white; padding: 22px 28px; border-radius: 18px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
            .header-card h1 { font-size: 1.7rem; font-weight: 600; display: flex; align-items: center; gap: 12px; }
            .header-card p { font-size: 0.9rem; opacity: 0.85; margin-top: 4px; }
            .badge { background: #2e7d32; color: #fff; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; display: flex; align-items: center; gap: 8px; }

            /* Grid Layout */
            .layout-grid { display: grid; grid-template-columns: 340px 1fr; gap: 20px; }
            
            /* Form Panel */
            .panel-card { background: white; padding: 22px; border-radius: 18px; border: 1px solid #d7ccc8; box-shadow: 0 3px 12px rgba(0,0,0,0.03); }
            .panel-card h3 { font-size: 1.1rem; color: #4e342e; margin-bottom: 15px; border-bottom: 2px solid #efebe9; padding-bottom: 8px; }
            .input-group { margin-bottom: 12px; }
            .input-group label { display: block; font-size: 0.85rem; color: #5d4037; font-weight: 500; margin-bottom: 5px; }
            .input-group input, .input-group select { width: 100%; padding: 10px 12px; border: 1.5px solid #d7ccc8; border-radius: 10px; font-size: 0.95rem; outline: none; background: #faf8f5; }
            .input-group input:focus, .input-group select:focus { border-color: #8d6e63; background: #fff; }
            button { width: 100%; padding: 13px; background: #6d4c41; color: white; border: none; border-radius: 10px; font-size: 1.05rem; font-weight: 500; cursor: pointer; margin-top: 10px; transition: 0.2s; box-shadow: 0 4px 10px rgba(109,76,65,0.2); }
            button:hover { background: #3e2723; }

            /* Ingredient Cards (5 Items) */
            .kpi-title { font-size: 1rem; color: #4e342e; font-weight: 600; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
            .ingredients-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 20px; }
            .ing-card { background: white; padding: 14px 10px; border-radius: 14px; text-align: center; border: 1px solid #d7ccc8; border-top: 4px solid #6d4c41; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
            .ing-card i { font-size: 1.3rem; color: #6d4c41; margin-bottom: 6px; }
            .ing-card h5 { font-size: 0.75rem; color: #795548; font-weight: 500; }
            .ing-card .val { font-size: 1.25rem; font-weight: 600; color: #3e2723; margin-top: 4px; }

            /* Chart Area */
            .chart-card { background: white; padding: 20px; border-radius: 18px; border: 1px solid #d7ccc8; box-shadow: 0 3px 12px rgba(0,0,0,0.03); margin-bottom: 20px; }
            .chart-card h3 { font-size: 1rem; color: #4e342e; margin-bottom: 4px; }
            .chart-card p { font-size: 0.8rem; color: #8d6e63; margin-bottom: 15px; }

            .footer-text { text-align: center; margin-top: 25px; font-size: 0.85rem; color: #8d6e63; }
            .footer-text a { color: #6d4c41; font-weight: 600; text-decoration: none; }

            @media (max-width: 900px) { .layout-grid { grid-template-columns: 1fr; } }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <div class="header-card">
                <div>
                    <h1><i class="fa-solid fa-mug-hot"></i> Daily Drip Cafe</h1>
                    <p>ระบบ AI พยากรณ์ยอดขายและคำนวณวัตถุดิบสดล่วงหน้า (Predictive Inventory)</p>
                </div>
                <div class="badge">
                    <i class="fa-solid fa-circle-check"></i> Render Cloud Live
                </div>
            </div>

            <div class="layout-grid">
                <!-- Left Input Panel -->
                <div class="panel-card">
                    <h3><i class="fa-solid fa-sliders"></i> ปัจจัยพยากรณ์ประจำวัน</h3>
                    <div class="input-group">
                        <label><i class="fa-solid fa-cloud-rain"></i> ปริมาณฝนตก (mm):</label>
                        <input type="number" id="rainfall" value="20.0" step="0.5">
                    </div>
                    <div class="input-group">
                        <label><i class="fa-solid fa-temperature-high"></i> อุณหภูมิเฉลี่ย (°C):</label>
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
                            <option value="0">ไม่ใช่วันหยุด</option>
                            <option value="1">วันหยุดนักขัตฤกษ์</option>
                        </select>
                    </div>
                    <button onclick="calculateAI()"><i class="fa-solid fa-wand-magic-sparkles"></i> ประมวลผลด้วย AI</button>
                </div>

                <!-- Right Analytics & Results -->
                <div>
                    <div class="kpi-title"><i class="fa-solid fa-boxes-packing"></i> สรุปวัตถุดิบและแก้วที่ต้องสั่งซื้อประจำวัน</div>
                    <div class="ingredients-grid">
                        <div class="ing-card">
                            <i class="fa-solid fa-motorcycle"></i>
                            <h5>ยอด Delivery</h5>
                            <div class="val" id="res-cups">85 แก้ว</div>
                        </div>
                        <div class="ing-card">
                            <i class="fa-solid fa-seedling"></i>
                            <h5>เมล็ดกาแฟ</h5>
                            <div class="val" id="res-coffee">1.5 กก.</div>
                        </div>
                        <div class="ing-card">
                            <i class="fa-solid fa-bottle-droplet"></i>
                            <h5>นมสดสด</h5>
                            <div class="val" id="res-milk">12.8 ลิตร</div>
                        </div>
                        <div class="ing-card">
                            <i class="fa-solid fa-bread-slice"></i>
                            <h5>เบเกอรี่อบสด</h5>
                            <div class="val" id="res-bakery">18 ชิ้น</div>
                        </div>
                        <div class="ing-card">
                            <i class="fa-solid fa-box"></i>
                            <h5>แก้ว Delivery</h5>
                            <div class="val" id="res-box">85 ชุด</div>
                        </div>
                    </div>

                    <!-- Chart section -->
                    <div class="chart-card">
                        <h3><i class="fa-solid fa-chart-line"></i> แนวโน้มพยากรณ์ยอดขายและวัตถุดิบล่วงหน้า 30 วัน</h3>
                        <p>วิเคราะห์เปรียบเทียบระหว่างยอดขายคาดการณ์ (แก้ว) และอัตราการใช้นมสด (ลิตร)</p>
                        <canvas id="analyticsChart" height="110"></canvas>
                    </div>
                </div>
            </div>

            <div class="footer-text">
                Daily Drip Cafe AI System | <a href="/docs" target="_blank">เปิดหน้า Interactive Swagger UI API</a>
            </div>
        </div>

        <script>
            let myChart;

            function initChart() {
                const labels = Array.from({length: 30}, (_, i) => {
                    let d = new Date();
                    d.setDate(d.getDate() - (29 - i));
                    return `${d.getDate()}/${d.getMonth()+1}`;
                });

                const salesData = [38, 40, 42, 45, 68, 78, 85, 42, 40, 39, 44, 72, 84, 88, 46, 41, 40, 45, 70, 82, 85, 48, 42, 40, 44, 66, 78, 85, 50, 85];
                const milkData = salesData.map(v => (v * 0.15).toFixed(1));

                const ctx = document.getElementById('analyticsChart').getContext('2d');
                myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'ยอดขายคาดการณ์ (แก้ว)',
                                data: salesData,
                                borderColor: '#6d4c41',
                                backgroundColor: 'rgba(109, 76, 65, 0.1)',
                                fill: true,
                                tension: 0.3
                            },
                            {
                                label: 'นมสดที่ต้องใช้ (ลิตร)',
                                data: milkData,
                                borderColor: '#d84315',
                                borderDash: [5, 5],
                                fill: false,
                                tension: 0.3
                            }
                        ]
                    },
                    options: { responsive: true, plugins: { legend: { position: 'top' } } }
                });
            }

            function calculateAI() {
                const rainfall = parseFloat(document.getElementById('rainfall').value);
                const temp = parseFloat(document.getElementById('temp').value);
                const isWeekend = parseInt(document.getElementById('weekend').value);
                const isHoliday = parseInt(document.getElementById('holiday').value);

                fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        rainfall_mm: rainfall,
                        temperature_c: temp,
                        is_weekend: isWeekend,
                        is_holiday: isHoliday
                    })
                })
                .then(res => res.json())
                .then(data => {
                    const cups = data.predicted_delivery_cups;
                    const milk = data.suggested_milk_liters;
                    const coffee = data.suggested_coffee_kg;
                    const bakery = data.suggested_bakery_pieces;
                    const containers = data.suggested_delivery_cups;

                    document.getElementById('res-cups').innerText = cups + ' แก้ว';
                    document.getElementById('res-milk').innerText = milk + ' ลิตร';
                    document.getElementById('res-coffee').innerText = coffee + ' กก.';
                    document.getElementById('res-bakery').innerText = bakery + ' ชิ้น';
                    document.getElementById('res-box').innerText = containers + ' ชุด';

                    // Update last data point on Chart
                    myChart.data.datasets[0].data[29] = cups;
                    myChart.data.datasets[1].data[29] = milk;
                    myChart.update();
                });
            }

            window.onload = initChart;
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/predict", summary="Predict Delivery Supplies")
def predict_supplies(data: WeatherInput):
    features = [[
        data.rainfall_mm,
        data.temperature_c,
        data.is_weekend,
        data.is_holiday
    ]]

    predicted_cups = float(model.predict(features)[0])
    predicted_cups_rounded = round(predicted_cups)

    # สูตรคำนวณวัตถุดิบกาแฟ Specialty 5 รายการ
    suggested_milk = round(predicted_cups_rounded * 0.15, 1)      # นมสด ~150ml / แก้ว
    suggested_coffee = round(predicted_cups_rounded * 0.018, 1)    # เมล็ดกาแฟ ~18g / แก้ว
    
    # ถ้าฝนตกหนัก เบเกอรี่หน้าร้านจะขายได้น้อยลง (ลดความเสี่ยง Food Waste)
    if data.rainfall_mm > 15.0:
        suggested_bakery = max(10, round(predicted_cups_rounded * 0.2)) 
    else:
        suggested_bakery = round(predicted_cups_rounded * 0.4)

    suggested_containers = predicted_cups_rounded

    return {
        "predicted_delivery_cups": predicted_cups_rounded,
        "suggested_milk_liters": suggested_milk,
        "suggested_coffee_kg": suggested_coffee,
        "suggested_bakery_pieces": suggested_bakery,
        "suggested_delivery_cups": suggested_containers,
        "status": "success",
        "message": "คำนวณพยากรณ์วัตถุดิบเรียบร้อยแล้ว"
    }