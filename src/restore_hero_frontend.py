"""
Rebuilder that preserves the exact original Valuation Studio as the main view
(as seen in media_1795080640498_4c2e1659.jpg), with:
1. Exact dark cosmic particle vortex banner (zero green bleed, canvas width/height guarded, shadowBlur reset).
2. Valuation Studio is the DEFAULT visible screen on page load.
3. Top search bar, API 9ms, bell, profile avatar REMOVED.
4. Breadcrumb ('Dashboard > Used Car Valuation Studio') and 'Telemetry Sync' REMOVED.
5. Overlapping select arrows FIXED (single clean arrow, background-image: none !important).
6. Mock "Share Report" and "Save Valuation" buttons replaced with fully functional "Bulk CSV Valuation" and "Download Sample CSV".
7. Functional Bulk CSV modal / panel.
8. Navigation links (Overview, Valuation Studio, Bulk CSV, Market Analytics, Model Performance, Project Info) working smoothly.
9. Rupee currency (₹ INR / Lakhs) with 0 remaining dollar signs.
10. Manufacturing Year slider 2006 to 2026.
11. Dynamic 10 Brands & 43 Models.
"""

import os
import sys
import json
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
STITCH_SOURCE = os.path.join(PROJECT_ROOT, "frontend_stitch", "new_stitch", "code.html")
WEIGHTS_PATH = os.path.join(PROJECT_ROOT, "static_model_weights.json")

with open(STITCH_SOURCE, "r", encoding="utf-8") as f:
    html = f.read()

with open(WEIGHTS_PATH, "r", encoding="utf-8") as f:
    weights_data = json.load(f)

# Brand Models mapping
BRAND_MODELS = {
    "Maruti Suzuki": ["Alto K10", "Baleno", "Brezza", "Dzire", "Ertiga", "Swift", "Wagon R"],
    "Hyundai": ["Alcazar", "Creta", "Grand i10 Nios", "Venue", "Verna", "i20"],
    "Tata": ["Altroz", "Harrier", "Nexon", "Punch", "Safari", "Tiago"],
    "Mahindra": ["Bolero", "Scorpio-N", "Thar", "XUV300", "XUV700"],
    "Toyota": ["Fortuner", "Glanza", "Innova Crysta", "Urban Cruiser Hyryder"],
    "Kia": ["Carens", "Seltos", "Sonet"],
    "Honda": ["Amaze", "City", "Elevate"],
    "Volkswagen": ["Polo", "Taigun", "Virtus"],
    "Skoda": ["Kushaq", "Octavia", "Slavia"],
    "MG": ["Astor", "Hector", "ZS EV"]
}

# 1. Title & Favicon Links
head_tags = '''<head>
  <meta charset="utf-8"/>
  <title>CARPRICE AI — Indian Used Car Valuation Studio (₹ INR)</title>
  <link rel="icon" type="image/png" href="static/favicon.png"/>
  <link rel="shortcut icon" href="favicon.ico"/>
  <link rel="apple-touch-icon" href="static/logo.jpg"/>'''

if '<head><meta charset="utf-8"/>' in html:
    html = html.replace('<head><meta charset="utf-8"/>', head_tags)
elif '<head>' in html:
    html = html.replace('<head>', head_tags)

# 1b. Replace Sidebar Logo with New Cyber Artwork
old_logo_pattern = r'<div class="p-space-lg flex items-center gap-space-sm border-b border-primary/10">[\s\S]*?Valuation Engine</div>\s*</div>\s*</div>'
new_logo_html = '''<div class="p-3.5 border-b border-primary/15 flex items-center gap-3 bg-[#030904]/60 backdrop-blur-sm">
  <div class="relative group shrink-0 cursor-pointer" onclick="document.querySelector('aside nav a[data-path=\\'price-prediction-studio\\']')?.click()">
    <div class="absolute -inset-0.5 bg-gradient-to-r from-primary/60 via-lime-400/50 to-emerald-400/60 rounded-xl blur-sm opacity-70 group-hover:opacity-100 transition duration-300"></div>
    <img src="static/logo.jpg" onerror="this.src='logo.jpg'" alt="CARPRICE AI Logo" class="relative w-11 h-11 rounded-xl object-cover border border-primary/40 shadow-[0_0_15px_rgba(163,230,53,0.35)] group-hover:scale-105 transition-transform" />
  </div>
  <div class="overflow-hidden min-w-0 cursor-pointer" onclick="document.querySelector('aside nav a[data-path=\\'price-prediction-studio\\']')?.click()">
    <div class="font-headline-md text-base font-extrabold text-white tracking-tight flex items-center gap-1.5 leading-tight">
      <span class="text-primary font-bold tracking-tight">CARPRICE</span>
      <span class="text-white text-[10px] px-1.5 py-0.5 rounded bg-primary/20 text-primary border border-primary/30 font-mono font-bold">AI</span>
    </div>
    <div class="font-mono text-[9px] text-primary/80 uppercase tracking-widest font-semibold truncate flex items-center gap-1 mt-0.5">
      <span>Indian Valuation Engine</span>
    </div>
  </div>
</div>'''
html = re.sub(old_logo_pattern, new_logo_html, html)

# 2. Add global select CSS to fix double arrow permanently
select_fix_css = """
    /* Fix native select arrow overlap */
    select {
      -webkit-appearance: none !important;
      -moz-appearance: none !important;
      appearance: none !important;
      background-image: none !important;
    }
    select::-ms-expand {
      display: none !important;
    }
"""
html = html.replace('</style>', select_fix_css + '\n  </style>')

# 3. Remove Header completely (search bar, API 9ms, bell, tune, profile avatar)
pos_hdr = html.find('<header class="fixed top-0 left-72 right-0')
if pos_hdr != -1:
    pos_hdr_end = html.find('</header>', pos_hdr)
    if pos_hdr_end != -1:
        html = html[:pos_hdr] + html[pos_hdr_end + 9:]

# 4. Remove Breadcrumb & Telemetry sync bar (Dashboard > Used Car Valuation Studio)
breadcrumb_pattern = r'<!-- Top Navigation & Breadcrumb Layer -->[\s\S]*?<!-- ========================================================================= -->'
html = re.sub(breadcrumb_pattern, '<!-- ========================================================================= -->', html)

# Also remove standalone breadcrumb if comment missing
html = re.sub(r'<div class="flex flex-col gap-space-sm pt-space-md pb-space-sm">[\s\S]*?</div>\s*</div>\s*</div>', '', html)

# 5. Fix pt-16 in main to pt-6 for clean spacing
html = html.replace('<main class="relative w-full pt-16 bg-transparent', '<main class="relative w-full pt-6 bg-transparent')

# 6. Update Navigation in Sidebar
old_nav = '''<nav class="flex-1 px-space-md space-y-space-xs"><a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20" data-path="overview" href="#"><span class="material-symbols-outlined text-[20px]">dashboard</span><span class="">Overview</span></a><a aria-current="page" class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg transition-all duration-150 bg-primary/20 text-primary font-semibold border border-primary/50 shadow-[0_0_20px_rgba(163,230,53,0.25)]" data-path="price-prediction-studio" href="#"><span class="material-symbols-outlined text-[20px] text-primary">insights</span><span class="text-primary font-bold">Price Prediction Studio</span></a><a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20" data-path="market-analytics" href="#"><span class="material-symbols-outlined text-[20px]">query_stats</span><span class="">Market Analytics</span></a><a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20" data-path="model-performance" href="#"><span class="material-symbols-outlined text-[20px]">speed</span><span class="">Model Performance</span></a><a class="flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20" data-path="project-info" href="#"><span class="material-symbols-outlined text-[20px]">info</span><span class="">Project Info</span></a></nav>'''

