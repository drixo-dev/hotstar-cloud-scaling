import os
import re
import base64
import markdown
import subprocess

CSS = """
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
}
body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    margin: 30px auto;
    max-width: 900px;
    color: #1e293b;
    padding: 0 15px;
}
h1 {
    color: #0f172a;
    font-size: 24px;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 8px;
    margin-top: 15px;
}
h2 {
    color: #0369a1;
    font-size: 19px;
    margin-top: 24px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
    page-break-after: avoid;
}
h3 {
    color: #334155;
    font-size: 15px;
    margin-top: 18px;
    page-break-after: avoid;
}
p, li {
    font-size: 13px;
    color: #334155;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    font-size: 12px;
    page-break-inside: avoid;
}
th, td {
    border: 1px solid #cbd5e1;
    padding: 7px 9px;
    text-align: left;
    vertical-align: top;
}
th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
}
tr:nth-child(even) {
    background-color: #f8fafc;
}
code {
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 4px;
    border-radius: 4px;
    font-family: 'Consolas', 'Menlo', monospace;
    font-size: 11.5px;
}
pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 10px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: 'Consolas', 'Menlo', monospace;
    font-size: 11px;
    line-height: 1.4;
    page-break-inside: avoid;
}
blockquote {
    border-left: 4px solid #0284c7;
    margin: 12px 0;
    padding: 6px 14px;
    background-color: #f0f9ff;
    color: #0369a1;
    font-style: italic;
}
img {
    max-width: 95%;
    max-height: 480px;
    height: auto;
    display: block;
    margin: 14px auto;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    page-break-inside: avoid;
}
em {
    color: #475569;
    font-size: 11.5px;
    display: block;
    text-align: center;
    margin-top: -6px;
    margin-bottom: 12px;
}
hr {
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 20px 0;
}
"""

def embed_images_as_base64(html_str, base_dir):
    def replace_src(match):
        alt = match.group(1)
        src = match.group(2)
        full_path = os.path.join(base_dir, src)
        if os.path.exists(full_path):
            with open(full_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(src)[1].lower().replace(".", "")
            if ext == "jpg": ext = "jpeg"
            return f'<img alt="{alt}" src="data:image/{ext};base64,{encoded}" />'
        return match.group(0)

    return re.sub(r'<img\s+alt="([^"]*)"\s+src="([^"]*)"\s*/>', replace_src, html_str)

def compile_doc(md_path, html_path, pdf_path):
    print(f"Compiling {md_path} -> {html_path}...")
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    html_body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'toc'])
    rep_dir = os.path.dirname(os.path.abspath(html_path))
    html_body_embedded = embed_images_as_base64(html_body, rep_dir)
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>IT457 Group 19 Technical Report</title>
<style>
{CSS}
</style>
</head>
<body>
{html_body_embedded}
</body>
</html>"""
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Generating PDF via LibreOffice: {pdf_path}...")
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        os.path.basename(html_path),
        "--outdir", rep_dir
    ]
    res = subprocess.run(cmd, cwd=rep_dir, capture_output=True, text=True)
    if res.returncode != 0:
        print("LibreOffice Error:", res.stderr)
    else:
        print(f"Successfully generated {pdf_path}")

if __name__ == "__main__":
    compile_doc("reports/IT457_Group19_Week2_Report.md", "reports/IT457_Group19_Week2_Report.html", "reports/IT457_Group19_Week2_Report.pdf")
    compile_doc("reports/IT457_Group19_Final_Report.md", "reports/IT457_Group19_Final_Report.html", "reports/IT457_Group19_Final_Report.pdf")
