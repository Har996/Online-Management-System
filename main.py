import datetime
import random
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI(title="Advance AI Student Management System")

# --- 1. MEMORY STATE DATABASE ---
db = {
    "current_module": "analytics",
    "chat_history": [],
    "last_prediction": None,
    "zoom_link": None,
    "zoom_topic": None,
    "zoom_duration": None
}

# --- 2. 15 CORE TECHNICAL BOOKS DATABASE ---
BOOKS_DATABASE = {
    "Python Programming 101": "Chapter 1: Introduction to Variables, Data Types (Strings, Integers, Floats), and Loops. Python is interpreted and dynamically typed. Memory optimization is managed via Automatic Garbage Collection.",
    "Data Structures & Algorithms": "Chapter 3: Linked Lists vs Arrays. Time Complexity analysis using Big O notation. Binary Search Trees offer O(log n) performance for search operations when balanced.",
    "Machine Learning Blueprint": "Chapter 2: Linear Regression minimizes the Residual Sum of Squares (RSS). Gradient Descent iteratively updates weights using the learning rate parameter to converge to global minima.",
    "Deep Learning & Neural Networks": "Chapter 5: Backpropagation algorithm computes the gradient of the loss function with respect to weights using the chain rule. Activation functions like ReLU prevent vanishing gradients.",
    "Database Management Systems (DBMS)": "Chapter 4: ACID Properties (Atomicity, Consistency, Isolation, Durability). Relational integrity is enforced using Primary and Foreign Keys in Structured Query Language (SQL).",
    "Web Development Essentials": "Chapter 1: HTML5 semantic structure, CSS3 Flexbox/Grid layouts, and asynchronous JavaScript (Promises, Async/Await) driving the modern client-side ecosystem.",
    "Cloud Computing Architecture": "Chapter 3: Microservices deployment on AWS using Elastic Container Service (ECS) and serverless computation via AWS Lambda. Load balancing maintains high availability.",
    "Cyber Security Principles": "Chapter 2: Symmetric vs Asymmetric Cryptography. RSA Encryption algorithm relies on the mathematical difficulty of factoring large prime numbers.",
    "Artificial Intelligence Foundation": "Chapter 1: Search algorithms (A* Search, Minimax for game theory, and Heuristics). Agent-based systems perceive environments through sensors and act via actuators.",
    "Operating Systems Concepts": "Chapter 6: Process Scheduling Algorithms (Round Robin, Shortest Job First). Virtual Memory management uses paging and page replacement policies to prevent thrashing.",
    "Computer Networks Protocols": "Chapter 4: The TCP/IP Model layers. OSI Reference Model 7 layers. TCP provides reliable, connection-oriented data streaming via a three-way handshake.",
    "Software Engineering Practices": "Chapter 2: Agile Development Frameworks, Scrum ceremonies, Git Version Control branching strategies (Gitflow), and Continuous Integration/Continuous Deployment (CI/CD) pipelines.",
    "Discrete Mathematics": "Chapter 3: Set Theory, Propositional Logic, Truth Tables, Graph Theory matrices, and Combinatorics principles essential for algorithmic formulation.",
    "Data Science with Pandas": "Chapter 2: Data Manipulation using DataFrames. Handling missing values via imputation, grouping operations, and merging multi-source datasets smoothly.",
    "Natural Language Processing (NLP)": "Chapter 4: Tokenization, Stemming, Lemmatization, TF-IDF vectorization, and modern Transformer architectures (Self-Attention mechanisms) for sequence understanding."
}

# --- 3. AI CHATBOT ENGINE ---
def ai_knowledge_chatbot(msg: str):
    msg = msg.lower()
    if 'status' in msg or 'system' in msg:
        return "🔮 <b>System Pulse:</b> All core nodes operational. Latency 14ms. Database synced with the main administrative network."
    elif 'class' in msg or 'zoom' in msg or 'camera' in msg:
        return "📹 <b>Live Feed Node:</b> System standard WebRTC protocols check active. Live class links generate encrypted tokens valid for 4 hours."
    elif 'book' in msg or 'read' in msg or 'library' in msg:
        return f"📚 <b>Library Matrix:</b> Hamare paas 15 digital textbooks aur academic assets index hain. Aap Left menu se Library select karke read kar sakte hain!"
        
    for title, content in BOOKS_DATABASE.items():
        if any(word in msg for word in title.lower().split() if len(word) > 3):
            return f"🤖 <b>AI Research Output (Based on '{title}'):</b> {content[:180]}..."
            
    return "💡 As your AI controller, I can parse data from our 15 text systems or check parameters. Try asking about 'library books' or 'system status'."

