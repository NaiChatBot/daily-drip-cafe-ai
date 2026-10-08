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
        <title>Daily Drip Cafe - Executive Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Kanit', sans-serif; }
            body { background: #f4efe9; color: #3e2723; padding: 20px; }
            .dashboard-container { max-width: 1100px; margin: 0 auto; }
            
            /* Header Bar */
            .top-bar { background: #4e342e; color: white; padding: 20px 25px; border-radius: 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            .top-bar .title h1 { font-size: 1.6rem; font-weight: 600; display: flex; align-items: center; gap: 10px; }
            .top-bar .title p { font-size: 0.85rem; opacity: 0.8; margin-top: 3px; }
            .status-badge { background: #2e7d32; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; display: flex; align-items: center; gap: 6px; }

            /* KPI Summary Cards */
            .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 20px; }
            .kpi-card { background: white; padding: 18px; border-radius: 14px; border: 1px solid #d7ccc8; box-shadow: 0 2px 8px rgba(0,0,0,0.03); border-left: 5px solid #6d4c41; }
            .kpi-card .label { font-size: 0.85rem; color: #795548; font-weight: 500; display: flex; justify-content: space-between; }
            .kpi-card .val { font-size: 1.8rem; font-weight: 600; color: #3e2723; margin-top: 8px; }
            .kpi-card .sub { font-size: 0.75rem; color: #8d6e63; margin-top: 4px; }

            /* Main Layout Grid */
            .main-grid { display: grid; grid-template-columns: 320px 1fr; gap: 20px; }
            
            /* Control Panel */
            .panel { background: white; padding: 22px; border-radius: 16px; border: 1px solid #d7ccc8; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
            .panel h3 { font-size: 1.1rem; color: #4e342e; margin-bottom: 15px; border-bottom: 2px solid #efebe9; padding-bottom: 8px; }
            .input-group { margin-bottom: 12px; }
            .input-group label { display: block; font-size: 0.85rem; color: #5d4037; font-weight: 500; margin-bottom: 5px; }
            .input-group input, .input-group select { width: 100%; padding: 10px; border: 1.5px solid #d7ccc8; border-radius: 8px; font-size: 0.95rem; outline: none; background: #faf8f5; }
            button { width: 100%; padding: 12px; background: #6d4c41; color: white; border: none; border-radius: 10px; font-size: 1rem; font-weight: 500; cursor: pointer; margin-top: 10px; transition: 0.2s; }
            button:hover { background: #3e2723; }

            /* Charts Area */
            .chart-card { background: white; padding: 20px; border-radius: 16px; border: 1px solid #d7ccc8; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
            .chart-card h3 { font-size: 1rem; color: #4e342e; margin-bottom: 5px; }
            .chart-card p { font-size: 0.8rem; color: #8d6e63; margin-bottom: 15px; }
            
            .footer-link { text-align: center; margin-top: 25px; font-size: 0.85rem; color: #8d6e63; }
            .footer-link a { color: #6d4c41; font-weight: 600; text-decoration: none; }

            @media (max-width: 850px) {
                .main-grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <!-- Top Bar -->
            <div class="top-bar">
                <div class="title">
                    <h1><i class="fa-solid fa-mug-hot"></i> Daily Drip Cafe</h1>
                    <p>ระบบวิเคราะห์และพยากรณ์การดำเนินงาน เพื่อช่วยวางแผนสต็อกล่วงหน้า</p>
                </div>
                <div class="status-badge">
                    <i class="fa-solid fa-circle-check"></i> เชื่อมต่อ AI Engine สำเร็จ
                </div>
            </div>

            <!-- KPI Summary Cards -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="label">พยากรณ์ Delivery <i class="fa-solid fa-motorcycle"></i></div>
                    <div class="val" id="kpi-cups">85 แก้ว</div>
                    <div class="sub">คำนวณจากปัจจัยสภาพอากาศ</div>
                </div>
                <div class="kpi-card">
                    <div class="label">นมสดที่แนะนำสั่ง <i class="fa-solid fa-bottle-droplet"></i></div>
                    <div class="val" id="kpi-milk">12.8 ลิตร</div>
                    <div class="sub">อัตราส่วน 0.15 ลิตร/แก้ว</div>
                </div>
                <div class="kpi-card">
                    <div class="label">แก้วบรรจุภัณฑ์ <i class="fa-solid fa-box"></i></div>
                    <div class="val" id="kpi-box">85 ชุด</div>
                    <div class="sub">เตรียมแก้ว + ฝา Delivery</div>
                </div>
                <div class="kpi-card">
                    <div class="label">ประเมินภาระงาน <i class="fa-solid fa-chart-line"></i></div>
                    <div class="val" id="kpi-workload" style="color:#d84315;">สูง (Peak)</div>
                    <div class="sub">แนะนำเพิ่มบาริสต้าช่วงเช้า</div>
                </div>
            </div>

            <!-- Main Layout Grid -->
            <div class="main-grid">
                <!-- Control Panel -->
                <div class="panel">
                    <h3><i class="fa-solid fa-sliders"></i> จำลองสภาพอากาศ</h3>
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
                            <option value="0">ไม่ใช่วันหยุด</option>
                            <option value="1">วันหยุดนักขัตฤกษ์</option>
                        </select>
                    </div>
                    <button onclick="updatePrediction()"><i class="fa-solid fa-wand-magic-sparkles"></i> อัปเดตการพยากรณ์</button>
                </div>

                <!-- Charts Section -->
                <div>
                    <div class="chart-card">
                        <h3>แนวโน้มยอดขาย Delivery คาดการณ์ (30 วัน)</h3>
                        <p>แสดงพฤติกรรมยอดขายตามการสลับวันหยุดและแนวโน้มสภาพอากาศ</p>
                        <canvas id="trendChart" height="130"></canvas>
                    </div>

                    <div class="chart-card">
                        <h3>การเปรียบเทียบภาระงานและวัตถุดิบที่ต้องใช้</h3>
                        <p>ใช้เพื่อดูช่วงสัปดาห์ที่ควรเตรียมปริมาณนมสดสต็อกเป็นพิเศษ</p>
                        <canvas id="barChart" height="110"></canvas>
                    </div>
                </div>
            </div>

            <div class="footer-link">
                Daily Drip Cafe AI Inventory System | <a href="/docs" target="_blank">เปิดหน้า Interactive API (Swagger UI)</a>
            </div>
        </div>

        <script>
            let trendChart, barChart;

            // สร้าง กราฟแนวโน้ม 30 วัน
            function initCharts() {
                const labels = Array.from({length: 30}, (_, i) => {
                    let d = new Date();
                    d.setDate(d.getDate() - (29 - i));
                    return `${d.getDate()}/${d.getMonth()+1}`;
                });

                // ข้อมูลจำลองเส้นกราฟ 30 วัน
                const dataTrend = [35, 38, 42, 40, 65, 78, 82, 45, 42, 39, 44, 70, 85, 88, 48, 42, 40, 46, 72, 80, 84, 50, 43, 41, 45, 68, 79, 85, 52, 85];
                const dataMilk = dataTrend.map(v => (v * 0.15).toFixed(1));

                const ctx1 = document.getElementById('trendChart').getContext('2d');
                trendChart = new Chart(ctx1, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'ยอดขายคาดการณ์ (แก้ว)',
                            data: dataTrend,
                            borderColor: '#6d4c41',
                            backgroundColor: 'rgba(109, 76, 65, 0.1)',
                            fill: true,
                            tension: 0.3,
                            pointRadius: 3
                        }]
                    },
                    options: { responsive: true, plugins: { legend: { display: false } } }
                });

                const ctx2 = document.getElementById('barChart').getContext('2d');
                barChart = new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: labels.slice(20, 30),
                        datasets: [{
                            label: 'ความต้องการนมสด (ลิตร)',
                            data: dataMilk.slice(20, 30),
                            backgroundColor: '#8d6e63',
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, plugins: { legend: { display: false } } }
                });
            }

            function updatePrediction() {
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
                    const cups = data.predicted_delivery_cups;
                    const milk = data.suggested_milk_liters;
                    
                    document.getElementById('kpi-cups').innerText = cups + ' แก้ว';
                    document.getElementById('kpi-milk').innerText = milk + ' ลิตร';
                    document.getElementById('kpi-box').innerText = cups + ' ชุด';
                    
                    // ปรับสถานะภาระงาน
                    const workload = cups > 70 ? 'สูง (Peak)' : cups > 40 ? 'ปานกลาง' : 'ปกติ';
                    const color = cups > 70 ? '#d84315' : cups > 40 ? '#f57c00' : '#2e7d32';
                    const wlElem = document.getElementById('kpi-workload');
                    wlElem.innerText = workload;
                    wlElem.style.color = color;

                    // อัปเดตกราฟจุดสุดท้าย
                    trendChart.data.datasets[0].data[29] = cups;
                    trendChart.update();
                });
            }

            window.onload = initCharts;
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

    suggested_milk = round(predicted_cups_rounded * 0.15, 1)
    suggested_containers = predicted_cups_rounded

    return {
        "predicted_delivery_cups": predicted_cups_rounded,
        "suggested_milk_liters": suggested_milk,
        "suggested_delivery_cups": suggested_containers,
        "status": "success",
        "message": "คำนวณพยากรณ์ยอดขายและคำแนะนำสั่งวัตถุดิบเรียบร้อยแล้ว"
    }