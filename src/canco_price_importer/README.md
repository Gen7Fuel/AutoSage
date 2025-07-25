# AutoSage

## **Canco Price Importer**

## **Authors**

Peter Lee - Data Scientist @gen7fuel - peter@gen7fuel.com 

## **History**

2025.07.25 - Creation.

## **Description**

A Streamlit-based tool to automate daily fuel price updates across Canada, transforming `.xlsx` price sheets into a Bookworks-compatible `.csv` file.

Hosted at: [autosage.gen7fuel.com](http://autosage.gen7fuel.com)

---

## 📌 Project Motivation

Updating daily fuel prices manually from various suppliers across Canada is error-prone and inefficient. This tool streamlines the process by allowing users to upload Excel sheets for Eastern and Western Canada, automatically generating a merged and cleaned CSV file formatted for Bookworks.

---

## ⚙️ What the Tool Does

### Inputs:
- **East Price File** (`.xlsx`) — includes cities like Toronto, Hamilton, London, etc.
- **Rest of Canada Price File** (`.xlsx`) — includes Kamloops, Vancouver, Winnipeg, etc.
- **Original Bookworks CSV File** — serves as a base template for updating.

---

## 🔁 Process Flow

### 1. Parse Excel Files:
- Extract fuel grades and base prices per city.
- Determine the “Effective Date” and format it for Bookworks.
- Normalize data using internal mappings:
  - `supplier_code_map`
  - `inventory_item_map`
  - `supplier_item_map`

### 2. Clean and Consolidate Data:
- Merge East and Rest data into a single DataFrame.
- Remove duplicates, keeping the most recent price updates.
- `'WULSD'` (Winter Diesel) price is set equal to `'ULSD'` (Diesel).
- If there is a discrepancy in base prices across files, the tool records the **higher base price**.
- Only locations with a defined `supplier_code` are processed; cities like **Calgary** and **Edmonton** are ignored.

### 3. Merge with Original CSV:
- Match data by `Supplier Code` and `Inventory Item`.
- Overwrite only where new price or effective date is found.

### 4. Output:
- Display updated CSV in the browser.
- Allow user to download the final Bookworks-ready file.

---

## ✅ Benefits

- **Automated pricing updates** — no manual spreadsheet editing required.
- **Accurate formatting** — fully compatible with Bookworks import expectations.
- **Mapping logic** — ensures consistent and traceable data transformations.
- **Overwrite only when needed** — preserves historical values unless explicitly updated.

---

## 🧰 Technical Overview

- **Frontend:** Streamlit Web UI
- **Backend:** Python + Pandas
- **Excel Parsing:** `openpyxl`
- **Output Format:** `.csv`
- **Mappings:** Defined in `constants.py`

---

## 🔒 Maintenance & Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Excel Format Drift** | Changes in the uploaded file structure may break parsing. | Add row-based validation and raise warnings. |
| **New Cities or Grades** | Missing mappings will skip data. | Regularly update `constants.py`. |
| **Incorrect File Uploads** | Wrong file order or structure causes confusion. | Improve UI prompts and validations. |
| **Downtime** | Hosting issues may delay updates. | Add basic monitoring and fallback instructions. |

### Maintenance Recommendations:
- Review mappings and parsing logic quarterly.
- Add unit tests for parsing functions.
- Monitor server performance or usage.
- Log parsing failures and upload issues.

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

- Email delivery of generated CSV.
- Bookworks API integration (if available).
- Authentication or admin interface.
- Logging of change history or pricing audit trail.
---