# 🤖 ML-Model-Generator

This Streamlit application allows users to generate machine learning models based on text descriptions. It supports both **Keras (TensorFlow)** and **PyTorch**, providing an interactive interface to generate, modify, and visualize models.  

---

## 🚀 Features  

✅ **Chatbot Interface:** Describe your model, and an AI-powered assistant will generate the corresponding code.  
✅ **Code Editor:** Modify the generated model code before running it.  
✅ **Model Execution:** Execute and extract models from the generated code.  
✅ **Visualization:** View the model architecture using `visualkeras` (for Keras).  
✅ **Interactive UI:** Scrollable columns for better usability.  

---

## 🏗️ Tech Stack  

- **Frontend:** Streamlit  
- **Backend:** OpenAI API (for model generation)  
- **Machine Learning:** TensorFlow/Keras, PyTorch  
- **Visualization:** `visualkeras` (Keras).

---

## 📜 Installation  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/avinashkella/ML-Model-Viewer
cd your repo-name
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)  
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies  
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables  
Create a `.env` file and add:  
```ini
OPENAI_API_KEY=your_api_key
ORGANIZATION=your_organization_id
```

---

## 🚀 Running the Application  

Run the Streamlit app with:  
```sh
streamlit run app.py
```

---

## 📌 How It Works  

### **1️⃣ ML Model Generator (Left Panel)**  
- Enter a description of the model you want (e.g., "CNN for image classification or Unet model using tensorflow").  
- Click **"Send"**, and the chatbot will generate model code using OpenAI.  
- The generated model is stored in session state and passed to the code editor.  

### **2️⃣ Code Editor (Middle Panel)**  
- The generated model code appears here.  
- Modify the code if needed.  
- Click **"Run Model"** to extract the model.  

### **3️⃣ Model Visualization (Right Panel)**  
- Displays the model summary and visualization.  
- **Keras Models**: Uses `visualkeras` for architecture and `.summary()` for layers.  
- **PyTorch Models**: Uses `torchsummary` for summary.

---

## 🖼️ Screenshots  

### **Model Code Editor & Chatbot**  
![Model Visualization](https://github.com/avinashkella/ML-Model-Viewer/blob/main/images/CNN.png) 

### **Model Visualization**  
![Model Visualization](https://github.com/avinashkella/ML-Model-Viewer/blob/main/images/unet.png) 
 

---

## 🛠️ To-Do / Future Improvements  

- ✅ Implement `torchview` for PyTorch visualization.  
- ✅ Improve the chatbot response for better model accuracy.  
- ⏳ Add support for other ML frameworks (e.g., Scikit-Learn).  
- ⏳ Allow users to download generated model code as a `.py` file.  


