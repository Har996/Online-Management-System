import datetime
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI(title="Smart AI Management System")
templates = Jinja2Templates(directory="templates")

# --- MOCK DATABASE STATE (In-Memory) ---
db = {
    "logged_in": False,
    "current_module": "dashboard",
    "chat_history": []
}

# --- MACHINE LEARNING ENGINE ---
def get_ml_prediction(days: int, tasks: int, books: int):
    np.random.seed(42)
    X = np.random.randint(1, 50, (100, 3))
    y = X[:, 0] * 1.2 + X[:, 1] * 0.8 + X[:, 2] * 2.0 + np.random.randint(10, 30, 100)
    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict(np.array([[days, tasks, books]]))
    return round(min(float(pred[0]), 100.0), 2)

# --- CHATBOT INTELLIGENCE ---
def ai_chatbot(msg: str):
    msg = msg.lower()
    if 'status' in msg or 'dashboard' in msg:
        return "System status nominal hai. All modules (Hostel, Library, Inventory) online hain."
    elif 'book' in msg or 'library' in msg:
        return "Library section se aap books issue kar sakte hain. Fine calculation auto-managed hai."
    elif 'zoom' in msg or 'meeting' in msg:
        return "Online classes schedule karne ke liye Appointment section check karein."
    else:
        return "Main aapka Smart AI assistant hoon. Aap mujhse system performance ya modules ke baare me pooch sakte hain!"

# --- JINJA2 GLOBAL HTML TEMPLATE (Base layout with Lavender Theme) ---
BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart AI Management System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --bg-lavender: #F3F0FB;
            --primary-blue: #4A51A3;
            --accent-lavender: #DCD6F7;
            --text-main: #2B2D42;
        }
        body { background-color: var(--bg-lavender); color: var(--text-main); }
    </style>
</head>
<body class="flex h-screen overflow-hidden">
    <div class="w-64 bg-[#4A51A3] text-white flex flex-col justify-between p-4 shadow-lg">
        <div>
            <h2 class="text-2xl font-bold text-center mb-2">Smart AI System</h2>
            <hr class="border-[#DCD6F7] mb-6">
            <nav class="space-y-2">
                <a href="/module/dashboard" class="block p-3 rounded hover:bg-[#383D7A] {% if active_module == 'dashboard' %}bg-[#383D7A]{% endif %}">📊 Dashboard Analytics</a>
                <a href="/module/library" class="block p-3 rounded hover:bg-[#383D7A] {% if active_module == 'library' %}bg-[#383D7A]{% endif %}">📚 Library Management</a>
                <a href="/module/inventory" class="block p-3 rounded hover:bg-[#383D7A] {% if active_module == 'inventory' %}bg-[#383D7A]{% endif %}">📦 Inventory Module</a>
                <a href="/module/zoom" class="block p-3 rounded hover:bg-[#383D7A] {% if active_module == 'zoom' %}bg-[#383D7A]{% endif %}">📅 Appointments & Zoom</a>
                <a href="/module/feedback" class="block p-3 rounded hover:bg-[#383D7A] {% if active_module == 'feedback' %}bg-[#383D7A]{% endif %}">📝 Feedback & Complaints</a>
            </nav>
        </div>
        <a href="/logout" class="block text-center bg-red-500 hover:bg-red-600 p-2 rounded text-sm font-semibold">🚪 Logout Platform</a>
    </div>

    <div class="flex-1 flex flex-col overflow-y-auto p-8">
        {{ content | safe }}
    </div>