new_nav = '''<nav class="flex-1 px-space-md space-y-space-xs">
  <a class="nav-item flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg transition-all duration-150 bg-primary/20 text-primary font-semibold border border-primary/50 shadow-[0_0_20px_rgba(163,230,53,0.25)] cursor-pointer" data-path="price-prediction-studio" href="#">
    <span class="material-symbols-outlined text-[20px] text-primary">insights</span>
    <span class="font-bold">Valuation Studio</span>
  </a>
  <a class="nav-item flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20 cursor-pointer" data-path="bulk-csv" href="#">
    <span class="material-symbols-outlined text-[20px]">upload_file</span>
    <span>Bulk CSV Valuation</span>
  </a>
  <a class="nav-item flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20 cursor-pointer" data-path="market-analytics" href="#">
    <span class="material-symbols-outlined text-[20px]">query_stats</span>
    <span>Market Analytics</span>
  </a>
  <a class="nav-item flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20 cursor-pointer" data-path="model-performance" href="#">
    <span class="material-symbols-outlined text-[20px]">speed</span>
    <span>Model Performance</span>
  </a>
  <a class="nav-item flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20 cursor-pointer" data-path="project-info" href="#">
    <span class="material-symbols-outlined text-[20px]">info</span>
    <span>Project Info</span>
  </a>
</nav>'''
html = html.replace(old_nav, new_nav)

# 7. Update Hero Header Badges & Currencies
html = html.replace('Valuation Studio ($ USD / Global)', 'Valuation Studio (₹ INR / India)')
html = html.replace('calculate an instant fair market valuation in USD.', 'calculate an instant fair market valuation in Indian Rupees (₹ INR).')

# 8. Update Manufacturing Year Slider to 2006-2026
old_slider = '<input class="w-full h-2 rounded-lg cursor-pointer" id="yearSlider" max="2024" min="2012" type="range" value="2020"/>'
new_slider = '<input class="w-full h-2 rounded-lg cursor-pointer" id="yearSlider" max="2026" min="2006" type="range" value="2022"/>'
html = html.replace(old_slider, new_slider)

old_ticks = '''<div class="flex justify-between font-label-sm text-label-sm text-outline">
<span class="">2012</span>
<span class="">2016</span>
<span class="">2020</span>
<span class="">2024</span>
</div>'''
new_ticks = '''<div class="flex justify-between font-label-sm text-label-sm text-outline">
<span class="">2006</span>
<span class="">2011</span>
<span class="">2016</span>
<span class="">2021</span>
<span class="">2026</span>
</div>'''
html = html.replace(old_ticks, new_ticks)

# Update default year display
html = html.replace(
    '<span class="px-space-md py-0.5 rounded-full bg-primary text-black font-label-sm text-label-sm font-bold shadow-[0_0_12px_rgba(163,230,53,0.5)]" id="yearDisplay">2020</span>',
    '<span class="px-space-md py-0.5 rounded-full bg-primary text-black font-label-sm text-label-sm font-bold shadow-[0_0_12px_rgba(163,230,53,0.5)]" id="yearDisplay">2022</span>'
)

# 9. Update Manufacturer and Model Dropdowns with inline style preventing double arrows
brand_options_html = '<select style="background-image: none !important; -webkit-appearance: none !important; -moz-appearance: none !important; appearance: none !important;" class="w-full bg-[#09170c] border border-primary/30 text-on-surface px-space-md py-space-sm rounded-lg font-body-md text-body-md focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary cursor-pointer shadow-sm transition-all pr-10" id="manufacturer">\n'
for b in sorted(BRAND_MODELS.keys()):
    sel = ' selected=""' if b == 'Kia' else ''
    brand_options_html += f'  <option class="bg-[#040804] text-white" value="{b}"{sel}>{b}</option>\n'
brand_options_html += '</select>'

html = re.sub(
    r'<select[^>]+id="manufacturer">[\s\S]*?</select>',
    brand_options_html,
    html
)

kia_models_html = '<select style="background-image: none !important; -webkit-appearance: none !important; -moz-appearance: none !important; appearance: none !important;" class="w-full bg-[#09170c] border border-primary/30 text-on-surface px-space-md py-space-sm rounded-lg font-body-md text-body-md focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary cursor-pointer shadow-sm transition-all pr-10" id="modelSelect">\n'
for m in BRAND_MODELS['Kia']:
    sel = ' selected=""' if m == 'Seltos' else ''
    kia_models_html += f'  <option class="bg-[#040804] text-white" value="{m}"{sel}>{m}</option>\n'
kia_models_html += '</select>'

html = re.sub(
    r'<select[^>]+id="modelSelect">[\s\S]*?</select>',
    kia_models_html,
    html
)

# 10. Update Color Swatches
html = html.replace('data-color="Pearl Alpine White" title="Pearl Alpine White"', 'data-color="White" title="Alpine White"')
html = html.replace('data-color="Metallic Silver" title="Metallic Silver"', 'data-color="Silver" title="Metallic Silver"')
html = html.replace('data-color="Dark Obsidian Navy" title="Dark Obsidian Navy"', 'data-color="Black" title="Obsidian Black"')
html = html.replace('data-color="Royal Cobalt Blue" title="Royal Cobalt Blue"', 'data-color="Blue" title="Cobalt Blue"')
html = html.replace('data-color="Crimson Metallic Red" title="Crimson Metallic Red"', 'data-color="Red" title="Crimson Red"')
html = html.replace('data-color="Metallic Charcoal Gray" title="Metallic Charcoal Gray"', 'data-color="Grey" title="Charcoal Grey"')
html = html.replace('>Pearl Alpine White</span>', '>Alpine White</span>')

# 11. Update Service History with no-chevron inline style
new_service = '''<select style="background-image: none !important; -webkit-appearance: none !important; -moz-appearance: none !important; appearance: none !important;" class="w-full bg-[#09170c] border border-primary/30 text-on-surface px-space-md py-space-sm rounded-lg font-body-md text-body-md focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary cursor-pointer shadow-sm transition-all pr-10" id="serviceHistory">
<option class="bg-[#040804] text-white" selected="" value="Authorized Dealer">Authorized Dealer (OEM Certified Logbook)</option>
<option class="bg-[#040804] text-white" value="Independent Garage">Independent Garage (Third-Party Garage)</option>
<option class="bg-[#040804] text-white" value="Partial">Partial History (Mixed Maintenance)</option>
</select>'''
html = re.sub(r'<select[^>]+id="serviceHistory">[\s\S]*?</select>', new_service, html)

# 12. Update Hero Price Display
old_price_block = '''<div class="font-metric-valuation text-metric-valuation tracking-tight font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-primary to-lime-400 neon-lime-glow" id="valuationOutputPrice">
              $21,850.00 <span class="font-headline-md text-headline-md text-primary/70 font-normal">USD</span>
</div>
<div class="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-space-xs">
<span class="material-symbols-outlined text-primary/70 text-[16px]">price_change</span>
<span class="">Confidence Interval: $21,184.38 – $22,515.62 USD (± $665 RMSE)</span>
</div>'''

