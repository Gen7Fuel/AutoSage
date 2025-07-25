import streamlit.components.v1 as components
import base64
from pathlib import Path

def main():
    # Optional: Load an image as background or logo
    logo_path = "assets/images/gen7_logo.png"  # Ensure this file exists
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
            }}

            .container {{
                max-width: 1000px;
                margin: auto;
                padding: 40px 20px;
            }}

            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}

            .header img {{
                width: 180px;
                margin-bottom: 10px;
            }}

            .header h1 {{
                margin: 0;
                font-size: 2.5rem;
                color: #2c3e50;
            }}

            .description {{
                text-align: center;
                font-size: 1.2rem;
                color: #555;
                margin-bottom: 50px;
            }}

            .card {{
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                margin-bottom: 30px;
                padding: 20px;
                display: flex;
                flex-direction: row;
                gap: 20px;
                align-items: center;
            }}

            .card img {{
                width: 150px;
                border-radius: 6px;
                object-fit: cover;
            }}

            .card h3 {{
                margin: 0;
                color: #333;
            }}

            .card p {{
                margin: 10px 0 0;
                color: #666;
                font-size: 0.95rem;
            }}

            .footer {{
                text-align: center;
                margin-top: 40px;
                color: #888;
                font-size: 0.85rem;
            }}

            @media (max-width: 768px) {{
                .card {{
                    flex-direction: column;
                    text-align: center;
                }}

                .card img {{
                    width: 100%;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="data:image/png;base64,{logo_base64}" alt="Gen7 Logo" />
                <h1>Welcome to AutoSage</h1>
                <div class="description">Your internal platform for data-driven document automation and business insights</div>
            </div>

            <div class="card">
                <img src="data:image/png;base64,{logo_base64}" alt="Canco">
                <div>
                    <h3>Canco Price Importer</h3>
                    <p>Streamline daily wholesale fuel price updates with this tool that imports, cleans, and outputs a Bookworks-compatible pricing CSV.</p>
                </div>
            </div>

            <div class="card">
                <img src="data:image/png;base64,{logo_base64}" alt="Demand">
                <div>
                    <h3>Demand Analysis Assistant</h3>
                    <p>Analyze historical vendor sales, calculate liquidity ratios, and project inventory needs using a powerful pivot logic engine.</p>
                </div>
            </div>

            <div class="footer">
                &copy; 2025 Gen7Fuel — Built with ❤️ by Peter
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html_code, height=1100, scrolling=True)