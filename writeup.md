### AH shit, here we go again!!!

# 🛰️ SkyShadow Backend: Phase 1 Workflow (Arush)

**Objective:** specific steps to go from zero to a live Satellite API.

### **Step 1: The "Clean Room" Setup**
* **Action:** Create the project folder (`SkyShadow`) and open in VS Code.
* **Command:** Create the Virtual Environment to isolate libraries.
    `python3 -m venv .venv`
* **Command:** Activate the "Box" (Mac/Linux).
    `source .venv/bin/activate`
* **Verification:** Ensure terminal line starts with `(.venv)`.

### **Step 2: Tool Installation**
* **Action:** Install the 3 core pillars of the backend.
* **Command:**
    `pip install fastapi uvicorn earthengine-api`
    * `fastapi`: The Web Server.
    * `uvicorn`: The Server Runner.
    * `earthengine-api`: The Google Link.

### **Step 3: The Mac SSL Fix (Crucial)**
* **Context:** Mac Python doesn't trust Google's certificates by default.
* **Action:** Run the certificate installer script included with Python.
* **Command:** `/Applications/Python\ 3.13/Install\ Certificates.command`

### **Step 4: Google Authentication**
* **Action:** Link your terminal to your Google Cloud account.
* **Command:** `earthengine authenticate`
* **Process:**
    1. Browser opens -> Login with GEE email.
    2. Select "Generate Token".
    3. Copy the long code -> Paste into Terminal -> Enter.

### **Step 5: The Project Identity**
* **Context:** The script failed initially because it didn't know *where* to bill the credits.
* **Discovery:** Found the specific **Project ID** in Google Cloud Console.
* **Your ID:** `global-sun-484918-f5`
* **Implementation:** Always use `ee.Initialize(project='global-sun-484918-f5')` in Python scripts.

### **Step 6: VS Code Configuration**
* **Context:** The "Play" button was using the wrong Python.
* **Fix:**
    1. Open a Python file.
    2. Click the python version in the bottom right corner.
    3. Select the one marked `('.venv': venv)`.
    4. Or, use the terminal directly to run files (safer).

### **Step 7: The "Single Dot" Architecture**
* **Structure:** We split the backend into two files:
    1.  **`engine.py`**: Handles the math. Connects to GEE, fetches Sentinel-2, calculates NDVI.
    2.  **`main.py`**: Handles the traffic. Uses FastAPI to create the `/analyze` link.

### **Step 8: Launch**
* **Command:** Start the live server.
    `uvicorn main:app --reload`
* **Success Metric:**
    * Visit: `http://127.0.0.1:8000/analyze?lat=28.61&lon=77.20`
    * Output: Real JSON data showing "Vegetation found".