new_price_block = '''<div class="font-metric-valuation text-metric-valuation tracking-tight font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-primary to-lime-400 neon-lime-glow flex items-baseline gap-2 flex-wrap" id="valuationOutputPrice">
  <span id="priceLakhDisplay">₹ 16.46 Lakh</span> <span class="text-xl font-mono text-primary/80 font-normal" id="valuationOutputInrSub">(₹ 16,45,896 INR)</span>
</div>
<div class="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-space-xs" id="confidenceIntervalDisplay">
<span class="material-symbols-outlined text-primary/70 text-[16px]">price_change</span>
<span id="ciText">Expected Range: ₹ 15.90 Lakh – ₹ 17.01 Lakh (± ₹ 55,579 RMSE)</span>
</div>'''
html = html.replace(old_price_block, new_price_block)

# 13. Update Cohort Price Benchmarks
html = html.replace(
    '<div class="font-label-lg text-label-lg text-on-surface font-semibold mt-0.5 font-mono">$16,200</div>',
    '<div class="font-label-lg text-label-lg text-on-surface font-semibold mt-0.5 font-mono" id="cohortLowPrice">₹ 13.52 Lakh</div>'
)
html = html.replace(
    '<div class="font-label-lg text-label-lg text-on-surface font-semibold mt-0.5 font-mono">$19,400</div>',
    '<div class="font-label-lg text-label-lg text-on-surface font-semibold mt-0.5 font-mono" id="cohortMedianPrice">₹ 16.20 Lakh</div>'
)
html = html.replace(
    '<div class="font-label-lg text-label-lg text-primary font-bold mt-0.5 font-mono neon-lime-glow">$21,850</div>',
    '<div class="font-label-lg text-label-lg text-primary font-bold mt-0.5 font-mono neon-lime-glow" id="cohortHighPrice">₹ 18.25 Lakh</div>'
)

# 14. REMOVE mock "Share Report" and "Save Valuation" buttons, REPLACE WITH FUNCTIONAL BULK CSV BUTTONS
old_action_bar = '''<!-- Report Export & Save Action Bar -->
<div class="grid grid-cols-2 gap-space-sm pt-space-xs">
<button class="py-space-sm px-space-md rounded-lg bg-[#09170c] border border-primary/30 hover:border-primary hover:bg-primary/20 text-on-surface hover:text-primary font-label-lg text-label-lg transition-all flex items-center justify-center gap-space-xs shadow-sm active:scale-95" type="button">
<span class="material-symbols-outlined text-[18px]">share</span>
<span class="">Share Report</span>
</button>
<button class="py-space-sm px-space-md rounded-lg bg-primary hover:bg-lime-400 text-black font-label-lg text-label-lg font-bold transition-all flex items-center justify-center gap-space-xs shadow-[0_0_15px_rgba(163,230,53,0.35)] active:scale-95" type="button">
<span class="material-symbols-outlined text-[18px]">bookmark</span>
<span class="">Save Valuation</span>
</button>
</div>'''

new_action_bar = '''<!-- Functional Bulk Valuation Action Bar -->
<div class="grid grid-cols-2 gap-space-sm pt-space-xs">
  <button id="btnOpenBulkCsv" class="py-space-sm px-space-md rounded-lg bg-primary hover:bg-lime-400 text-black font-label-lg text-label-lg font-bold transition-all flex items-center justify-center gap-space-xs shadow-[0_0_15px_rgba(163,230,53,0.35)] active:scale-95 cursor-pointer" type="button">
    <span class="material-symbols-outlined text-[18px]">upload_file</span>
    <span>Bulk CSV Valuation</span>
  </button>
  <button id="btnDownloadSampleCsv" class="py-space-sm px-space-md rounded-lg bg-[#09170c] border border-primary/30 hover:border-primary hover:bg-primary/20 text-on-surface hover:text-primary font-label-lg text-label-lg transition-all flex items-center justify-center gap-space-xs shadow-sm active:scale-95 cursor-pointer" type="button">
    <span class="material-symbols-outlined text-[18px]">download</span>
    <span>Download Sample CSV</span>
  </button>
</div>'''
html = html.replace(old_action_bar, new_action_bar)

# 15. Create TAB: BULK CSV VALUATION STUDIO (#tab-bulk)
bulk_csv_tab_html = '''
<!-- ========================================================================= -->
<!-- TAB: BULK CSV FLEET VALUATION (#tab-bulk) -->
<!-- ========================================================================= -->
<div id="tab-bulk" class="tab-pane hidden flex-col w-full space-y-space-lg">
  <div class="flex flex-col gap-1">
    <div class="flex items-center gap-2 mb-1">
      <span class="font-label-sm text-label-sm uppercase tracking-wider text-outline">Fleet Telemetry</span>
      <span class="text-primary/60 text-xs">›</span>
      <span class="font-label-sm text-label-sm text-primary font-semibold">Bulk Automated Evaluation</span>
    </div>
    <h1 class="font-headline-xl text-3xl font-bold text-white tracking-tight">Bulk CSV <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-emerald-400 neon-lime-glow">Fleet Valuation Studio</span></h1>
    <p class="font-body-sm text-body-sm text-on-surface-variant max-w-2xl leading-relaxed">
      Upload automobile inventory files in CSV format to compute instant algorithmic valuations for each vehicle in Indian Rupees (₹ INR).
    </p>
  </div>

  <!-- Upload & Action Station Card -->
  <div class="rounded-xl cyber-glass p-space-lg border border-primary/30 space-y-space-md">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-space-md items-center">
      <!-- Upload Drop Zone (Col 2) -->
      <div class="md:col-span-2 border-2 border-dashed border-primary/40 hover:border-primary rounded-xl p-space-lg bg-[#07170a]/60 flex flex-col items-center justify-center text-center cursor-pointer transition-colors relative group" id="bulkDropZone">
        <input type="file" id="bulkCsvFileInput" accept=".csv" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full"/>
        <div class="w-12 h-12 rounded-xl bg-primary/20 border border-primary/40 flex items-center justify-center text-primary group-hover:scale-110 transition-transform mb-2 shadow-[0_0_15px_rgba(163,230,53,0.3)]">
          <span class="material-symbols-outlined text-[28px]">cloud_upload</span>
        </div>
        <div class="font-bold text-white text-base">Click to Upload or Drag &amp; Drop CSV File</div>
        <div class="text-xs text-on-surface-variant mt-1">Supports standard CSV with brand, model, make_year, mileage_kmpl, engine_cc, etc.</div>
      </div>

      <!-- Quick Template & Actions (Col 1) -->
      <div class="flex flex-col gap-space-sm p-space-md rounded-xl bg-[#09170c] border border-primary/20">
        <div class="font-bold text-white text-sm flex items-center gap-1.5">
          <span class="material-symbols-outlined text-primary text-[18px]">description</span>
          <span>Sample Template</span>
        </div>
        <p class="text-xs text-on-surface-variant">Download our pre-populated template with 5 ready-to-test vehicles (Swift, Fortuner, Creta, Thar, Seltos).</p>
        <button id="btnDownloadSampleCsvTemplate" class="w-full py-2.5 px-3 rounded-lg bg-primary hover:bg-lime-400 text-black font-bold text-xs transition-all flex items-center justify-center gap-1.5 shadow-[0_0_12px_rgba(163,230,53,0.3)] cursor-pointer">
          <span class="material-symbols-outlined text-[16px]">download</span>
          <span>Download Sample CSV</span>
        </button>
        <button id="btnLoadDemoFleet" class="w-full py-2 px-3 rounded-lg bg-[#0d2212] border border-primary/30 hover:border-primary text-primary font-semibold text-xs transition-all flex items-center justify-center gap-1.5 cursor-pointer">
          <span class="material-symbols-outlined text-[16px]">play_circle</span>
          <span>Load Demo 5-Car Fleet</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Bulk Results Section (hidden by default until CSV loaded) -->
  <div id="bulkResultsContainer" class="hidden space-y-space-md">
    <!-- Fleet KPI Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-space-md">
      <div class="p-space-md rounded-xl cyber-glass border border-primary/30 space-y-1">
        <div class="text-xs font-mono text-outline uppercase">Vehicles Evaluated</div>
        <div class="text-3xl font-mono font-extrabold text-primary neon-lime-glow" id="bulkTotalVehicles">0</div>
        <div class="text-[11px] text-on-surface-variant">Validated CSV Rows</div>
      </div>
      <div class="p-space-md rounded-xl cyber-glass border border-primary/30 space-y-1">
        <div class="text-xs font-mono text-outline uppercase">Total Fleet Valuation</div>
        <div class="text-3xl font-mono font-extrabold text-white" id="bulkTotalValuation">₹ 0.00 Lakh</div>
        <div class="text-[11px] text-primary" id="bulkTotalValuationInr">₹ 0 INR</div>
      </div>
      <div class="p-space-md rounded-xl cyber-glass border border-primary/30 space-y-1">
        <div class="text-xs font-mono text-outline uppercase">Average Value Per Car</div>
        <div class="text-3xl font-mono font-extrabold text-white" id="bulkAvgValuation">₹ 0.00 Lakh</div>
        <div class="text-[11px] text-on-surface-variant">Calculated OLS Mean</div>
      </div>
    </div>

    <!-- Export Action Bar -->
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="text-sm text-on-surface font-semibold flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
        <span id="bulkStatusText">Valuation Complete: 5 vehicles processed in 2.1 ms</span>
      </div>
      <button id="btnExportValuedCsv" class="py-2 px-4 rounded-lg bg-primary hover:bg-lime-400 text-black font-bold text-xs transition-all flex items-center gap-1.5 shadow-[0_0_12px_rgba(163,230,53,0.3)] cursor-pointer">
        <span class="material-symbols-outlined text-[16px]">file_download</span>
        <span>Export Evaluated CSV with Valuations</span>
      </button>
    </div>

    <!-- Results Table Card -->
    <div class="rounded-xl cyber-glass border border-primary/30 overflow-hidden shadow-lg">
      <div class="overflow-x-auto">
        <table class="w-full text-left font-body-sm text-xs">
          <thead class="bg-[#07170a] border-b border-primary/20 text-outline uppercase font-mono">
            <tr>
              <th class="py-3 px-3">#</th>
              <th class="py-3 px-3">Vehicle Spec</th>
              <th class="py-3 px-3">Year</th>
              <th class="py-3 px-3">Powertrain / Fuel</th>
              <th class="py-3 px-3">Mileage / Engine</th>
              <th class="py-3 px-3">Owners</th>
              <th class="py-3 px-3 text-right">Predicted Valuation (₹ Lakh)</th>
              <th class="py-3 px-3 text-right">Amount (₹ INR)</th>
            </tr>
          </thead>
          <tbody id="bulkResultsTableBody" class="divide-y divide-primary/10 font-mono">
            <!-- Dynamically populated rows -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
'''

