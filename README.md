# 🌲 AutoSage

## Intelligent Business Operations Toolkit for Gen7 Fuel  
**Author:** Peter Lee – Data Scientist @gen7fuel – [peter@gen7fuel.com](mailto:peter@gen7fuel.com)  
**Hosted at:** [autosage.gen7fuel.com](http://autosage.gen7fuel.com)

---

## 📌 Overview

**AutoSage** is a collection of internal tools designed to streamline and automate core business operations across Gen7 Fuel — from fuel price updates to retail inventory planning.  

Built with **Streamlit**, these lightweight yet powerful web apps replace tedious spreadsheet tasks with user-friendly, intelligent workflows.

---

## 🧭 Applications Inside AutoSage

### 1. ⛽ Canco Price Importer

> Automates the daily fuel price update workflow for Bookworks.

- Accepts `.xlsx` rack price files from Canco (East + Rest of Canada).
- Normalizes and merges prices using pre-mapped codes.
- Detects effective dates and overwrites only updated prices.
- Outputs a clean `.csv` formatted for direct upload into the Bookworks accounting system.
- Built-in validations to ignore incomplete cities (e.g., Calgary, Edmonton).

🔗 More info: [`apps/canco_price_importer/README.md`](apps/canco_price_importer/README.md)

---

### 2. 📊 Demand Analysis Assistant

> Generates bi-weekly sales forecasts and reorder recommendations from raw sales/purchase reports.

- Upload raw Excel reports from store systems.
- Filter by vendor to generate monthly pivot tables.
- Automatically calculates:
  - Sales performance
  - LIQ %
  - Shelf life
  - Bi-weekly forecasts
  - Safety stock
  - Suggested order quantities
- Download vendor-specific Excel files with ready-to-use insights.

🔗 More info: [`apps/demand_analysis_assistant/README.md`](apps/demand_analysis_assistant/README.md)

---

## 🚀 Why AutoSage?

- 🕒 **Saves time** — automates repetitive business processes  
- 🎯 **Reduces error** — enforces consistent logic across uploads  
- 📈 **Improves decision-making** — delivers data-driven insights to operators  
- 👥 **User-friendly** — no coding or Excel formulas required  

---

## 🔧 Tech Stack

| Component   | Details                  |
|------------|--------------------------|
| Frontend   | [Streamlit](https://streamlit.io) Web Interface |
| Backend    | Python 3 (Pandas, NumPy) |
| File Support | `.xlsx`, `.csv`        |
| Hosting    | Internal Gen7 App Server |

---

## 🔒 Maintenance Notes

| Risk                        | Mitigation                             |
|-----------------------------|-----------------------------------------|
| File format changes         | Add schema detection & better errors    |
| Missing supplier/vendor maps| Update constants in sub-apps            |
| High memory usage on large files | Use Streamlit caching + chunking  |
| App downtime                | Monitor server or host on fallback port |

---

## 📬 Contact

For bugs, updates, or feature ideas:  
📧 [Peter@gen7fuel.com](mailto:peter@gen7fuel.com)

---

## 📅 Changelog

- **2025.07.25** – Initial release of AutoSage with two core modules
- **TBD** – API integration for automated data ingestion
- **TBD** – Authentication layer for multi-user deployment

---