# --- 4. GLOBAL PREMIUM LAYOUT (Lavender + Blue Theme) ---
BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advance AI Student Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root { --bg-lavender: #F3F0FB; --primary-blue: #4A51A3; --accent-lavender: #DCD6F7; }
        body { background-color: var(--bg-lavender); color: #2B2D42; font-family: 'Segoe UI', system-ui, sans-serif; }
    </style>
</head>
<body class="flex h-screen overflow-hidden">
    <div class="w-72 bg-[#4A51A3] text-white flex flex-col justify-between p-5 shadow-xl">
        <div>
            <h1 class="text-2xl font-bold text-center tracking-wide">🎓 AI Student Hub</h1>
            <p class="text-xs text-center text-[#DCD6F7] mb-2">v2.0 Premium Matrix</p>
            <hr class="border-[#DCD6F7] mb-6">
            <nav class="space-y-2">
                <a href="/module/analytics" class="block p-3 rounded-lg hover:bg-[#383D7A] transition [ANALYTICS_ACTIVE]">📊 Dynamic Analytics</a>
                <a href="/module/library" class="block p-3 rounded-lg hover:bg-[#383D7A] transition [LIBRARY_ACTIVE]">📖 Intelligent Library</a>
                <a href="/module/classroom" class="block p-3 rounded-lg hover:bg-[#383D7A] transition [CLASSROOM_ACTIVE]">📹 Live Classroom</a>
                <a href="/module/chatbot" class="block p-3 rounded-lg hover:bg-[#383D7A] transition [CHATBOT_ACTIVE]">🤖 Central Core Chatbot</a>
            </nav>
        </div>
        <div class="p-3 bg-[#383D7A] rounded-lg text-xs text-center border border-[#DCD6F7]/30 text-[#DCD6F7]">
            Active Frame: Lavender & Blue Base
        </div>
    </div>

    <div class="flex-1 overflow-y-auto p-10">
        [CONTENT]
    </div>
</body>
</html>
"""

# --- 5. ROUTES CONTROLLER ---

@app.get("/")
async def root():
    return RedirectResponse(url=f"/module/{db['current_module']}")

@app.get("/module/{module_name}", response_class=HTMLResponse)
async def render_interface(module_name: str, book: str = "Python Programming 101"):
    db["current_module"] = module_name
    content = ""

    # --- MODULE 1: DYNAMIC ANALYTICS (ML ENGINE) ---
    if module_name == "analytics":
        pred_text = f"{db['last_prediction']}%" if db['last_prediction'] else "84.2%"
        content = f"""
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-2">📊 Dynamic System Control & AI Analytics</h1>
        <p class="text-gray-600 mb-8">Real-Time Academic Performance Layer</p>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-5 mb-10">
            <div class="bg-white p-6 rounded-2xl border-2 border-[#DCD6F7] text-center shadow-md">
                <p class="text-xs font-bold text-gray-500 uppercase">Total Enrolled</p><p class="text-3xl font-extrabold text-[#4A51A3] mt-2">2,450</p>
            </div>
            <div class="bg-white p-6 rounded-2xl border-2 border-[#DCD6F7] text-center shadow-md">
                <p class="text-xs font-bold text-gray-500 uppercase">Digital Volumes</p><p class="text-3xl font-extrabold text-[#4A51A3] mt-2">15 Books</p>
            </div>
            <div class="bg-white p-6 rounded-2xl border-2 border-[#DCD6F7] text-center shadow-md">
                <p class="text-xs font-bold text-gray-500 uppercase">Live Network</p><p class="text-3xl font-extrabold text-teal-500 mt-2">Active</p>
            </div>
            <div class="bg-white p-6 rounded-2xl border-2 border-[#DCD6F7] text-center shadow-md">
                <p class="text-xs font-bold text-gray-500 uppercase">Server Integrity</p><p class="text-3xl font-extrabold text-[#4A51A3] mt-2">99.9%</p>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm">
                <h3 class="text-lg font-bold text-[#4A51A3] mb-4">⚙️ Performance Simulator Input</h3>
                <form action="/action/predict" method="post" class="space-y-4 text-sm">
                    <div><label class="block font-medium text-gray-700">Attendance (Days)</label><input type="number" name="days" value="42" class="w-full mt-1 p-2 border rounded-lg"></div>
                    <div><label class="block font-medium text-gray-700">Completed Tasks</label><input type="number" name="tasks" value="35" class="w-full mt-1 p-2 border rounded-lg"></div>
                    <div><label class="block font-medium text-gray-700">Books Read Thoroughly</label><input type="number" name="books" value="8" class="w-full mt-1 p-2 border rounded-lg"></div>
                    <button class="w-full bg-[#4A51A3] text-white p-2.5 rounded-lg font-semibold hover:bg-[#383D7A] transition shadow-md">Compute AI Metrics</button>
                </form>
            </div>
            <div class="lg:col-span-2 bg-white p-8 rounded-2xl border-2 border-[#4A51A3] shadow-md flex flex-col justify-center text-center">
                <p class="text-lg font-semibold text-gray-700">Estimated AI Grade Performance Index</p>
                <p class="text-7xl font-black text-[#4A51A3] my-4">{pred_text}</p>
                <p class="text-xs text-gray-500">Mathematical simulation compiled smoothly via Backend Linear Regression Analysis Weights.</p>
            </div>
        </div>
        """

    # --- MODULE 2: INTELLIGENT LIBRARY (15 BOOKS INTEGRATION) ---
    elif module_name == "library":
        options = "".join([f"<option {'selected' if b == book else ''}>{b}</option>" for b in BOOKS_DATABASE.keys()])
        content = f"""
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-2">📖 AI Powered Digital Library Engine</h1>
        <p class="text-gray-600 mb-6">Browse and extract context directly from 15 high-tier vectorized assets.</p>
        
        <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-md max-w-2xl mb-8">
            <form action="/action/read-book" method="get" class="flex gap-4 items-end">
                <div class="flex-1">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Select Academic Volume to Mount:</label>
                    <select name="book" class="w-full p-2.5 border rounded-lg bg-gray-50 text-sm focus:ring-2 focus:ring-[#4A51A3]">{options}</select>
                </div>
                <button class="bg-[#4A51A3] text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-[#383D7A] transition text-sm">Mount Book</button>
            </form>
        </div>

        <h3 class="text-xl font-bold text-[#4A51A3] mb-3">📑 Current Content Asset Frame: <span class="italic text-gray-700 font-medium">{book}</span></h3>
        <div class="bg-[#FAF9FE] p-6 rounded-xl border-l-8 border-[#4A51A3] font-serif text-lg leading-relaxed text-gray-800 shadow-inner">
            {BOOKS_DATABASE.get(book, "No data content found.")}
        </div>
        """

    # --- MODULE 3: LIVE SECURE CLASSROOM + CAMERA INTEGRATION ---
    elif module_name == "classroom":
        zoom_box = ""
        if db["zoom_link"]:
            zoom_box = f"""
            <div class="bg-emerald-50 border border-emerald-300 p-5 rounded-xl mb-6 text-sm">
                <p class="text-emerald-800 font-bold">🔗 Secure Video Tunnel Active!</p>
                <code class="block bg-white p-2 rounded border my-2 text-xs text-gray-700 select-all">{db['zoom_link']}</code>
                <p class="text-gray-600">Topic: <b>{db['zoom_topic']}</b> | Frame Matrix Allocation: <b>{db['zoom_duration']}</b></p>
            </div>
            """
        content = f"""
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-2">📹 Virtual Synchronous Classroom Interface</h1>
        <p class="text-gray-600 mb-8">Generate live secure session streaming tunnels with instant WebRTC system loops.</p>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-md">
                <h3 class="text-lg font-bold text-[#4A51A3] mb-4">🖥️ Tunnel Setup Controls</h3>
                <form action="/action/zoom-gen" method="post" class="space-y-4 text-sm">
                    <div><label class="block font-medium text-gray-700">Meeting Topic/Subject Matrix</label><input type="text" name="topic" value="Advanced Artificial Intelligence & Neural Architectures" class="w-full mt-1 p-2 border rounded-lg" required></div>
                    <div><label class="block font-medium text-gray-700">Duration Parameter</label><select name="duration" class="w-full mt-1 p-2 border rounded-lg"><option>45 Minutes</option><option>90 Minutes</option></select></div>
                    <button class="w-full bg-[#4A51A3] text-white p-2.5 rounded-lg font-semibold hover:bg-[#383D7A] transition">Generate Secure Stream Gateway Token</button>
                </form>
            </div>
            
            <div class="bg-white p-6 rounded-2xl border border-gray-200 shadow-md flex flex-col justify-between">
                <div>
                    <h3 class="text-lg font-bold text-[#4A51A3] mb-2">📷 Live Pre-Flight Camera Check Module</h3>
                    <p class="text-xs text-gray-500 mb-4">Verify localized capturing media interface pipeline compatibility inside standard browser views.</p>
                    {zoom_box}
                    
                    <div class="relative rounded-xl overflow-hidden bg-slate-900 aspect-video flex items-center justify-center border-2 border-dashed border-[#4A51A3]/30">
                        <video id="webcam" autoplay playsinline class="w-full h-full object-cover transform -scale-x-100"></video>
                        <div class="absolute bottom-3 left-3 bg-black/60 px-2.5 py-1 text-[10px] text-white rounded font-mono tracking-widest">LOCAL_FEED_ACTIVE</div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Native JavaScript handler to access device camera and stream video live on HTML Canvas window
            navigator.mediaDevices.getUserMedia({{ video: true, audio: false }})
                .then(function(stream) {{
                    var video = document.getElementById('webcam');
                    video.srcObject = stream;
                }})
                .catch(function(err) {{
                    console.log("Camera Blocked or Not Found: " + err);
                }});
        </script>
        """

    # --- MODULE 4: CENTRAL AI CHATBOT PANEL ---
    elif module_name == "chatbot":
        chat_html = "".join([
            f'<div class="flex flex-col mb-3 items-end"><div class="bg-[#4A51A3] text-white text-sm p-3 rounded-2xl max-w-md shadow-sm">{c["u"]}</div></div>'
            f'<div class="flex flex-col mb-3 items-start"><div class="bg-gray-100 text-gray-800 text-sm p-3 rounded-2xl max-w-md border shadow-sm">{c["ai"]}</div></div>'
            for c in db["chat_history"]
        ])
        content = f"""
        <h1 class="text-3xl font-bold text-[#4A51A3] mb-2">🤖 Central Intelligence System Chatbot Core</h1>
        <p class="text-gray-600 mb-6">Ask queries across system parameters, machine learning weights, or text references across all 15 contextual volumes.</p>
        
        <div class="bg-white rounded-2xl border border-gray-200 shadow-lg flex flex-col h-[520px] max-w-4xl">
            <div class="flex-1 p-6 overflow-y-auto space-y-4 bg-slate-50/50 rounded-t-2xl" id="chatWindow">
                {chat_html if chat_html else '<p class="text-gray-400 text-center text-sm my-auto pt-20">Awaiting context questions. Try asking: "Explain Deep Learning Backpropagation" or "System status check"</p>'}
            </div>
            
            <div class="p-4 border-t bg-white rounded-b-2xl">
                <form action="/action/chat" method="post" class="flex gap-3">
                    <input type="text" name="msg" placeholder="Type your knowledge query here..." class="flex-1 p-3 border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#4A51A3]" required>
                    <button class="bg-[#4A51A3] text-white px-6 py-3 rounded-xl font-semibold hover:bg-[#383D7A] transition text-sm">Send Vector</button>
                </form>
            </div>
        </div>
        <script>
            var objDiv = document.getElementById("chatWindow");
            objDiv.scrollTop = objDiv.scrollHeight;
        </script>
        """

    # Highlighting Active Layout Side menu element safely
    html_out = BASE_HTML.replace("[CONTENT]", content).replace(f"[{module_name.upper()}_ACTIVE]", "bg-[#383D7A]")
    
    # Wipe un-selected navigation placeholders 
    for m in ["analytics", "library", "classroom", "chatbot"]:
        html_out = html_out.replace(f"[{m.upper()}_ACTIVE]", "")
        
    return HTMLResponse(content=html_out)


# --- 6. ACTION INTERACTION SUBMISSIONS ---

@app.post("/action/predict")
async def action_predict(days: int = Form(...), tasks: int = Form(...), books: int = Form(...)):
    # Local Machine learning Linear regression live weight modeling
    np.random.seed(10)
    X = np.random.randint(5, 50, (150, 3))
    y = X[:, 0] * 1.1 + X[:, 1] * 0.9 + X[:, 2] * 1.8 + np.random.randint(5, 15, 150)
    model = LinearRegression().fit(X, y)
    pred = model.predict(np.array([[days, tasks, books]]))[0]
    db["last_prediction"] = round(min(float(pred), 100.0), 2)
    return RedirectResponse(url="/module/analytics", status_code=303)

@app.get("/action/read-book")
async def action_read_book(book: str):
    return RedirectResponse(url=f"/module/library?book={book}", status_code=303)

@app.post("/action/zoom-gen")
async def action_zoom_gen(topic: str = Form(...), duration: str = Form(...)):
    db["zoom_topic"] = topic
    db["zoom_duration"] = duration
    db["zoom_link"] = f"https://zoom.us/j/9876543210?pwd=SECURE_AI_HUB_{random.randint(1000,9999)}"
    return RedirectResponse(url="/module/classroom", status_code=303)

@app.post("/action/chat")
async def action_chat(msg: str = Form(...)):
    ai_reply = ai_knowledge_chatbot(msg)
    db["chat_history"].append({"u": msg, "ai": ai_reply})
    return RedirectResponse(url="/module/chatbot", status_code=303)