# Import Analytics, Performance, Info tabs
from src.build_stitch_frontend import analytics_tab_html, performance_tab_html, info_tab_html

# Add official emblem badge card to Project Info tab
info_tab_branded = info_tab_html.replace(
    '<div class="grid grid-cols-1 md:grid-cols-3 gap-space-lg">',
    '''<div class="p-space-lg rounded-xl cyber-glass border border-primary/30 flex flex-col sm:flex-row items-center gap-6 mb-6 shadow-[0_0_20px_rgba(163,230,53,0.15)]">
      <div class="relative group shrink-0">
        <div class="absolute -inset-1 bg-gradient-to-r from-primary/50 to-emerald-500/50 rounded-2xl blur-md opacity-75"></div>
        <img src="static/logo.jpg" onerror="this.src='logo.jpg'" alt="CARPRICE AI Official Emblem" class="relative w-28 h-28 rounded-2xl object-cover border-2 border-primary/50 shadow-[0_0_25px_rgba(163,230,53,0.4)]" />
      </div>
      <div class="space-y-1 text-left">
        <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-primary/15 border border-primary/40 text-primary font-mono text-xs">
          <span class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
          Indian Valuation Engine — Official Emblem
        </div>
        <h2 class="text-2xl font-bold text-white tracking-tight">CARPRICE AI <span class="text-primary font-mono text-base">(Indian Valuation Engine)</span></h2>
        <p class="text-xs text-on-surface-variant leading-relaxed">
          Autonomous bio-synthetic kinetic valuation platform engineered for India's automobile market across 10 top OEMs, 43 passenger models, 2006–2026 manufacturing spectrum, and leakage-free algorithmic regression inference.
        </p>
      </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-space-lg">'''
)

# 16. Wrap the Valuation Studio in #tab-studio (ACTIVE AND VISIBLE BY DEFAULT, NOT HIDDEN!)
pos_hero = html.find('<!-- HERO INTERACTIVE VORTEX / COSMIC TELEMETRY BANNER')
if pos_hero == -1:
    pos_hero = html.find('<section class="relative w-full rounded-2xl cyber-glass')

pos_end_workspace = html.find('</main>')

html = (
    html[:pos_hero]
    + '<div id="tab-studio" class="tab-pane flex flex-col w-full">\n'
    + html[pos_hero:pos_end_workspace]
    + '\n</div>\n'
    + bulk_csv_tab_html
    + '\n'
    + analytics_tab_html
    + '\n'
    + performance_tab_html
    + '\n'
    + info_tab_branded
    + '\n'
    + html[pos_end_workspace:]
)

# 17. Fix canvas code in html to ENSURE ZERO SHADOW ACCUMULATION & OBSIDIAN DARK BASE
# We replace the renderVortex function in html:
old_render_vortex_str = '''function renderVortex() {
      if (mouse.isHovering) {
        vortexCenter.targetX = width * 0.68 + (mouse.x - width * 0.68) * 0.18;
        vortexCenter.targetY = height * 0.62 + (mouse.y - height * 0.62) * 0.18;
      }
      vortexCenter.x += (vortexCenter.targetX - vortexCenter.x) * 0.08;
      vortexCenter.y += (vortexCenter.targetY - vortexCenter.y) * 0.08;

      ctx.clearRect(0, 0, width, height);

      // Deep glowing dark green backdrop
      const bgGrad = ctx.createRadialGradient(
        vortexCenter.x, vortexCenter.y, 5,
        vortexCenter.x, vortexCenter.y, width * 0.7
      );'''

new_render_vortex_str = '''function renderVortex() {
      if (mouse.isHovering) {
        vortexCenter.targetX = width * 0.68 + (mouse.x - width * 0.68) * 0.18;
        vortexCenter.targetY = height * 0.62 + (mouse.y - height * 0.62) * 0.18;
      }
      vortexCenter.x += (vortexCenter.targetX - vortexCenter.x) * 0.08;
      vortexCenter.y += (vortexCenter.targetY - vortexCenter.y) * 0.08;

      // Always reset shadowBlur and globalAlpha to prevent shadow accumulation
      ctx.shadowBlur = 0;
      ctx.shadowColor = 'transparent';
      ctx.globalAlpha = 1.0;
      ctx.setLineDash([]);
      ctx.clearRect(0, 0, width, height);

      // Solid obsidian black base ensures background is never solid lime green
      ctx.fillStyle = '#030904';
      ctx.fillRect(0, 0, width, height);

      // Deep glowing dark green backdrop
      const safeRadius = Math.max(10, width * 0.7);
      const bgGrad = ctx.createRadialGradient(
        vortexCenter.x, vortexCenter.y, 5,
        vortexCenter.x, vortexCenter.y, safeRadius
      );'''