</body>
</html>
"""

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def index():
    if not db["logged_in"]:
        return RedirectResponse(url="/login")
    return RedirectResponse(url=f"/module/{db['current_module']}")

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    # Beautiful Tailwind Login Page
    return """
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="min-h-screen flex items-center justify-center bg-[#F3F0FB]">
        <div class="bg-white p-8 rounded-xl shadow-md border-2 border-[#DCD6F7] max-w-4xl flex w-full gap-8 m-4">
            <div class="w-1/2">
                <h1 class="text-2xl font-bold text-[#4A51A3] mb-4">🔑 Enterprise System Gateway</h1>
                <form action="/login" method="post" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" name="username" class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-[#4A51A3]" required>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" name="password" class="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-[#4A51A3]" required>
                    </div>
                    <button type="submit" class="w-full bg-[#4A51A3] text-white p-2 rounded-md hover:bg-[#383D7A] transition font-semibold">Login</button>
                </form>
            </div>
            <div class="w-1/2 bg-blue-50 p-6 rounded-lg flex flex-col justify-center border border-blue-200">
                <p class="text-blue-800 font-medium">💡 College Demo Accounts:</p>
                <p class="text-sm text-blue-700 mt-2">Use Username: <code class="bg-blue-100 px-1 py-0.5 rounded">admin</code> & Password: <code class="bg-blue-100 px-1 py-0.5 rounded">admin</code> to log in instantly without database setups.</p>
            </div>
        </div>
    </div>
    """

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin":
        db["logged_in"] = True
        return RedirectResponse(url="/", status_code=303)
    return RedirectResponse(url="/login?error=invalid", status_code=303)

@app.get("/logout")
async def logout():
    db["logged_in"] = False
    return RedirectResponse(url="/login")

@app.get("/module/{module_name}", response_class=HTMLResponse)
async def render_module(module_name: str):
    if not db["logged_in"]:
        return RedirectResponse(url="/login")
    
    db["current_module"] = module_name
    content = ""

    if module_name == "dashboard":
        score = get_ml_prediction(25, 40, 8)
        chat_html = "".join([f"<p class='text-sm mb-1'><b>You:</b> {c['u']}<br><span class='text-green-600'><b>AI:</b> {c['ai']}</span></p>" for c in db["chat_history"][-3:]])
        
        content = f"""
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-2">📊 Core Enterprise Control Dashboard</h1>
        <h3 class="text-lg text-gray-600 mb-6">Real-Time System Infrastructure Metrics</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-white p-6 rounded-xl border-2 border-[#DCD6F7] text-center shadow-sm">
                <p class="text-sm text-gray-500 font-medium">Total Users</p>
                <p class="text-3xl font-bold text-[#4A51A3] mt-2">1,248</p>
            </div>
            <div class="bg-white p-6 rounded-xl border-2 border-[#DCD6F7] text-center shadow-sm">
                <p class="text-sm text-gray-500 font-medium">Active Catalog Books</p>
                <p class="text-3xl font-bold text-[#4A51A3] mt-2">4,820</p>
            </div>
            <div class="bg-white p-6 rounded-xl border-2 border-[#DCD6F7] text-center shadow-sm">
                <p class="text-sm text-gray-500 font-medium">Low Stock Alerts</p>
                <p class="text-3xl font-bold text-red-500 mt-2">3 Items</p>
            </div>
            <div class="bg-white p-6 rounded-xl border-2 border-[#DCD6F7] text-center shadow-sm">
                <p class="text-sm text-gray-500 font-medium">AI Performance Index</p>
                <p class="text-3xl font-bold text-amber-500 mt-2">{score}%</p>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2 bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                <h3 class="text-xl font-bold text-[#4A51A3] mb-4">System Activity Analysis</h3>
                <p class="text-gray-500 text-sm mb-4">[Mock Data Visualized Layer Active]</p>
                <div class="h-48 bg-slate-50 border border-dashed border-gray-300 rounded flex items-center justify-center text-gray-400">
                    📈 Line Chart Placeholder (Requests, Transactions, API Hits)
                </div>
            </div>
            <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
                <div>
                    <h3 class="text-xl font-bold text-[#4A51A3] mb-4">🤖 AI System Chatbot</h3>
                    <div class="bg-gray-50 p-3 rounded-md h-32 overflow-y-auto mb-4 border border-gray-100">
                        {chat_html if chat_html else "<p class='text-gray-400 text-sm'>Ask something below...</p>"}
                    </div>
                </div>
                <form action="/chatbot" method="post" class="flex gap-2">
                    <input type="text" name="msg" placeholder="Ask System Intelligence..." class="flex-1 p-2 border rounded-md text-sm" required>
                    <button class="bg-[#4A51A3] text-white px-3 py-1 text-sm rounded hover:bg-[#383D7A]">Ask</button>
                </form>
            </div>
        </div>
        """
    elif module_name == "library":
        content = """
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-6">📚 Library Automation Module</h1>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm max-w-xl">
            <form action="/action/library" method="post" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Student Roll Number</label>
                    <input type="text" class="w-full mt-1 p-2 border rounded-md" required>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Select Book Title</label>
                    <select class="w-full mt-1 p-2 border rounded-md">
                        <option>Introduction to Python</option>
                        <option>Data Structures with Java</option>
                        <option>Machine Learning Blueprint</option>
                    </select>
                </div>
                <button type="submit" class="bg-[#4A51A3] text-white p-2 rounded-md hover:bg-[#383D7A] transition w-full font-semibold">Issue Asset</button>
            </form>
        </div>
        """
    elif module_name == "inventory":
        content = """
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-6">📦 Asset & Stock Inventory Analytics</h1>
        <div class="bg-white rounded-xl shadow-sm border overflow-hidden">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-50 border-b">
                        <th class="p-4 font-semibold text-gray-600">Product Name</th>
                        <th class="p-4 font-semibold text-gray-600">SKU Code</th>
                        <th class="p-4 font-semibold text-gray-600">Current Stock</th>
                        <th class="p-4 font-semibold text-gray-600">Status</th>
                    </tr>
                </thead>
                <tbody class="divide-y text-sm">
                    <tr><td class="p-4">Office Chairs</td><td class="p-4">INV-CH-01</td><td class="p-4">45</td><td class="p-4 text-green-600 font-medium">In Stock</td></tr>
                    <tr><td class="p-4">A4 Paper Rims</td><td class="p-4">INV-PP-12</td><td class="p-4">120</td><td class="p-4 text-green-600 font-medium">In Stock</td></tr>
                    <tr class="bg-red-50"><td class="p-4 font-medium text-red-700">LED Projectors</td><td class="p-4 text-red-700">INV-PR-04</td><td class="p-4 text-red-700 font-bold">2</td><td class="p-4 text-red-600 font-bold">LOW STOCK ALERT</td></tr>
                    <tr><td class="p-4">LAN Cables</td><td class="p-4">INV-CB-88</td><td class="p-4">85</td><td class="p-4 text-green-600 font-medium">In Stock</td></tr>
                </tbody>
            </table>
        </div>
        """
    elif module_name == "zoom":
        content = """
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-6">📅 Virtual Sessions & Zoom Integration</h1>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm max-w-xl">
            <form action="/action/zoom" method="post" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Meeting Subject / Class Topic</label>
                    <input type="text" class="w-full mt-1 p-2 border rounded-md" required>
                </div>
                <button type="submit" class="bg-[#4A51A3] text-white p-2 rounded-md hover:bg-[#383D7A] transition w-full font-semibold">Generate Secure Zoom Link</button>
            </form>
        </div>
        """
    elif module_name == "feedback":
        content = """
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-6">📝 Feedback & Complaint Logging Layer</h1>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm max-w-xl">
            <form action="/action/feedback" method="post" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Category</label>
                    <select class="w-full mt-1 p-2 border rounded-md"><option>Feedback</option><option>System Bug</option></select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Detailed Message</label>
                    <textarea class="w-full mt-1 p-2 border rounded-md h-24" required></textarea>
                </div>
                <button type="submit" class="bg-[#4A51A3] text-white p-2 rounded-md hover:bg-[#383D7A] transition w-full font-semibold">Submit Report</button>
            </form>
        </div>
        """

    # Injecting inner HTML content into global Layout
    html_out = BASE_HTML.replace("{{ content | safe }}", content).replace("{% if active_module == '" + module_name + "' %}bg-[#383D7A]{% endif %}", "bg-[#383D7A]")
    return HTMLResponse(content=html_out)

@app.post("/chatbot")
async def handle_chat(msg: str = Form(...)):
    if db["logged_in"]:
        ai_reply = ai_chatbot(msg)
        db["chat_history"].append({"u": msg, "ai": ai_reply})
    return RedirectResponse(url="/module/dashboard", status_code=303)

# Action Alerts (Feedback triggers)
@app.post("/action/{action_type}")
async def handle_actions(action_type: str):
    # Dummy alert action redirection back
    return RedirectResponse(url=f"/module/{action_type}", status_code=303)