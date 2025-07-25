# AutoSage

## **Demand Analysis Assistant**

### **Author**  
Peter Lee – Data Scientist @gen7fuel – [peter@gen7fuel.com](mailto:peter@gen7fuel.com)

### **History**  
2025.07.25 – Creation.

---

## 🧠 Description

The **Demand Analysis Assistant** is a Streamlit-powered internal tool to help inventory analysts and buyers assess product movement, calculate bi-weekly sales forecasts, and determine reordering needs across different vendors and stores.  

This tool processes exported purchase and sales reports (from POS or ERP systems), and outputs a fully analyzed Excel pivot table per vendor, making inventory decision-making fast, data-driven, and repeatable.

---

## 📌 Project Motivation

Manual forecasting of purchase quantities and on-hand inventory is slow and inconsistent. This tool removes the guesswork by calculating:

- Historical monthly sales  
- Bi-weekly sales trends  
- Shelf life of products (based on movement)  
- Recommended reorders based on safety stock logic  

It is designed to support Gen7 Fuel buyers and store operators in reducing stockouts and overstock, especially for high-volume categories like **vape** and **cannabis**.

---

## ⚙️ What the Tool Does

### ✅ Inputs:
- An Excel file (exported raw sales/purchase report) per location.
- Vendor filter dropdown in-app to select a target vendor.

---

### 🔁 Process Flow

1. **Upload Raw File**  
   - Parses and cleans the uploaded Excel file.  
   - Extracts `Month`, `UPC`, `Vendor`, `Purch QTY`, `QTY`, and `QTY, On Hand`.

2. **Vendor Selection**  
   - Automatically detects all vendors from the dataset.  
   - User selects one to generate analysis.

3. **Pivot Table Creation**  
   - Monthly pivot of:  
     - Purchase Quantity  
     - Sale Quantity  
     - On-Hand Quantity  
     - LIQ % = Sales / (Sales + On Hand)  
   - Fills missing months with 0s to ensure time continuity.

4. **Sales Forecasting & Inventory Logic**  
   - **Cumulative Sales (`Sale QTY`)**  
   - **Shelf Life** = number of months with sales activity  
   - **Avg Sales/Mnth**  
   - **Bi-Weekly Forecast** = Rounded (Avg Sales/Mnth ÷ 2)  
   - **Safety Stock** = 50% of Bi-Weekly Sales  
   - **Order Quantity** = Forecast + Safety - Current Stock (if needed)

5. **Output**  
   - Clean pivot table sorted by highest selling products  
   - Downloadable Excel file with all calculations prefilled

---

## 🧮 Example Calculations

| Metric               | Formula                                      |
|----------------------|----------------------------------------------|
| `LIQ %`              | `QTY / (QTY + On Hand)`                      |
| `Shelf Life`         | Count of months with `QTY > 0`              |
| `Avg Sales/Mnth`     | `Sale QTY / Shelf Life`                      |
| `Bi-Weekly Forecast` | Rounded(`Avg Sales/Mnth / 2`)                |
| `Safety STK`         | 50% of forecast                              |
| `Order`              | If needed: `Forecast + Safety - On Hand`     |

---

## 🧰 Technical Overview

- **Frontend:** Streamlit  
- **Backend:** Python (Pandas, NumPy)  
- **Excel Engine:** `openpyxl`  
- **UI Interaction:** File Upload, Vendor Dropdown  
- **Output Format:** Downloadable `.xlsx` pivot table

---

## ✅ Benefits

- 🧮 **Automated forecasting logic**  
- 📦 **Improved inventory accuracy**  
- 🕒 **Time-saving for buyers**  
- 📉 **Reduces human error in Excel**  
- 💡 **Vendor-specific insight**

---

## 🔒 Maintenance & Risks

| Risk               | Description                                  | Mitigation                        |
|--------------------|----------------------------------------------|------------------------------------|
| **Format Drift**   | Input Excel layout might change over time.   | Add row-based schema detection.   |
| **Vendor Mismatch**| Filtering fails if vendor names differ.      | Normalize vendor names pre-filter.|
| **Incorrect Inputs**| Users might upload wrong files or formats.  | Show user-friendly error messages.|
| **Performance**    | Large files may slow Streamlit.              | Use caching and chunk processing. |

---

## 🧼 User-Friendly Error Handling

If something breaks, the tool displays this message:

```
🐞 Something went wrong!
Please make sure all file formats and structures are correct.
If the issue persists, contact Peter@gen7fuel.com for help 💌
```

With a toggleable section to view full traceback for debugging. 🧑‍🔧

---

## 🚀 Future Enhancements

- Multi-vendor batch processing  
- Visualization of trends (e.g. charts)  
- Filter by store, category, or SKU group  
- Integration with POS or inventory APIs  
- AI-powered demand anomaly detection

---