html = html.replace(old_render_vortex_str, new_render_vortex_str)

# Also fix resize in initVortexHeroCanvas
old_resize_str = '''function resize() {
      const rect = canvas.getBoundingClientRect();
      width = canvas.width = rect.width;
      height = canvas.height = rect.height;
    }
    window.addEventListener('resize', resize);
    resize();'''

new_resize_str = '''function resize() {
      const rect = canvas.getBoundingClientRect();
      const w = Math.round(rect.width || canvas.offsetWidth || 1200);
      const h = Math.round(rect.height || canvas.offsetHeight || 350);
      if (w > 0 && h > 0) {
        width = canvas.width = w;
        height = canvas.height = h;
      }
    }
    window.addEventListener('resize', resize);
    resize();
    if (window.ResizeObserver) {
      new ResizeObserver(() => resize()).observe(canvas.parentElement || canvas);
    }'''
html = html.replace(old_resize_str, new_resize_str)

# 18. Inject the Complete Interactive Script
js_engine = '''
  // =========================================================================
  // 3. INTERACTIVE UI FORM LOGIC, TAB NAVIGATION, ML & BULK CSV VALUATION
  // =========================================================================
  const BRAND_MODELS = ''' + json.dumps(BRAND_MODELS) + ''';
  const ML_WEIGHTS = ''' + json.dumps(weights_data) + ''';
  const USD_TO_INR = 83.5;

  let currentBulkEvaluatedCars = [];

  document.addEventListener('DOMContentLoaded', () => {
    // -----------------------------------------------------------------------
    // A. TAB NAVIGATION (Valuation Studio, Bulk CSV, Analytics, Performance, Info)
    // -----------------------------------------------------------------------
    const navLinks = document.querySelectorAll('aside nav a.nav-item, [data-switch]');
    const tabPanes = {
      'overview': 'tab-studio',
      'price-prediction-studio': 'tab-studio',
      'bulk-csv': 'tab-bulk',
      'market-analytics': 'tab-analytics',
      'model-performance': 'tab-performance',
      'project-info': 'tab-info'
    };

    function switchTab(path) {
      const targetTabId = tabPanes[path] || 'tab-studio';
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
      const activeTab = document.getElementById(targetTabId);
      if (activeTab) {
        activeTab.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
        // Trigger canvas resize so vortex is crystal sharp
        window.dispatchEvent(new Event('resize'));
      }

      document.querySelectorAll('aside nav a.nav-item').forEach(link => {
        if (link.dataset.path === path || (path === 'overview' && link.dataset.path === 'price-prediction-studio')) {
          link.className = 'nav-item flex items-center gap-space-sm px-space-md py-space-sm rounded-lg transition-all duration-150 bg-primary/20 text-primary font-semibold border border-primary/50 shadow-[0_0_20px_rgba(163,230,53,0.25)] cursor-pointer';
          const icon = link.querySelector('.material-symbols-outlined');
          if (icon) icon.className = 'material-symbols-outlined text-[20px] text-primary';
          const span = link.querySelector('span:not(.material-symbols-outlined)');
          if (span) span.className = 'font-bold';
        } else {
          link.className = 'nav-item flex items-center gap-space-sm px-space-md py-space-sm rounded-lg font-label-lg text-label-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary transition-all duration-150 border border-transparent hover:border-primary/20 cursor-pointer';
          const icon = link.querySelector('.material-symbols-outlined');
          if (icon) icon.className = 'material-symbols-outlined text-[20px]';
          const span = link.querySelector('span:not(.material-symbols-outlined)');
          if (span) span.className = '';
        }
      });
    }

    document.querySelectorAll('aside nav a.nav-item').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const path = link.dataset.path;
        if (path) switchTab(path);
      });
    });

    document.querySelectorAll('[data-switch]').forEach(btn => {
      btn.addEventListener('click', () => {
        const path = btn.dataset.switch;
        if (path) switchTab(path);
      });
    });

    const openBulkBtn = document.getElementById('btnOpenBulkCsv');
    if (openBulkBtn) {
      openBulkBtn.addEventListener('click', () => switchTab('bulk-csv'));
    }

    // -----------------------------------------------------------------------
    // B. BRAND & MODEL SELECT LOGIC
    // -----------------------------------------------------------------------
    const mfgSelect = document.getElementById('manufacturer');
    const modelSelect = document.getElementById('modelSelect');

    function populateModels(brand, selectedModel = null) {
      if (!modelSelect) return;
      const models = BRAND_MODELS[brand] || [];
      modelSelect.innerHTML = '';
      models.forEach((m, idx) => {
        const opt = document.createElement('option');
        opt.className = 'bg-[#040804] text-white';
        opt.value = m;
        opt.textContent = m;
        if (selectedModel ? m === selectedModel : idx === 0) {
          opt.selected = true;
        }
        modelSelect.appendChild(opt);
      });
      updateSummaryChip();
    }

    if (mfgSelect) {
      mfgSelect.addEventListener('change', (e) => {
        populateModels(e.target.value);
        triggerPrediction();
      });
    }

    if (modelSelect) {
      modelSelect.addEventListener('change', () => {
        updateSummaryChip();
        triggerPrediction();
      });
    }

    // -----------------------------------------------------------------------
    // C. YEAR SLIDER (2006 to 2026)
    // -----------------------------------------------------------------------
    const yearSlider = document.getElementById('yearSlider');
    const yearDisplay = document.getElementById('yearDisplay');

    if (yearSlider && yearDisplay) {
      yearSlider.addEventListener('input', (e) => {
        yearDisplay.textContent = e.target.value;
        updateSummaryChip();
        triggerPrediction();
      });
    }

    // -----------------------------------------------------------------------
    // D. OWNERS SLIDER
    // -----------------------------------------------------------------------
    const ownersSlider = document.getElementById('ownersSlider');
    const ownersDisplay = document.getElementById('ownersDisplay');
    const chipOwner = document.getElementById('chipOwner');

    if (ownersSlider && ownersDisplay) {
      ownersSlider.addEventListener('input', (e) => {
        const val = e.target.value;
        ownersDisplay.textContent = val == 1 ? '1 Owner (Prime Equity)' : `${val} Registered Owners`;
        if (chipOwner) chipOwner.textContent = `${val} Owner${val > 1 ? 's' : ''}`;
        triggerPrediction();
      });
    }

    // -----------------------------------------------------------------------
    // E. FUEL BUTTONS
    // -----------------------------------------------------------------------
    const fuelBtns = document.querySelectorAll('.fuel-btn');
    const chipPower = document.getElementById('chipPower');
    const engineInput = document.getElementById('engineInput');
    let selectedFuel = 'Petrol';

    fuelBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        fuelBtns.forEach(b => {
          b.className = 'fuel-btn py-space-xs px-space-sm rounded-md font-label-md text-label-md text-center transition-all text-on-surface-variant hover:text-primary hover:bg-surface-container-high';
        });
        btn.className = 'fuel-btn py-space-xs px-space-sm rounded-md font-label-md text-label-md text-center transition-all bg-primary text-black font-bold shadow-[0_0_15px_rgba(163,230,53,0.4)]';
        selectedFuel = btn.dataset.val || btn.textContent.trim();
        
        if (selectedFuel === 'Electric') {
          if (engineInput) engineInput.value = '0 CC (EV Motor)';
        } else if (engineInput && engineInput.value.includes('0 CC')) {
          engineInput.value = '1497 CC';
        }
        if (chipPower) {
          chipPower.textContent = `${engineInput ? engineInput.value.replace(' CC', '').trim() : '1497'} CC ${selectedFuel}`;
        }
        triggerPrediction();
      });
    });

    // -----------------------------------------------------------------------
    // F. TRANSMISSION BUTTONS
    // -----------------------------------------------------------------------
    const transBtns = document.querySelectorAll('.trans-btn');
    let selectedTrans = 'Automatic';

    transBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        transBtns.forEach(b => {
          b.className = 'trans-btn py-space-sm px-space-md rounded-lg font-label-lg text-label-lg text-center transition-all bg-[#09170c] border border-primary/20 text-on-surface-variant hover:text-primary hover:border-primary/50 shadow-sm';
        });
        btn.className = 'trans-btn py-space-sm px-space-md rounded-lg font-label-lg text-label-lg text-center transition-all bg-primary text-black font-bold shadow-[0_0_20px_rgba(163,230,53,0.45)] border border-primary';
        selectedTrans = (btn.dataset.trans && btn.dataset.trans.toLowerCase() === 'manual') ? 'Manual' : 'Automatic';
        triggerPrediction();
      });
    });

    // -----------------------------------------------------------------------
    // G. COLOR SWATCHES
    // -----------------------------------------------------------------------
    const swatches = document.querySelectorAll('.color-swatch');
    const colorLabel = document.getElementById('selectedColorName');
    let selectedColor = 'White';

    swatches.forEach(swatch => {
      swatch.addEventListener('click', () => {
        swatches.forEach(s => {
          s.classList.remove('ring-2', 'ring-primary', 'ring-offset-2', 'ring-offset-[#071209]');
          s.innerHTML = '';
        });
        swatch.classList.add('ring-2', 'ring-primary', 'ring-offset-2', 'ring-offset-[#071209]');
        swatch.innerHTML = '<span class="material-symbols-outlined text-[#030704] text-[18px] absolute inset-0 m-auto flex items-center justify-center font-bold">check</span>';
        selectedColor = swatch.dataset.color || 'White';
        if (colorLabel) colorLabel.textContent = swatch.getAttribute('title') || selectedColor;
        triggerPrediction();
      });
    });

    // -----------------------------------------------------------------------
    // H. ACCIDENT STEPPER & INSURANCE TOGGLE
    // -----------------------------------------------------------------------
    const decBtn = document.getElementById('decAccident');
    const incBtn = document.getElementById('incAccident');
    const accidentDisplay = document.getElementById('accidentCount');
    let accidentCount = 0;

    if (decBtn && incBtn && accidentDisplay) {
      decBtn.addEventListener('click', () => {
        if (accidentCount > 0) {
          accidentCount--;
          accidentDisplay.textContent = accidentCount;
          triggerPrediction();
        }
      });
      incBtn.addEventListener('click', () => {
        accidentCount++;
        accidentDisplay.textContent = accidentCount;
        triggerPrediction();
      });
    }

    const insuranceToggle = document.getElementById('insuranceToggle');
    if (insuranceToggle) {
      insuranceToggle.addEventListener('change', () => triggerPrediction());
    }

    const serviceSelect = document.getElementById('serviceHistory');
    const chipService = document.getElementById('chipService');
    if (serviceSelect) {
      serviceSelect.addEventListener('change', () => {
        if (chipService) chipService.textContent = serviceSelect.value;
        triggerPrediction();
      });
    }

    // -----------------------------------------------------------------------
    // I. NUMERICAL INPUTS
    // -----------------------------------------------------------------------
    const mileageInput = document.getElementById('mileageInput');
    if (mileageInput) {
      mileageInput.addEventListener('change', () => triggerPrediction());
    }
    if (engineInput) {
      engineInput.addEventListener('change', () => {
        if (chipPower) {
          chipPower.textContent = `${engineInput.value.replace(' CC', '').trim()} CC ${selectedFuel}`;
        }
        triggerPrediction();
      });
    }

    // -----------------------------------------------------------------------
    // J. PRESET BUTTONS
    // -----------------------------------------------------------------------
    const presets = document.querySelectorAll('.preset-btn');
    presets.forEach(p => {
      p.addEventListener('click', () => {
        const type = p.dataset.preset;
        if (type === 'swift') {
          if (mfgSelect) mfgSelect.value = 'Maruti Suzuki';
          populateModels('Maruti Suzuki', 'Swift');
          if (yearSlider) yearSlider.value = 2021;
          if (yearDisplay) yearDisplay.textContent = '2021';
          if (engineInput) engineInput.value = '1197 CC';
          if (mileageInput) mileageInput.value = '22.4 km/l';
          selectFuel('Petrol');
          selectTrans('Manual');
        } else if (type === 'fortuner') {
          if (mfgSelect) mfgSelect.value = 'Toyota';
          populateModels('Toyota', 'Fortuner');
          if (yearSlider) yearSlider.value = 2023;
          if (yearDisplay) yearDisplay.textContent = '2023';
          if (engineInput) engineInput.value = '2755 CC';
          if (mileageInput) mileageInput.value = '14.2 km/l';
          selectFuel('Diesel');
          selectTrans('Automatic');
        } else if (type === 'mg') {
          if (mfgSelect) mfgSelect.value = 'MG';
          populateModels('MG', 'ZS EV');
          if (yearSlider) yearSlider.value = 2022;
          if (yearDisplay) yearDisplay.textContent = '2022';
          if (engineInput) engineInput.value = '0 CC (EV Motor)';
          if (mileageInput) mileageInput.value = '18.0 km/l';
          selectFuel('Electric');
          selectTrans('Automatic');
        }
        triggerPrediction();
      });
    });

    function selectFuel(fuelName) {
      fuelBtns.forEach(btn => {
        if (btn.dataset.val === fuelName || btn.textContent.trim() === fuelName) {
          btn.click();
        }
      });
    }

    function selectTrans(transName) {
      transBtns.forEach(btn => {
        if (btn.textContent.toLowerCase().includes(transName.toLowerCase())) {
          btn.click();
        }
      });
    }

    function updateSummaryChip() {
      const chipSpec = document.getElementById('chipSpec');
      if (!chipSpec) return;
      const yr = yearSlider ? yearSlider.value : '2022';
      const mfgText = mfgSelect ? mfgSelect.value : 'Kia';
      const modelText = modelSelect ? modelSelect.value : 'Seltos';
      chipSpec.textContent = `${yr} ${mfgText} ${modelText}`;
    }

    // -----------------------------------------------------------------------
    // K. CLIENT-SIDE ML REGRESSION ENGINE
    // -----------------------------------------------------------------------
    function parseNumeric(val, defaultVal = 0) {
      if (val === null || val === undefined) return defaultVal;
      if (typeof val === 'number') return isNaN(val) ? defaultVal : val;
      const str = String(val).trim();
      const match = str.match(/[-+]?[0-9]*\\.?[0-9]+/);
      if (match) {
        const parsed = parseFloat(match[0]);
        return isNaN(parsed) ? defaultVal : parsed;
      }
      return defaultVal;
    }

    function calculateClientPrediction(car) {
      const year = parseInt(car.make_year) || 2022;
      const carAge = 2026 - year;
      const mileage = parseNumeric(car.mileage_kmpl, 16.5);
      const engine = parseNumeric(car.engine_cc, 1497);
      const owners = parseInt(car.owner_count) || 1;
      const accidents = parseInt(car.accidents_reported) || 0;
      const accidentStatus = accidents > 0 ? 1 : 0;

      const numVals = [year, mileage, engine, owners, accidents, carAge, accidentStatus];
      const scaledNum = numVals.map((v, i) => (v - ML_WEIGHTS.scaler_mean[i]) / ML_WEIGHTS.scaler_scale[i]);

      const activeCats = new Set([
        `brand_${car.brand}`,
        `model_${car.model}`,
        `fuel_type_${car.fuel_type}`,
        `transmission_${car.transmission}`,
        `color_${car.color}`,
        `service_history_${car.service_history}`,
        `insurance_valid_${car.insurance_valid}`
      ]);

      const catVals = ML_WEIGHTS.cat_features.map(cat => activeCats.has(cat) ? 1.0 : 0.0);
      const featVector = scaledNum.concat(catVals);

      let predUsd = ML_WEIGHTS.intercept;
      for (let i = 0; i < featVector.length; i++) {
        predUsd += featVector[i] * ML_WEIGHTS.coef[i];
      }
      predUsd = Math.max(1500.0, predUsd);
      const predInr = predUsd * USD_TO_INR;

      return {
        pred_usd: predUsd,
        pred_inr: predInr,
        formatted_lakh: (predInr / 100000).toFixed(2),
        formatted_inr: Math.round(predInr).toLocaleString('en-IN')
      };
    }

    function formatLakhs(val) {
      const num = Number(val);
      if (isNaN(num) || num <= 0) return '₹ 0.00 Lakh';
      return `₹ ${(num / 100000).toFixed(2)} Lakh`;
    }

    function updateDisplays(predObj) {
      if (!predObj) return;
      const predInr = Number(predObj.pred_inr);
      const predUsd = Number(predObj.pred_usd);
      if (isNaN(predInr) || predInr <= 0) return;

      const formattedLakh = predObj.formatted_lakh || (predInr / 100000).toFixed(2);
      const formattedInr = predObj.formatted_inr || Math.round(predInr).toLocaleString('en-IN');

      const priceLakhElem = document.getElementById('priceLakhDisplay');
      const inrSubElem = document.getElementById('valuationOutputInrSub');
      const ciDisplay = document.getElementById('ciText');
      const cohortLow = document.getElementById('cohortLowPrice');
      const cohortMedian = document.getElementById('cohortMedianPrice');
      const cohortHigh = document.getElementById('cohortHighPrice');

      if (priceLakhElem) {
        priceLakhElem.textContent = `₹ ${formattedLakh} Lakh`;
      }
      if (inrSubElem) {
        inrSubElem.textContent = `(₹ ${formattedInr} INR)`;
      }

      // Dynamic confidence bounds (RMSE ~ ₹ 55,579)
      const rmseInr = 55579;
      const lowInr = Math.max(125000, predInr - rmseInr);
      const highInr = predInr + rmseInr;

      if (ciDisplay) {
        ciDisplay.textContent = `Expected Range: ₹ ${(lowInr/100000).toFixed(2)} Lakh – ₹ ${(highInr/100000).toFixed(2)} Lakh (± ₹ 55,579 RMSE)`;
      }

      if (cohortLow) cohortLow.textContent = formatLakhs(predInr * 0.82);
      if (cohortMedian) cohortMedian.textContent = formatLakhs(predInr * 0.98);
      if (cohortHigh) cohortHigh.textContent = formatLakhs(predInr);
    }

    function getCurrentCarPayload() {
      return {
        brand: mfgSelect ? mfgSelect.value : 'Kia',
        model: modelSelect ? modelSelect.value : 'Seltos',
        make_year: yearSlider ? parseInt(yearSlider.value) : 2022,
        mileage_kmpl: parseNumeric(mileageInput ? mileageInput.value : 16.5, 16.5),
        engine_cc: parseNumeric(engineInput ? engineInput.value : 1497, 1497),
        fuel_type: selectedFuel,
        transmission: selectedTrans,
        color: selectedColor,
        owner_count: ownersSlider ? parseInt(ownersSlider.value) : 1,
        service_history: serviceSelect ? serviceSelect.value : 'Authorized Dealer',
        accidents_reported: accidentCount,
        insurance_valid: (insuranceToggle && insuranceToggle.checked) ? 'Yes' : 'No'
      };
    }

    let debounceTimer = null;
    function triggerPrediction() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const car = getCurrentCarPayload();
        // 1. Instant client-side linear regression evaluation
        const pred = calculateClientPrediction(car);
        if (pred && !isNaN(pred.pred_inr)) {
          updateDisplays(pred);
        }

        // 2. Optional server query if hosted on Flask /api/predict
        fetch('/api/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(car)
        })
        .then(res => res.ok ? res.json() : null)
        .then(data => {
          if (data && data.success) {
            const inrVal = Number(data.price_inr ?? data.prediction_inr);
            const usdVal = Number(data.price_usd ?? data.prediction_usd);
            if (!isNaN(inrVal) && inrVal > 0) {
              updateDisplays({
                pred_usd: usdVal,
                pred_inr: inrVal,
                formatted_lakh: (inrVal / 100000).toFixed(2),
                formatted_inr: Math.round(inrVal).toLocaleString('en-IN')
              });
            }
          }
        })
        .catch(() => {
          // Static environment fallback
        });
      }, 50);
    }

    const calcBtn = document.getElementById('calcValuationBtn');
    if (calcBtn) {
      calcBtn.addEventListener('click', () => {
        const originalText = calcBtn.innerHTML;
        calcBtn.innerHTML = '<span class="material-symbols-outlined text-[24px] animate-spin text-black">refresh</span><span class="text-black">Computing Telemetry &amp; Regression Matrices...</span>';
        calcBtn.disabled = true;

        setTimeout(() => {
          triggerPrediction();
          calcBtn.innerHTML = originalText;
          calcBtn.disabled = false;
          const priceCard = document.getElementById('valuationOutputPrice');
          if (priceCard) {
            priceCard.classList.add('scale-105', 'transition-transform');
            setTimeout(() => priceCard.classList.remove('scale-105'), 300);
          }
        }, 350);
      });
    }

    // -----------------------------------------------------------------------
    // L. FULLY FUNCTIONAL BULK CSV VALUATION ENGINE
    // -----------------------------------------------------------------------
    const sampleCsvData = `brand,model,make_year,mileage_kmpl,engine_cc,fuel_type,transmission,color,owner_count,service_history,accidents_reported,insurance_valid
Maruti Suzuki,Swift,2021,22.4,1197,Petrol,Manual,White,1,Authorized Dealer,0,Yes
Toyota,Fortuner,2023,14.2,2755,Diesel,Automatic,White,1,Authorized Dealer,0,Yes
Hyundai,Creta,2022,17.0,1497,Petrol,Automatic,Silver,1,Authorized Dealer,0,Yes
Mahindra,Thar,2022,15.2,1997,Diesel,Manual,Black,2,Partial,1,No
Kia,Seltos,2020,16.5,1497,Petrol,Automatic,Grey,1,Authorized Dealer,0,Yes`;

    function downloadSampleCsvFile() {
      const blob = new Blob([sampleCsvData], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'car_fleet_valuation_template.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    const btnDownloadSample1 = document.getElementById('btnDownloadSampleCsv');
    const btnDownloadSample2 = document.getElementById('btnDownloadSampleCsvTemplate');
    if (btnDownloadSample1) btnDownloadSample1.addEventListener('click', downloadSampleCsvFile);
    if (btnDownloadSample2) btnDownloadSample2.addEventListener('click', downloadSampleCsvFile);

    function parseCsvString(csvText) {
      const lines = csvText.trim().split(/\\r?\\n/).filter(line => line.trim().length > 0);
      if (lines.length < 2) return [];
      const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
      const records = [];

      for (let i = 1; i < lines.length; i++) {
        const parts = lines[i].split(',').map(p => p.trim());
        if (parts.length >= headers.length) {
          const rowObj = {};
          headers.forEach((h, idx) => {
            rowObj[h] = parts[idx];
          });
          records.push(rowObj);
        }
      }
      return records;
    }

    function processBulkCars(carsList) {
      if (!carsList || carsList.length === 0) return;
      const startTime = performance.now();
      let totalInr = 0;
      const evaluated = [];

      carsList.forEach((car, index) => {
        const payload = {
          brand: car.brand || 'Maruti Suzuki',
          model: car.model || 'Swift',
          make_year: parseInt(car.make_year) || 2022,
          mileage_kmpl: parseNumeric(car.mileage_kmpl, 18.0),
          engine_cc: parseNumeric(car.engine_cc, 1497),
          fuel_type: car.fuel_type || 'Petrol',
          transmission: car.transmission || 'Manual',
          color: car.color || 'White',
          owner_count: parseInt(car.owner_count) || 1,
          service_history: car.service_history || 'Authorized Dealer',
          accidents_reported: parseInt(car.accidents_reported) || 0,
          insurance_valid: car.insurance_valid || 'Yes'
        };

        const pred = calculateClientPrediction(payload);
        totalInr += pred.pred_inr;

        evaluated.push({
          index: index + 1,
          ...payload,
          pred_usd: pred.pred_usd,
          pred_inr: pred.pred_inr,
          formatted_lakh: pred.formatted_lakh,
          formatted_inr: pred.formatted_inr
        });
      });

      const elapsed = (performance.now() - startTime).toFixed(1);
      currentBulkEvaluatedCars = evaluated;

      const resContainer = document.getElementById('bulkResultsContainer');
      const totalVehiclesElem = document.getElementById('bulkTotalVehicles');
      const totalValuationElem = document.getElementById('bulkTotalValuation');
      const totalValuationInrElem = document.getElementById('bulkTotalValuationInr');
      const avgValuationElem = document.getElementById('bulkAvgValuation');
      const statusTextElem = document.getElementById('bulkStatusText');
      const tbody = document.getElementById('bulkResultsTableBody');

      if (resContainer) resContainer.classList.remove('hidden');
      if (totalVehiclesElem) totalVehiclesElem.textContent = evaluated.length;
      
      const totalLakhs = (totalInr / 100000).toFixed(2);
      if (totalValuationElem) {
        if (totalInr >= 10000000) {
          totalValuationElem.textContent = `₹ ${(totalInr / 10000000).toFixed(2)} Crore`;
        } else {
          totalValuationElem.textContent = `₹ ${totalLakhs} Lakh`;
        }
      }
      if (totalValuationInrElem) {
        totalValuationInrElem.textContent = `(₹ ${Math.round(totalInr).toLocaleString('en-IN')} INR)`;
      }

      const avgLakhs = ((totalInr / evaluated.length) / 100000).toFixed(2);
      if (avgValuationElem) avgValuationElem.textContent = `₹ ${avgLakhs} Lakh`;

      if (statusTextElem) {
        statusTextElem.textContent = `Valuation Complete: ${evaluated.length} vehicles processed in ${elapsed} ms`;
      }

      if (tbody) {
        tbody.innerHTML = '';
        evaluated.forEach(item => {
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-primary/5 transition-colors';
          tr.innerHTML = `
            <td class="py-2.5 px-3 text-outline font-mono">${item.index}</td>
            <td class="py-2.5 px-3 font-semibold text-white">${item.brand} ${item.model}</td>
            <td class="py-2.5 px-3 text-on-surface">${item.make_year}</td>
            <td class="py-2.5 px-3 text-on-surface-variant">${item.fuel_type} / ${item.transmission}</td>
            <td class="py-2.5 px-3 text-on-surface-variant">${item.mileage_kmpl} km/l / ${item.engine_cc} CC</td>
            <td class="py-2.5 px-3 text-on-surface-variant">${item.owner_count}</td>
            <td class="py-2.5 px-3 text-right font-bold text-primary font-mono neon-lime-glow">₹ ${item.formatted_lakh} Lakh</td>
            <td class="py-2.5 px-3 text-right text-on-surface font-mono">₹ ${item.formatted_inr}</td>
          `;
          tbody.appendChild(tr);
        });
      }
    }

    const fileInput = document.getElementById('bulkCsvFileInput');
    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (event) => {
            const text = event.target.result;
            const parsed = parseCsvString(text);
            if (parsed.length > 0) {
              processBulkCars(parsed);
            } else {
              alert('Could not parse vehicles from the uploaded CSV. Please check formatting or download the sample template.');
            }
          };
          reader.readAsText(file);
        }
      });
    }

    const btnDemoFleet = document.getElementById('btnLoadDemoFleet');
    if (btnDemoFleet) {
      btnDemoFleet.addEventListener('click', () => {
        const parsed = parseCsvString(sampleCsvData);
        processBulkCars(parsed);
      });
    }

    const btnExportValuedCsv = document.getElementById('btnExportValuedCsv');
    if (btnExportValuedCsv) {
      btnExportValuedCsv.addEventListener('click', () => {
        if (!currentBulkEvaluatedCars || currentBulkEvaluatedCars.length === 0) return;
        const headers = ['brand','model','make_year','mileage_kmpl','engine_cc','fuel_type','transmission','color','owner_count','service_history','accidents_reported','insurance_valid','predicted_price_lakh','predicted_price_inr'];
        const rows = [headers.join(',')];

        currentBulkEvaluatedCars.forEach(c => {
          rows.push([
            c.brand,
            c.model,
            c.make_year,
            c.mileage_kmpl,
            c.engine_cc,
            c.fuel_type,
            c.transmission,
            c.color,
            c.owner_count,
            c.service_history,
            c.accidents_reported,
            c.insurance_valid,
            `₹ ${c.formatted_lakh} Lakh`,
            c.pred_inr
          ].join(','));
        });

        const csvContent = rows.join('\\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'evaluated_automobile_fleet_valuations.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    // Initialize values
    updateSummaryChip();
    triggerPrediction();
  });
</script>
</body>
</html>
'''

# Find script starting point
pos_script_start = html.find('// 3. INTERACTIVE UI FORM LOGIC')
if pos_script_start != -1:
    html = html[:pos_script_start] + js_engine
else:
    pos_last_script = html.rfind('<script>')
    if pos_last_script != -1:
        html = html[:pos_last_script] + '<script>' + js_engine

index_path = os.path.join(PROJECT_ROOT, "index.html")
template_path = os.path.join(PROJECT_ROOT, "templates", "index.html")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

with open(template_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully rebuilt:")
print(f"-> {index_path} ({len(html)} bytes)")
print(f"-> {template_path} ({len(html)} bytes)")
