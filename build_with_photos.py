"""
Comprehensive Avinox bike spreadsheet - now with Photo Link and Instagram columns
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
wb.remove(wb.active)

# =========================================================================
# SHEET 1: Master comparison with full specs + photo + IG
# =========================================================================
ws = wb.create_sheet("Bikes Full Spec")

headers = [
    "Brand", "Model", "Build/Trim", "Country", "Status",
    "Motor", "Peak W", "Peak Nm",
    "Battery (Wh)", "Battery Type", "Removable",
    "Front Travel (mm)", "Rear Travel (mm)",
    "Frame", "Wheels Setup",
    "Weight (kg)", "Weight Source",
    "Fork", "Rear Shock", "Drivetrain", "Brakes", "Wheelset", "Dropper",
    "GBP £", "EUR €", "USD $", "CAD $", "AUD $",
    "Photo Link", "Instagram (action shots)",
    "Notes / Caveats", "Source URL(s)"
]

header_font = Font(bold=True, color="FFFFFF", name="Arial", size=9)
header_fill = PatternFill("solid", fgColor="1F4E79")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
data_font = Font(name="Arial", size=8)
data_align = Alignment(vertical="center", wrap_text=True)

green_fill = PatternFill("solid", fgColor="C6EFCE")
blue_fill = PatternFill("solid", fgColor="DDEBF7")
yellow_fill = PatternFill("solid", fgColor="FFF2CC")
red_fill = PatternFill("solid", fgColor="FFCCCC")

thin = Side(style='thin', color='BFBFBF')
border = Border(left=thin, right=thin, top=thin, bottom=thin)

for col, h in enumerate(headers, 1):
    c = ws.cell(row=1, column=col, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = header_align
    c.border = border

# IG handles by brand
IG = {
    "Amflow": "https://www.instagram.com/amflowbikes/",
    "Atherton": "https://www.instagram.com/athertonbikes/",
    "BH": "https://www.instagram.com/bh_bikes/",
    "Canyon": "https://www.instagram.com/canyon/",
    "Commencal": "https://www.instagram.com/commencalbikes/",
    "Crestline": "https://www.instagram.com/crestlinebikes/",
    "Crussis": "https://www.instagram.com/crussis_en/",
    "Forbidden": "https://www.instagram.com/forbiddenbikecompany/",
    "Forestal": "https://www.instagram.com/forestalbikes/",
    "Lee Cougan": "https://www.instagram.com/leecouganbicycles/",
    "MAXX": "https://www.instagram.com/maxxbikes/",
    "Megamo": "https://www.instagram.com/megamo_bicycles/",
    "MMR": "https://www.instagram.com/mmrbikes/",
    "Mondraker": "https://www.instagram.com/mondrakerbikes/",
    "Olympia": "https://www.instagram.com/olympiacicli/",
    "Orange": "https://www.instagram.com/orangebikes/",
    "Pivot": "https://www.instagram.com/pivotcycles/",
    "Raymon": "https://www.instagram.com/r__raymon/",
    "Rotwild": "https://www.instagram.com/rotwildbikes/",
    "Steppenwolf": "https://www.instagram.com/steppenwolfbikes/",
    "Teewing": "https://www.instagram.com/teewingbikes/",
    "Thömus": "https://www.instagram.com/thoemus/",
    "Unno": "https://www.instagram.com/rideunno/",
    "Velduro": "https://www.instagram.com/veldurobikes/",
    "Whyte": "https://www.instagram.com/whytebikes/",
    "YT": "https://www.instagram.com/yt_industries/",
    "Apache": "Not on Instagram (Czech distributor only)",
    "Forbidden_Dread": "https://www.instagram.com/forbiddenbikecompany/",  # same brand
}

bikes = []

# ===== AMFLOW PX =====
bikes.append([
    "Amflow", "PX Carbon", "PX Carbon", "China/Global", "UPD",
    "M2S", 1500, 150,
    700, "Avinox FP700 integrated", "No",
    160, 150,
    "Carbon (Phantom Black)", "Mullet (29F/27.5R), 29 convertible",
    None, "M-size figure 20.6kg claimed; PX Pro 21.94kg measured",
    "FOX 36 Performance MY27, GRIP damper, 160mm",
    "FOX Float X Performance MY27, 210x55, 2-pos lever",
    "SRAM S1000 Eagle Transmission AXS 1x12, 38T, 10-52T",
    "Magura Gustav Pro 4-pot, 203mm Sensor rotors",
    "Amflow XMA-30 alloy 30mm, SAPIM E-Light, Maxxis tires",
    "Amflow Dropper, M/L 190mm, XL 210mm, XXL 230mm",
    6499, 7499, 7999, None, None,
    "https://cdn.amflowbikes.com/stormsend/uploads/986fcc03-73bc-4617-8d7b-e42c4f2ac5a8/default/xl.jpg",
    IG["Amflow"],
    "20.6kg claimed (Amflow). Full 1500W only with FP700 battery. SmoothShift via SRAM AXS hardwired to motor.",
    "https://www.amflowbikes.com/px-carbon/specs"
])
bikes.append([
    "Amflow", "PX Carbon", "PX Carbon Pro", "China/Global", "UPD",
    "M2S", 1500, 150,
    700, "Avinox FP700 integrated", "No",
    160, 150,
    "Carbon (Moonstone Gray)", "Mullet (29F/27.5R), 29 convertible",
    21.94, "Measured w/ pedals (EMTB Forums); 20.6kg M-size claimed by Amflow",
    "FOX 36 Factory MY27, GRIP X2 damper, HSC/LSC/HSR/LSR",
    "FOX Float X Factory MY27, 210x55, LSC & LSR adjust",
    "SRAM X0 Eagle Transmission AXS 1x12, 38T, 10-52T XS-1295",
    "Magura Gustav Pro 4-pot, 203mm Sensor rotors",
    "Amflow XMC-30 carbon 30mm, SAPIM E-Light",
    "Amflow Dropper, M/L 190mm, XL 210mm, XXL 230mm",
    8999, 9999, 10199, None, None,
    "https://cdn.amflowbikes.com/stormsend/uploads/70eaf868-16e2-43f5-99f4-92fedd5c159a/default/xl.jpg",
    IG["Amflow"],
    "Lightest available M2S bike at 21.94kg measured. Full 1500W with FP700. Apple Find My integration.",
    "https://www.amflowbikes.com/px-carbon/specs"
])

# ===== AMFLOW PR =====
bikes.append([
    "Amflow", "PR Carbon", "PR Carbon (M2)", "China/Global", "UPD",
    "M2", 1100, 125,
    800, "Avinox RS800 removable", "Yes",
    160, 150,
    "Carbon (Moss Green)", "Mullet (29F/27.5R), 29 convertible",
    None, "Frame 2.9kg claimed; complete bike not yet measured",
    "FOX AWL HD Sport MY27, RAIL 2.0 damper, 160mm",
    "FOX Float Rhythm MY27, custom tune, 210x55",
    "SRAM S1000 Eagle Transmission AXS 1x12, 38T, 10-52T",
    "Tektro TKD173 4-pot, 203mm rotors",
    "Amflow XMA-30 alloy 30mm, Maxxis Assegai/DHR II",
    "Amflow Dropper, M 190mm, L/XL 210mm, XXL 230mm",
    3999, 4499, 4999, None, None,
    "https://cdn.amflowbikes.com/stormsend/uploads/fa50fe12-d3a7-45a8-b5b4-88aadad51fda/default/xl.jpg",
    IG["Amflow"],
    "M2 motor (not M2S). Cheapest Avinox bike + only Amflow with removable battery on M2.",
    "https://www.amflowbikes.com/pr-carbon/specs"
])
bikes.append([
    "Amflow", "PR Carbon", "PR Carbon Pro", "China/Global", "UPD",
    "M2S", 1300, 150,
    800, "Avinox RS800 removable", "Yes",
    160, 150,
    "Carbon (Basalt Grey)", "Mullet (29F/27.5R), 29 convertible",
    24.2, "Measured Size L (E-MOUNTAINBIKE Magazine review)",
    "FOX 36 Performance MY27, GRIP damper, 160mm",
    "FOX Float X Performance MY27, 210x55, 2-pos lever",
    "SRAM S1000 Eagle Transmission AXS 1x12, 38T, 10-52T",
    "Magura Gustav Pro 4-pot, 203mm Sensor rotors",
    "Amflow XMA-30 alloy 30mm, Schwalbe Magic Mary/Albert Gravity Pro",
    "Amflow Dropper, M 190mm, L/XL 210mm, XXL 230mm",
    5399, 5899, 6799, None, 8699,
    "https://cdn.amflowbikes.com/stormsend/uploads/18f890dc-c284-49b6-9a27-6186ad2c9866/default/xl.jpg",
    IG["Amflow"],
    "M2S capped at 1300W due to RS800 battery. Apple Find My. RS600 600Wh option L/XL/XXL.",
    "https://www.amflowbikes.com/pr-carbon/specs"
])

# ===== ATHERTON S.170E =====
ath_photo = "https://athertonbikes.com/cdn/shop/files/S.170E_Studio_Drive_Side.jpg"
bikes.append([
    "Atherton", "S.170E", "Build 3 (entry)", "UK (Wales)", "EXIST",
    "M2S", 1500, 150,
    700, "Avinox FP700 integrated", "No",
    180, 170,
    "CNC alloy 7075 (Wales-made)", "Mullet (29F/27.5R)",
    None, "Not published",
    "RockShox Lyrik Select", "RockShox Super Deluxe Select",
    "SRAM Eagle 90 T-Type 1x12", "SRAM Maven Base, 200mm rotors",
    "DT Swiss/in-house alloy", "OneUp V3",
    6999, None, None, None, None,
    "https://athertonbikes.com (product page)", IG["Atherton"],
    "12 frame sizes, 1600-2000m climb claimed range. Full 1500W with FP700.",
    "https://athertonbikes.com"
])
bikes.append([
    "Atherton", "S.170E", "Build 2", "UK (Wales)", "EXIST",
    "M2S", 1500, 150, 700, "Avinox FP700 integrated", "No",
    180, 170, "CNC alloy 7075", "Mullet",
    None, "Not published",
    "RockShox Lyrik Ultimate", "RockShox Super Deluxe Ultimate",
    "SRAM GX Eagle T-Type AXS", "SRAM Maven Silver, 200mm",
    "DT Swiss alloy", "OneUp V3",
    7999, None, None, None, None,
    "https://athertonbikes.com (product page)", IG["Atherton"],
    "Mid-tier of the 3 builds.",
    "https://athertonbikes.com"
])
bikes.append([
    "Atherton", "S.170E", "Build 1 (top)", "UK (Wales)", "EXIST",
    "M2S", 1500, 150, 700, "Avinox FP700 integrated", "No",
    180, 170, "CNC alloy 7075", "Mullet",
    None, "Not published",
    "FOX 38 Factory GRIP X2", "FOX Float X Factory",
    "SRAM X0 Eagle T-Type AXS", "SRAM Maven Ultimate",
    "DT Swiss carbon", "OneUp V3",
    None, None, None, None, None,
    "https://athertonbikes.com (product page)", IG["Atherton"],
    "Top-spec build details limited. Pricing assumed >£8,500.",
    "https://athertonbikes.com"
])

# ===== BH iLYNX+ DL =====
bh_url = "https://www.bhbikes.com/en_GB/e-mtb/enduro/ilynx-plus-dl"
bikes.append([
    "BH", "iLynx+ DL", "Enduro 9.0 (Alloy entry)", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 170, "Hydroformed triple-butted alloy", "29 only",
    None, "Not published; Carbon 9.8 quoted at 22.4kg",
    "FOX 36", "FOX Rhythm",
    "Shimano Deore 12sp", "4-pot hydraulic",
    "Alloy", "Generic",
    None, 5399.90, None, None, None,
    bh_url, IG["BH"],
    "Cheapest M2S 170mm full-suspension. Note: 160mm fork on entry, 180mm on top builds.",
    bh_url
])
bikes.append([
    "BH", "iLynx+ DL", "Enduro 9.1 (Alloy)", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 170, "Hydroformed triple-butted alloy", "29 only",
    None, "Not published",
    "FOX 38", "FOX Float X",
    "SRAM mech T-Type", "4-pot, 200mm rotors",
    "DT Swiss H1700 hybrid", "Generic",
    None, None, None, None, None,
    bh_url, IG["BH"],
    "Notable: alloy 9.1 with FOX 38 = cheapest path to FOX 38 in iLynx range.",
    bh_url
])
bikes.append([
    "BH", "iLynx+ DL", "Carbon 9.5", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 170, "Ballistic Carbon front, alloy rear", "29 only",
    None, "22.4kg (top model)",
    "FOX 36", "FOX Float X",
    "Shimano XT mech", "Shimano XT 4-pot, 200mm",
    "DT Swiss H1700 hybrid", "Generic",
    None, None, None, None, None,
    bh_url, IG["BH"],
    "Carbon front + alloy rear hybrid frame.",
    bh_url
])
bikes.append([
    "BH", "iLynx+ DL", "Carbon 9.6", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 170, "Ballistic Carbon front, alloy rear", "29 only",
    None, "Not published",
    "FOX 38", "FOX Float X",
    "SRAM GX AXS T-Type", "SRAM Maven Silver, 200mm",
    "DT Swiss H1700", "Generic",
    None, None, None, None, None,
    bh_url, IG["BH"],
    "Mid-tier carbon hybrid.",
    bh_url
])
bikes.append([
    "BH", "iLynx+ DL", "Carbon 9.7", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 170, "Full Ballistic Carbon", "29 only",
    None, "Not published",
    "FOX 38 Factory GRIP X2", "FOX Float X Factory",
    "Shimano XT Di2", "Shimano XT 4-pot, 200mm",
    "DT Swiss carbon hybrid", "Generic",
    None, None, None, None, None,
    bh_url, IG["BH"],
    "Full carbon + electronic Shimano.",
    bh_url
])
bikes.append([
    "BH", "iLynx+ DL", "Carbon 9.8 (Top)", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 170, "Full Ballistic Carbon", "29 only",
    22.4, "Manufacturer claim (BH website footnote)",
    "FOX 38 Factory GRIP X2", "FOX Float X2 Factory",
    "Shimano XTR Di2", "Shimano XTR 4-pot, 200mm",
    "DT Swiss carbon hybrid", "Generic",
    None, 8999.90, None, None, None,
    bh_url, IG["BH"],
    "Top of range. 165kg max system weight.",
    bh_url
])

# ===== COMMENCAL META POWER SX =====
com_url = "https://www.commencalusa.com/meta-power-sx-c2x44181828"
bikes.append([
    "Commencal", "Meta Power SX Avinox", "Origin (entry)", "Andorra", "EXIST",
    "M2S", 1300, 150, 600, "Avinox 600Wh integrated", "No",
    170, 160, "Alloy (lifetime warranty)", "Mullet",
    24.0, "Manufacturer estimate Size L",
    "FOX 38 Performance", "FOX Float X Performance",
    "Shimano Deore 12sp", "Shimano 4-pot, 200mm",
    "Alloy", "Generic",
    None, 7900, None, None, None,
    com_url, IG["Commencal"],
    "Size S 600Wh fixed; M+ get 800Wh option. M2S with 800Wh capped at 1300W peak.",
    com_url
])
bikes.append([
    "Commencal", "Meta Power SX Avinox", "Race (top, est.)", "Andorra", "EXIST",
    "M2S", 1300, 150,
    800, "Avinox 800Wh integrated", "No",
    170, 160, "Alloy", "Mullet",
    24.0, "Estimate",
    "FOX 38 Factory", "FOX Float X Factory",
    "SRAM AXS T-Type", "SRAM Maven, 200mm",
    "DT Swiss", "OneUp/RockShox",
    None, 10950, None, None, None,
    com_url, IG["Commencal"],
    "5 build options €7,900-€10,950. VCS suspension.",
    com_url
])

# ===== CRESTLINE =====
cl_url = "https://crestlinebikes.com/current-bikes/"
bikes.append([
    "Crestline", "RS 181.2", "(single build est.)", "USA", "NEW",
    "M2S", 1500, 150, 800, "Avinox 800Wh integrated", "No",
    180, 181, "Carbon (USA hand-built)", "Mullet",
    None, "Not published",
    "FOX 38 Factory", "FOX Float X2 Factory",
    "SRAM AXS T-Type", "SRAM Maven Ultimate",
    "DT Swiss", "OneUp",
    None, None, None, None, None,
    cl_url, IG["Crestline"],
    "USA-made boutique. Aaron Gwin co-owner. Limited public spec.",
    cl_url
])

# ===== CRUSSIS =====
cr_url = "https://www.crussis.com"
bikes.append([
    "Crussis", "e-Hard 1.11", "(entry hardtail)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 600, "Avinox 600Wh integrated", "No",
    130, 0, "Alloy", "29",
    None, "Not published",
    "FOX AWL 34", "n/a (hardtail)",
    "Shimano Deore mech", "SRAM DB8 Stealth 4-pot, 200mm",
    "Crussis alloy", "Generic",
    None, 3590, None, None, None,
    cr_url + "/avinox-motor-m2s-crussis-en.html", IG["Crussis"],
    "Cheapest Avinox bike anywhere. Hardtail.",
    cr_url + "/avinox-motor-m2s-crussis-en.html"
])
bikes.append([
    "Crussis", "e-Hard 11.11 PRO", "(160mm hardtail)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 0, "Alloy", "29",
    None, "Not published",
    "FOX AWL HD 36 GRIP X", "n/a",
    "Shimano XT", "SRAM DB8 Stealth, 200mm",
    "Crussis alloy", "Generic",
    None, 4490, None, None, None,
    cr_url + "/avinox-motor-m2s-crussis-en.html", IG["Crussis"],
    "Long-travel hardtail. Surprising spec for the money.",
    cr_url + "/avinox-motor-m2s-crussis-en.html"
])
bikes.append([
    "Crussis", "e-Full 11.11", "(600Wh)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 600, "Avinox 600Wh integrated", "No",
    160, 150, "Alloy (Czech-designed)", "29",
    None, "Not published",
    "FOX 36 Performance GRIP", "FOX Float Performance",
    "Shimano XT mech", "SRAM Maven Base 4-pot, 200mm",
    "Crussis alloy + Maxxis Assegai/DHR II", "Generic",
    None, 5290, None, None, None,
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-11-11-600-wh-m-2026.html",
    IG["Crussis"],
    "Entry full-sus alloy with 600Wh.",
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-11-11-600-wh-m-2026.html"
])
bikes.append([
    "Crussis", "e-Full 11.11", "(800Wh)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Alloy", "29",
    None, "Not published",
    "FOX 36 Performance GRIP", "FOX Float Performance",
    "Shimano XT mech", "SRAM Maven Base 4-pot, 200mm",
    "Crussis alloy", "Generic",
    None, 5690, None, None, None,
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-11-11-800-wh-m-2026.html",
    IG["Crussis"],
    "Same as 600Wh but with bigger battery.",
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-11-11-800-wh-m-2026.html"
])
bikes.append([
    "Crussis", "e-Full 12.11", "(800Wh)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Alloy", "29",
    None, "Not published",
    "FOX Float 36 Factory GRIP X2", "FOX Float X",
    "SRAM mech AXS path", "SRAM Maven Silver, 200mm",
    "Crussis alloy + Maxxis Assegai/DHR II 2.5", "FOX Transfer",
    None, 8690, None, None, None,
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-12-11-800-wh-xl-2026.html",
    IG["Crussis"],
    "Mid-trim full-sus alloy. Full FOX Factory front.",
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-12-11-800-wh-xl-2026.html"
])
bikes.append([
    "Crussis", "e-Full 12.11 PRO", "(800Wh)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Alloy", "29",
    None, "Not published",
    "FOX 38 Factory GRIP X2", "FOX Float X Factory",
    "SRAM AXS T-Type", "SRAM Maven Silver, 200mm",
    "DT Swiss + Maxxis", "FOX Transfer",
    None, 8990, None, None, None,
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-12-11-pro-800-wh-xl-2026.html",
    IG["Crussis"],
    "Premium alloy build.",
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-12-11-pro-800-wh-xl-2026.html"
])
bikes.append([
    "Crussis", "e-Full 12.11 PRO X", "(top spec carbon)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon (bespoke, not open-mold)", "29",
    None, "Not published",
    "FOX Podium AM (upside-down) GRIP X2", "FOX Float X Live Valve Neo",
    "SRAM AXS T-Type", "SRAM Maven Ultimate, 200mm",
    "DT Swiss + Maxxis Assegai/DHR II", "FOX Transfer Neo",
    None, 11990, None, None, None,
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-12-11-pro-x-800-wh-m-2026.html",
    IG["Crussis"],
    "Top Crussis. FOX Live Valve adaptive.",
    cr_url + "/eshop-crussis-full-suspension-mountain-e-bike-e-full-12-11-pro-x-800-wh-m-2026.html"
])

# ===== FORBIDDEN DRUID E =====
fb_url = "https://forbiddenbike.com/bikes/druid-e/"
fb_pinkbike = "https://www.pinkbike.com/news/forbidden-druid-e-gets-avinox-m2s-and-m2-upgrades-for-2026.html"
for tier_data in [
    ("Tier 4 Sandstorm", "M2", 1100, 125, "RockShox Lyrik Base", "RockShox Super Deluxe Base",
     "SRAM Eagle 70 T-Type", "SRAM DB4", "Crankbrothers Synthesis Alloy",
     6599, 7499, 7499, 9699,
     6899, 7799, 7799, 9999,
     22.0, 22.4),
    ("Tier 3 EVOO", "M2", 1100, 125, "RockShox Lyrik Select+", "RockShox Super Deluxe Select+",
     "SRAM Eagle 90 T-Type", "SRAM Maven Base", "Crankbrothers Synthesis Alloy",
     7499, 8699, 8599, 10999,
     7799, 8999, 8899, 11299,
     22.6, 23.4),
    ("Tier 2 Purple Haze", "M2S", 1300, 150, "FOX 36 Factory", "FOX Float X Factory",
     "SRAM GX T-Type AXS", "SRAM Maven Silver", "Crankbrothers Synthesis Alloy 2.0",
     8899, 10199, 10299, 13199,
     9199, 10499, 10599, 13499,
     22.4, 23.3),
    ("Tier 1 Vitalogy", "M2S", 1300, 150, "FOX Podium Factory", "FOX Float X Factory",
     "SRAM X0 T-Type AXS", "SRAM Maven Ultimate", "Crankbrothers Synthesis Carbon",
     10799, 12599, 12699, 16199,
     11099, 12899, 12999, 16499,
     22.3, 23.2),
]:
    (build_name, motor, peak_w, peak_nm, fork, shock, drive, brake, wheels,
     gbp_600, eur_600, usd_600, cad_600,
     gbp_800, eur_800, usd_800, cad_800,
     wt_600, wt_800) = tier_data
    bikes.append([
        "Forbidden", "Druid E", f"{build_name} (600Wh)", "Canada", "NEW",
        motor, peak_w, peak_nm,
        600, "Avinox RS600 removable", "Yes",
        160, 150, "Carbon w/ Trifecta high-pivot", "Mullet",
        wt_600, "Pinkbike press release weight",
        fork, shock, drive, brake, wheels, "OneUp Dropper",
        gbp_600, eur_600, usd_600, cad_600, None,
        fb_url, IG["Forbidden"],
        "OneRide proportional sizing. Trifecta high-pivot suspension. Removable battery.",
        fb_pinkbike
    ])
    bikes.append([
        "Forbidden", "Druid E", f"{build_name} (800Wh)", "Canada", "NEW",
        motor, peak_w, peak_nm,
        800, "Avinox RS800 removable", "Yes",
        160, 150, "Carbon w/ Trifecta high-pivot", "Mullet",
        wt_800, "Pinkbike press release weight",
        fork, shock, drive, brake, wheels, "OneUp Dropper",
        gbp_800, eur_800, usd_800, cad_800, None,
        fb_url, IG["Forbidden"],
        "Same build as 600Wh + upgraded battery (~+1kg, ~+£300).",
        fb_pinkbike
    ])

# Forbidden Dreadnought E
bikes.append([
    "Forbidden", "Dreadnought E", "(pre-order)", "Canada", "NEW",
    "M2S", 1500, 150, 800, "Avinox RS800 removable (likely)", "Yes",
    180, 170, "Carbon w/ Trifecta V3 high-pivot", "Mullet",
    None, "Not published",
    "FOX Podium / RockShox ZEB", "FOX Float X2 / RS Vivid",
    "SRAM AXS", "SRAM Maven Silver+",
    "DT Swiss / Crankbrothers", "OneUp",
    None, None, None, None, None,
    "https://forbiddenbike.com/bikes/dreadnought-e/", IG["Forbidden"],
    "PRE-ORDER. New high-pivot enduro. M2/M2S, both batteries available.",
    "https://forbiddenbike.com/bikes/dreadnought-e/"
])

# ===== FORESTAL =====
forestal_url = "https://forestal.com/en/products/siryon"
bikes.append([
    "Forestal", "e-Siryon V2", "Halō", "Andorra", "NEW",
    "M2S", 1500, 150, 800, "Avinox FP700? 800Wh integrated", "No",
    170, 174, "Carbon (Alpha Box) Twin Levity", "29 only",
    None, "21.5kg claimed for Diōde build (E-MOUNTAINBIKE)",
    "RockShox ZEB Select",
    "RockShox Vivid Select Air",
    "SRAM S1000 Eagle AXS Transmission",
    "SRAM Maven, 200/200mm",
    "Crankbrothers Synthesis Alloy 29 + Schwalbe Albert Gravity 29x2.5",
    "OneUp V3 31.6mm",
    None, 7500, None, None, None,
    forestal_url, IG["Forestal"],
    "Replaces M1-style EonDrive. 174mm rear travel. Twin Levity progressive 3.65→2.4.",
    forestal_url
])
bikes.append([
    "Forestal", "e-Siryon V2", "Diōde (top)", "Andorra", "NEW",
    "M2S", 1500, 150, 800, "Avinox 800Wh integrated", "No",
    170, 174, "Carbon (Alpha Box)", "29 only",
    21.5, "Manufacturer/E-MOUNTAINBIKE",
    "FOX Podium Factory (USD)",
    "FOX Float Factory X2",
    "SRAM AXS Transmission",
    "SRAM Maven Ultimate, 200/200mm",
    "Crankbrothers Synthesis Alloy",
    "FOX Transfer NEO Factory 31.6mm",
    None, 9599.99, None, None, None,
    forestal_url, IG["Forestal"],
    "Top spec. Lightest M2S 170mm bike at 21.5kg.",
    forestal_url
])

# ===== LEE COUGAN FLÖ =====
lc_url = "https://leecougan.com/en/bikes/e-bikes/flo"
bikes.append([
    "Lee Cougan", "Flö", "Carbon (entry)", "Italy", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon (2.5kg M-frame claimed)", "Mullet (29F/27.5R), 29 flip",
    None, "21.5kg/22kg estimated; not officially published",
    "RockShox ZEB Select",
    "RockShox Super Deluxe Select",
    "SRAM Eagle 90 T-Type",
    "Magura MT5 4-pot",
    "Ursus Pura M Alu + Continental Kryptotal Enduro",
    "Lee Cougan dropper, 150mm S, 170mm M/L",
    None, None, None, None, None,
    "https://s2api.it/wp-content/uploads/2026/04/Flo_Stonewave_Carbon_.webp",
    IG["Lee Cougan"],
    "Italian, lightest frame in category claim. Co-developed RockShox shock tune.",
    lc_url
])
bikes.append([
    "Lee Cougan", "Flö", "Carbon Pro", "Italy", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon (2.5kg M-frame)", "Mullet, 29 flip",
    20.5, "Manufacturer claim Carbon Pro Mullet",
    "RockShox ZEB Ultimate",
    "RockShox Super Deluxe Ultimate (custom tune)",
    "SRAM GX Eagle Transmission AXS",
    "Magura Gustav Pro 4-pot",
    "Ursus + Continental Kryptotal",
    "Lee Cougan dropper",
    None, 8699, None, None, None,
    "https://s2api.it/wp-content/uploads/2026/04/Flo_Pure-Black_Carbon-Pro_-2.webp",
    IG["Lee Cougan"],
    "Class-leading sub-21kg M2S 160mm. AXS draws power from main motor battery.",
    lc_url
])

# ===== MAXX FAB.4 ELA =====
maxx_url = "https://www.maxx.de/en/bikes/e-mtb/fab4_ela/"
bikes.append([
    "MAXX", "FAB.4 ELA", "Configurable base", "Germany (Rosenheim)", "NEW",
    "M2S", 1500, 150, 600, "Avinox RS600 removable", "Yes",
    170, 160, "Carbon (high-mod, Maxx-developed)", "29",
    None, "Not officially published",
    "Configurable (typ. FOX 38 / RockShox ZEB)",
    "Configurable (typ. FOX Float X / RS SD)",
    "Configurable (Shimano XT / SRAM T-Type)",
    "Configurable (Magura/SRAM/Shimano)",
    "Configurable", "Configurable",
    None, 6699, None, None, None,
    maxx_url, IG["MAXX"],
    "Configurator-built. 800Wh battery +€199. CUSTOM PAINT WORKSHOP - 50 standard colors or any code.",
    maxx_url
])
bikes.append([
    "MAXX", "FAB.4 ELA", "Configurable + 800Wh", "Germany (Rosenheim)", "NEW",
    "M2S", 1300, 150, 800, "Avinox RS800 removable", "Yes",
    170, 160, "Carbon", "29",
    None, "Not published",
    "Configurable", "Configurable", "Configurable", "Configurable", "Configurable", "Configurable",
    None, 6898, None, None, None,
    maxx_url, IG["MAXX"],
    "Same frame, 800Wh option (+€199 over base). 1300W peak with RS800.",
    maxx_url
])

# ===== MEGAMO REASON =====
me_url = "https://www.megamo.com/en/e-bike/e-full-suspension/reason"
bikes.append([
    "Megamo", "Reason", "AL 07 (entry alloy)", "Spain", "UPD",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Hydroformed alloy", "29 only",
    None, "AL ~23kg per Ribble Valley spec",
    "FOX AWL HD 36",
    "FOX Rhythm",
    "Shimano Deore 12sp",
    "Shimano XT 4-pot",
    "Megamo alloy + reinforced tires",
    "Megamo dropper",
    4999, 4999, None, None, None,
    me_url, IG["Megamo"],
    "Cheapest Megamo M2S full-sus.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "AL 05", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Alloy", "29 only",
    None, "~23kg estimate",
    "FOX 38 Performance E-Optimised",
    "FOX Float X Performance",
    "SRAM 90 T-Type",
    "Shimano XT 4-pot",
    "Megamo alloy",
    "Megamo dropper",
    None, 5999, None, None, None,
    me_url, IG["Megamo"],
    "Bang for buck pick. FOX 38 + XT.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "AL 03", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Alloy", "29",
    None, "~23kg",
    "FOX 38 Factory Kashima", "FOX Float X Factory",
    "SRAM mech T-Type", "Shimano XT 4-pot",
    "Carbon bars + alloy wheels", "FOX Transfer Kashima 120/150/180mm",
    None, 6499, None, None, None,
    me_url, IG["Megamo"],
    "Top alloy mechanical. Strong value.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "AL 03 AXS", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Alloy", "29",
    None, "~23kg",
    "FOX 38 Factory", "FOX Float X Factory",
    "SRAM AXS T-Type", "Shimano XT 4-pot",
    "Carbon bars", "FOX Transfer Kashima",
    None, 7499, None, None, None,
    me_url, IG["Megamo"],
    "Top alloy electronic. Same spec as CRB 03 AXS for €1,000 less.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "CRB 07 (entry carbon)", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon", "29",
    None, "Not published",
    "FOX AWL HD", "FOX Rhythm",
    "Shimano XT M8100 12sp", "Shimano MT520 4-pot",
    "Megamo own brand", "Megamo own",
    None, 5999, None, None, None,
    me_url, IG["Megamo"],
    "Entry carbon. Cost-cut spec.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "CRB 05", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon", "29",
    None, "Not published",
    "FOX 36 Performance", "FOX Float Performance",
    "Shimano 12sp", "Shimano XT 4-pot",
    "Megamo carbon", "Megamo",
    None, 6999, None, None, None,
    me_url, IG["Megamo"],
    "Mid carbon. Performance suspension.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "CRB 03", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon", "29",
    None, "Not published",
    "FOX 38 Factory", "FOX Float X Factory",
    "SRAM mech T-Type", "Shimano XT 4-pot",
    "DT Swiss/Megamo carbon", "FOX Transfer",
    None, 7999, None, None, None,
    me_url, IG["Megamo"],
    "Carbon mechanical, high-end suspension.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "CRB 03 AXS", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon", "29",
    22.2, "MBR review",
    "FOX 38 Factory", "FOX Float X Factory",
    "SRAM AXS T-Type", "Shimano XT 4-pot",
    "DT Swiss + Maxxis Doubledown", "FOX Transfer",
    8499, 8499, None, None, None,
    me_url, IG["Megamo"],
    "Most popular spec. AXS electronic.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "CRB 02", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon", "29",
    None, "Not published",
    "RockShox ZEB Ultimate", "RockShox Vivid Ultimate",
    "SRAM XX/S1000 hybrid T-Type", "SRAM Maven Ultimate",
    "DT Swiss H 1900 alloy", "Generic",
    None, 8999, None, None, None,
    me_url, IG["Megamo"],
    "RockShox-equipped premium.",
    me_url
])
bikes.append([
    "Megamo", "Reason", "CRB 01 (top)", "Spain", "UPD",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 160, "Carbon (Garnet UD finish)", "29",
    22.04, "Measured Size M (E-MOUNTAINBIKE)",
    "FOX 38 Factory Kashima", "FOX Float X Factory",
    "SRAM XX AXS T-Type", "Shimano XT 4-pot",
    "DT Swiss HXC 1501 carbon + Maxxis Assegai/DHR II Doubledown", "FOX Transfer Factory 175mm",
    None, 10999, None, None, None,
    me_url, IG["Megamo"],
    "Top Megamo. 175mm dropper criticized as short.",
    me_url
])
bikes.append([
    "Megamo", "Reason AIR", "(range €4,999-€11,999)", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    140, 140, "Carbon or Alloy", "29",
    None, "~21-22kg lighter than Reason",
    "Various", "Various", "Various", "Various", "Various", "Various",
    None, 4999, None, None, None,
    me_url, IG["Megamo"],
    "Trail/all-mountain sister model. 6 build variants. Lighter than Reason.",
    me_url
])

# ===== MMR LYTH =====
mmr_url = "https://www.mmr.com"
bikes.append([
    "MMR", "Lyth", "(single build at launch)", "Spain", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 0, "Mid-modulus carbon", "Mullet (flip-chip)",
    None, "Not published",
    "FOX Float 36 Rhythm 160mm",
    "FOX Float X Rhythm 185x55",
    "Shimano XT M8200 12sp",
    "Shimano Deore 4-pot",
    "Generic", "Generic",
    5499, None, None, None, None,
    mmr_url, IG["MMR"],
    "PRE-ORDER UK May 2026. Spanish full-carbon at competitive price.",
    "https://www.emtbforums.com/threads/please-provide-updated-list-of-all-bikes-that-are-avaliable-or-scheduled-to-be-released-in-6-months-that-have-avinox-m2s-motor-full-29-wheel-option.46432"
])

# ===== MONDRAKER ZENDIT =====
md_url = "https://www.mondraker.com/en/zendit"
bikes.append([
    "Mondraker", "Zendit", "RR (entry)", "Spain", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    170, 165, "Carbon (Crafty platform)", "Mullet",
    None, "Not published; RR S 23.24kg M/L",
    "FOX 38 Factory", "FOX Float X Factory",
    "SRAM mech AXS T-Type", "SRAM Maven",
    "DT Swiss", "OneUp",
    7399, 8499, None, None, None,
    md_url, IG["Mondraker"],
    "Successor to Crafty. 165mm rear travel.",
    md_url
])
bikes.append([
    "Mondraker", "Zendit", "RR S (top)", "Spain", "UPD",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    170, 165, "Carbon", "Mullet",
    23.24, "Measured M/L (E-MOUNTAINBIKE)",
    "FOX Podium Factory upside-down", "FOX Float X Factory",
    "SRAM AXS T-Type", "SRAM Maven Ultimate",
    "DT Swiss carbon", "OneUp",
    None, 10499, None, None, None,
    md_url, IG["Mondraker"],
    "Top spec with Podium upside-down fork.",
    md_url
])

# ===== ORANGE PHASE EVO =====
or_url = "https://orangebikes.com"
bikes.append([
    "Orange", "Phase Evo Avinox", "(top spec)", "UK", "EXIST",
    "M1", 1000, 120, 800, "Avinox 800Wh integrated", "No",
    160, 155, "Hand-built UK alloy (folded plate)", "Mullet",
    19.5, "Manufacturer claim",
    "FOX 36 Performance / Factory", "FOX Float X",
    "SRAM AXS / Shimano", "SRAM/Shimano 4-pot",
    "Hope/DT Swiss", "Generic",
    None, None, None, None, None,
    or_url, IG["Orange"],
    "STILL M1 motor. Lightest full-power Avinox bike at 19.5kg. Hand-built UK.",
    or_url
])

# ===== PIVOT SHUTTLE AMP'D =====
pv_url = "https://pivotcycles.com/bike/shuttle-ampd/"
bikes.append([
    "Pivot", "Shuttle AMP'd", "Ride GX Eagle Transmission", "USA", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Hollow Core Carbon (size-tuned layup)", "Mullet (flip to 29)",
    None, "Team XX measured ~21.5kg L; Ride GX heavier",
    "FOX 38 Performance, GRIP",
    "FOX Float X Performance",
    "SRAM GX Eagle Transmission, Praxis Alloy 155mm crank, 34T",
    "SRAM Maven Base 4-pot, 200mm Centerline",
    "DT Swiss E532 alloy + Continental Kryptotal Enduro",
    "OneUp Dropper V3 150-240mm size-specific",
    None, 9699, 9499, None, 13999,
    pv_url, IG["Pivot"],
    "Entry 4-amp charger (no fast charge). Class 1 default; toggle to Class 3 in app.",
    pv_url
])
bikes.append([
    "Pivot", "Shuttle AMP'd", "Pro X0 Eagle Transmission", "USA", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Hollow Core Carbon", "Mullet",
    21.5, "Manufacturer claim Size L",
    "RockShox ZEB Ultimate Charger 3.2",
    "RockShox Super Deluxe Ultimate",
    "SRAM X0 Eagle Transmission AXS, Praxis Alloy 155mm",
    "SRAM Maven Silver 4-pot, 200mm HS2 rotors",
    "DT Swiss Hybrid HX1501 MX + Conti Kryptotal Enduro",
    "OneUp V3 150-240mm size-specific",
    None, 11999, 11999, None, None,
    pv_url, IG["Pivot"],
    "Includes 12A fast charger. Phoenix Team carbon bar.",
    pv_url
])
bikes.append([
    "Pivot", "Shuttle AMP'd", "Team XX Eagle Transmission", "USA", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Hollow Core Carbon", "Mullet",
    21.5, "Manufacturer Size L; VitalMTB measured 21.97kg",
    "FOX 38 Factory, GRIP X2",
    "FOX Float X Factory",
    "SRAM XX Eagle Transmission AXS, Praxis Carbon eCranks 155mm 34T",
    "SRAM Maven Ultimate 4-pot, 200mm HS2",
    "DT Swiss Hybrid HXC1501 carbon + Conti Kryptotal Enduro",
    "RockShox Reverb V2 200mm L",
    None, 13999, 14499, None, None,
    pv_url, IG["Pivot"],
    "Top spec. Reverb V2 sacrifices ~15mm drop vs OneUp.",
    pv_url
])

# ===== RAYMON =====
ra_url = "https://raymon-bikes.com"
bikes.append([
    "Raymon", "Tarok", "Pro (M2)", "Germany", "EXIST",
    "M2", 1100, 125, 700, "Avinox 700Wh integrated", "No",
    160, 150, "Carbon front / Alloy rear", "Mullet",
    None, "~22kg estimate",
    "FOX 36 Performance", "FOX Float Performance",
    "SRAM mech", "SRAM 4-pot",
    "Generic", "Generic",
    None, 4999, None, None, None,
    ra_url, IG["Raymon"],
    "Entry M2 Tarok.",
    ra_url
])
bikes.append([
    "Raymon", "Tarok", "Ultra (M2S)", "Germany", "UPD",
    "M2S", 1500, 150, 700, "Avinox FP700 integrated", "No",
    160, 150, "Carbon", "Mullet",
    22.0, "Manufacturer claim Size L",
    "FOX 38 Factory", "FOX Float X Factory",
    "SRAM AXS T-Type", "SRAM Maven Silver",
    "DT Swiss alloy", "OneUp",
    None, 7499, None, None, None,
    ra_url, IG["Raymon"],
    "M2S top spec with FP700 = full 1500W.",
    ra_url
])

# ===== ROTWILD R.EX =====
rw_rex_url = "https://www.rotwild.com/en/r.ex-core/20386"
bikes.append([
    "Rotwild", "R.EX", "Core (M1)", "Germany", "EXIST",
    "M1", 1000, 120, 864, "Custom Rotwild IPU 900 (864Wh) removable", "Yes",
    160, 150, "Carbon (Mid-High Pivot)", "Mullet (29F/27.5R)",
    22.4, "Manufacturer claim",
    "FOX 36 Performance", "FOX Performance",
    "Shimano XT mech 12sp", "Shimano XT 4-pot",
    "Crankbrothers Synthesis Enduro Alloy", "Eightpins NGS 3.0",
    None, 8990, None, None, None,
    rw_rex_url, IG["Rotwild"],
    "Lightest battery: 864Wh @ 3.58kg (200Wh/kg). M1 motor still here.",
    rw_rex_url
])
bikes.append([
    "Rotwild", "R.EX", "Pro (M1)", "Germany", "EXIST",
    "M1", 1000, 120, 864, "Custom Rotwild IPU 900 removable", "Yes",
    160, 150, "Carbon", "Mullet",
    22.1, "Manufacturer claim",
    "RockShox Lyrik Select+", "RockShox Super Deluxe Select+",
    "SRAM GX AXS T-Type", "SRAM Maven Base",
    "Crankbrothers Synthesis Alloy", "Eightpins NGS 3.0",
    None, 9990, None, None, None,
    rw_rex_url, IG["Rotwild"],
    "Mid-tier R.EX with M1.",
    rw_rex_url
])
bikes.append([
    "Rotwild", "R.EX", "Ultra (M1)", "Germany", "EXIST",
    "M1", 1000, 120, 864, "Custom Rotwild IPU 900 removable", "Yes",
    160, 150, "Carbon", "Mullet",
    23.2, "Measured Size L (E-MOUNTAINBIKE)",
    "FOX 36 Factory GRIP X2", "FOX Float X Factory",
    "SRAM XX AXS T-Type", "SRAM Maven Ultimate",
    "Crankbrothers Synthesis Carbon", "Eightpins NGS 3.0",
    None, 12490, None, None, None,
    rw_rex_url, IG["Rotwild"],
    "Top R.EX. 864Wh removable battery — largest in market.",
    rw_rex_url
])

# ===== ROTWILD R.EXC =====
rw_rexc_pro_url = "https://www.rotwild.com/en/r.exc-pro/20395"
rw_rexc_ultra_url = "https://www.rotwild.com/en/r.exc-ultra/20399"
bikes.append([
    "Rotwild", "R.EXC", "Pro (M2S)", "Germany", "NEW",
    "M2S", 1500, 150, 864, "Custom Rotwild IPU 900 removable", "Yes",
    170, 160, "Carbon (Elevated Box, Mid-High Pivot)", "Mullet",
    None, "Pro weight not published; Ultra at 21.7kg L",
    "FOX 38 Performance", "FOX Float X Performance",
    "SRAM mech T-Type", "Magura/SRAM 4-pot",
    "DT Swiss alloy", "Eightpins NGS 3.0 up to 225mm",
    None, 10990, None, None, None,
    rw_rexc_pro_url, IG["Rotwild"],
    "RACE-FOCUSED. Rear travel adjustable 145/150/160mm via shock mount.",
    rw_rexc_pro_url
])
bikes.append([
    "Rotwild", "R.EXC", "Ultra (M2S)", "Germany", "NEW",
    "M2S", 1500, 150, 864, "Custom Rotwild IPU 900 removable", "Yes",
    170, 160, "Carbon", "Mullet",
    21.7, "Manufacturer claim Size L",
    "FOX 38 Factory GRIP X2", "FOX Float X Factory",
    "SRAM AXS T-Type", "SRAM Maven Ultimate",
    "DT Swiss carbon hybrid", "Eightpins NGS 3.0",
    None, 14990, None, None, None,
    rw_rexc_ultra_url, IG["Rotwild"],
    "Top R.EXC. 864Wh removable + M2S = unique combo.",
    rw_rexc_ultra_url
])

# ===== STEPPENWOLF =====
sw_url = "https://steppenwolf-bikes.com"
bikes.append([
    "Steppenwolf", "Tundra", "9.0 (entry M2S)", "Germany", "NEW",
    "M2S", 1300, 130, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Alloy or Carbon (uncertain)", "29 or Mullet",
    None, "Not published",
    "FOX/RockShox", "FOX/RockShox", "Shimano/SRAM mech", "4-pot", "Generic", "Generic",
    None, None, None, None, None,
    sw_url, IG["Steppenwolf"],
    "PRE-ORDER, Autumn 2026. Brand returns post-insolvency.",
    sw_url
])
bikes.append([
    "Steppenwolf", "Tundra", "10.0", "Germany", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    170, 160, "Carbon", "29",
    None, "Not published",
    "FOX 38 Performance", "FOX Float X", "SRAM AXS", "SRAM Maven", "DT Swiss", "Generic",
    None, None, None, None, None,
    sw_url, IG["Steppenwolf"],
    "PRE-ORDER, Autumn 2026.",
    sw_url
])
bikes.append([
    "Steppenwolf", "Tundra", "11.0 (top)", "Germany", "NEW",
    "M2S", 1500, 150, 800, "Avinox 800Wh integrated", "No",
    170, 170, "Carbon", "29",
    None, "Not published",
    "FOX 38 Factory", "FOX Float X2", "SRAM X0 AXS T-Type", "SRAM Maven Ultimate", "DT Swiss carbon", "Generic",
    None, None, None, None, None,
    sw_url, IG["Steppenwolf"],
    "PRE-ORDER. Top spec.",
    sw_url
])

# ===== TEEWING =====
tw_url = "https://teewingbikes.com/collections/electric-bikes"
bikes.append([
    "Teewing", "Turbo Force", "Pro", "China/EU", "UPD",
    "M2S", 1300, 130, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon", "Mullet",
    None, "~22-23kg estimate",
    "FOX/RockShox Performance", "FOX Float", "SRAM AXS", "SRAM/Magura 4-pot", "Generic", "Generic",
    None, 8999, None, None, None,
    "https://teewingbikes.com/collections/electric-bikes/products/turbo-force-pro", IG["Teewing"],
    "Top Turbo Force build.",
    "https://teewingbikes.com/collections/electric-bikes/products/turbo-force-pro"
])
bikes.append([
    "Teewing", "Turbo Force", "XT (entry)", "China/EU", "NEW",
    "M2S", 1300, 130, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon", "Mullet",
    None, "~22-23kg estimate",
    "FOX/RockShox Performance", "FOX Float", "SRAM AXS", "SRAM/Magura 4-pot", "Generic", "Generic",
    None, 5899, None, None, None,
    "https://teewingbikes.com/collections/electric-bikes/products/turbo-force-xt", IG["Teewing"],
    "Entry Turbo Force build.",
    "https://teewingbikes.com/collections/electric-bikes/products/turbo-force-xt"
])
bikes.append([
    "Teewing", "Flux One", "A (entry)", "China/EU", "UPD",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 178, "CAT 5 Carbon, high-pivot", "29 / Mullet flip",
    None, "Not published",
    "FOX 38", "FOX Float X2", "SRAM mech AXS", "SRAM Maven Silver", "DT Swiss", "Generic",
    None, 6899, None, None, None,
    "https://teewingbikes.com/collections/electric-bikes/products/flux-one-a", IG["Teewing"],
    "Longest travel of any Avinox bike. High-pivot.",
    "https://teewingbikes.com/collections/electric-bikes/products/flux-one-a"
])
bikes.append([
    "Teewing", "Flux One", "Pro", "China/EU", "UPD",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 178, "CAT 5 Carbon, high-pivot", "29 / Mullet",
    None, "Not published",
    "FOX Podium Factory", "FOX Float X2 Factory", "SRAM AXS X0", "SRAM Maven Ultimate", "DT Swiss carbon", "Generic",
    None, 8999, None, None, None,
    "https://teewingbikes.com/collections/electric-bikes/products/flux-one-pro", IG["Teewing"],
    "Top high-pivot Teewing.",
    "https://teewingbikes.com/collections/electric-bikes/products/flux-one-pro"
])

# ===== THÖMUS =====
th_url = "https://thoemus.ch/en/oberrider/"
bikes.append([
    "Thömus", "Oberrider", "Trail (configurable)", "Switzerland", "NEW",
    "M2S", 1500, 150, 800, "Avinox 800Wh integrated", "No",
    150, 150, "Carbon (Swiss)", "29",
    19.9, "Manufacturer claim, lightest config",
    "Configurable", "Configurable", "Configurable", "Configurable", "Configurable", "Configurable",
    None, 5800, None, None, None,
    th_url, IG["Thömus"],
    "5,490 CHF base. Sub-20kg in lightest configurator build.",
    th_url
])
bikes.append([
    "Thömus", "Oberrider", "Enduro (configurable)", "Switzerland", "NEW",
    "M2S", 1500, 150, 800, "Avinox 800Wh integrated", "No",
    170, 170, "Carbon", "29",
    None, "~21kg estimate",
    "Configurable", "Configurable", "Configurable", "Configurable", "Configurable", "Configurable",
    None, 6500, None, None, None,
    th_url, IG["Thömus"],
    "Long-travel sibling. Higher base CHF.",
    th_url
])

# ===== UNNO MITH =====
un_url = "https://unno.com/mith/"
bikes.append([
    "Unno", "Mith", "(updated M2S)", "Spain", "UPD",
    "M2S", 1500, 150, 800, "Avinox 800Wh integrated", "No",
    170, 160, "Carbon (Boutique Spanish)", "Mullet",
    21.5, "Manufacturer claim",
    "FOX Podium / RockShox ZEB Ultimate", "FOX Float X / RS Vivid",
    "SRAM AXS T-Type", "SRAM Maven Ultimate", "DT Swiss carbon", "OneUp",
    None, 13500, None, None, None,
    un_url, IG["Unno"],
    "Boutique Spanish. Updated for M2S. 21.5kg claimed.",
    un_url
])

# ===== VELDURO =====
vd_url = "https://www.velduro.com"
bikes.append([
    "Velduro", "Rogue R", "(complete bike)", "New Zealand", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 172, "Carbon CAT 5 (i-Track licensed)", "Mullet (flip to 29)",
    25.4, "Measured Size L w/ pedals (Pinkbike, M1 version)",
    "FOX Float X2 Factory or Podium",
    "FOX Float X / X2 Factory",
    "SRAM mech AXS T-Type",
    "SRAM Maven Silver 4-pot, 200mm",
    "DT Swiss + Maxxis Doubledown",
    "OneUp/RockShox",
    None, None, None, 14300, None,
    vd_url, IG["Velduro"],
    "NZ brand. M2S frameset from $7,200 CAD; complete to $14,300 CAD. Adjustable 165-172mm rear travel via flip-chip.",
    "https://www.pinkbike.com/news/first-ride-the-avinox-powered-velduro-rogue-r-is-dh-bike-in-an-enduro-bikes-clothing.html"
])

# ===== WHYTE =====
wh_url_rs = "https://whytebikes.com/products/karve-evo-rs-trail-enduro-electric-mountain-bike"
wh_url_rsx = "https://whytebikes.com/products/karve-evo-rsx-trail-enduro-electric-mountain-bike"
bikes.append([
    "Whyte", "Karve EVO", "RS (entry)", "UK", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 180, "Uni-directional carbon front + 6061 alloy rear", "Mullet (29F/27.5R)",
    23.9, "Press release weight (per Rob Rides EMTB)",
    "RockShox ZEB",
    "RockShox Super Deluxe",
    "SRAM Eagle 70 mech T-Type",
    "SRAM Maven Base 4-pot, 200mm",
    "Alloy + Vee/Maxxis tires",
    "Adjustable-travel dropper, size-specific",
    5650, 6399, None, None, None,
    wh_url_rs, IG["Whyte"],
    "180mm/180mm gravity. UK proportional sizing. 12A fast charger NOT included.",
    wh_url_rs
])
bikes.append([
    "Whyte", "Karve EVO", "RSX (top)", "UK", "EXIST",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 180, "Carbon front + alloy rear", "Mullet, 29 conversion ready",
    23.9, "Estimated, RS measured (RSX similar)",
    "RockShox ZEB Ultimate", "RockShox Vivid Ultimate",
    "SRAM AXS Eagle 1x12 T-Type", "SRAM Maven Silver 4-pot, 200mm",
    "Alloy/DT Swiss + Maxxis", "Adjustable-travel dropper",
    7299, 8399, None, None, None,
    wh_url_rsx, IG["Whyte"],
    "Top spec. RideWrap 85% coverage included. 12A fast charger included.",
    wh_url_rsx
])

# ===== YT DECOY X =====
yt_url = "https://www.yt-industries.com/Bikes/Decoy-X/"
bikes.append([
    "YT", "Decoy X", "Launch Edition", "Germany", "EXIST",
    "M2S", 1300, 130, 800, "Avinox 800Wh integrated", "No",
    170, 160, "Hydroformed alloy", "Mullet",
    None, "~24kg estimate (alloy)",
    "FOX Podium upside-down", "FOX Float X2 (custom-tuned)",
    "SRAM X0 Eagle Transmission AXS", "SRAM Maven 4-pot",
    "DT Swiss HX1500 hybrid", "OneUp/RockShox",
    8499, 8999, None, None, None,
    yt_url, IG["YT"],
    "5 sizes (S-XXL). V4L kinematics. Alloy frame keeps cost down.",
    yt_url
])

# ===== APACHE =====
ap_url = "https://apache-bikes.com"
bikes.append([
    "Apache", "Eagle", "3 (entry)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon", "Mullet",
    None, "Not published",
    "FOX 36", "FOX Float", "Shimano XT", "Shimano 4-pot", "Alloy", "Generic",
    None, 5360, None, None, None,
    ap_url, IG["Apache"],
    "Entry of Czech Apache Eagle range.",
    ap_url
])
bikes.append([
    "Apache", "Eagle", "2", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon", "Mullet",
    None, "Not published",
    "FOX 38", "FOX Float X", "SRAM mech", "SRAM Maven", "DT Swiss", "Generic",
    None, 6185, None, None, None,
    ap_url, IG["Apache"],
    "Mid-trim.",
    ap_url
])
bikes.append([
    "Apache", "Eagle", "1 (top)", "Czech Rep.", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon", "Mullet",
    None, "Not published",
    "FOX 38 Factory", "FOX Float X Factory", "SRAM AXS", "SRAM Maven Ultimate", "DT Swiss carbon", "OneUp",
    None, None, None, None, None,
    ap_url, IG["Apache"],
    "Top Eagle, pricing not yet published.",
    ap_url
])

# ===== OLYMPIA =====
ol_url = "https://olympiabici.it"
bikes.append([
    "Olympia", "Hekton 160", "Evo-R", "Italy", "NEW",
    "M2S", 1300, 130, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon", "29 or Mullet flip",
    None, "Not published",
    "FOX 36 Performance", "FOX Float Performance",
    "SRAM mech", "SRAM Maven Base",
    "Alloy", "Generic",
    None, 6690, None, None, None,
    ol_url, IG["Olympia"],
    "160mm Italian.",
    ol_url
])
bikes.append([
    "Olympia", "Hekton 160", "Pro", "Italy", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    160, 150, "Carbon", "29 or Mullet",
    None, "Not published",
    "FOX 38 Factory", "FOX Float X Factory", "SRAM AXS", "SRAM Maven Silver", "DT Swiss", "OneUp",
    None, 6990, None, None, None,
    ol_url, IG["Olympia"],
    "Pro version of Hekton 160, +€300.",
    ol_url
])
bikes.append([
    "Olympia", "Hekton 180", "Evo-R", "Italy", "NEW",
    "M2S", 1300, 150, 800, "Avinox 800Wh integrated", "No",
    180, 170, "Carbon", "Mullet",
    None, "Not published",
    "FOX 38 Performance", "FOX Float X Performance",
    "SRAM mech", "SRAM Maven Base", "Alloy", "Generic",
    None, None, None, None, None,
    ol_url, IG["Olympia"],
    "Long-travel Hekton 180.",
    ol_url
])

# ===== CANYON =====
ca_url = "https://www.canyon.com"
bikes.append([
    "Canyon", "(unannounced)", "(TBA)", "Germany", "EXIST",
    "M2S?", None, None, None, "TBD", "TBD",
    None, None, "TBD", "TBD",
    None, "Not announced",
    "TBD", "TBD", "TBD", "TBD", "TBD", "TBD",
    None, None, None, None, None,
    ca_url, IG["Canyon"],
    "Confirmed Avinox partner per April 9 launch press release. No model announced as of late April.",
    "https://theloamwolf.com/emtb/avinox-launches-m2s-and-m2-motors"
])

# =========================================================================
# Map (brand, model) → specific action/launch Instagram post URL
# Verified via Google site:instagram.com search, April 2026 launch window
# =========================================================================
SPECIFIC_IG = {
    # Amflow PR/PX
    ("Amflow", "PX Carbon"): "https://www.instagram.com/reel/DW6iUlGjJ_W/",      # PX Carbon Pro 2026 Italian action reel
    ("Amflow", "PR Carbon"): "https://www.instagram.com/p/DVZ9zWRjuMo/",         # PR Carbon Pro promo

    # Atherton
    ("Atherton", "S.170E"): "https://www.instagram.com/p/DW5u3aADSYW/",          # "S.170E has landed and it's a thing of..." launch

    # BH
    ("BH", "iLynx+ DL"): "https://www.instagram.com/reel/DW51snOjH-o/",          # Solarider Team review of new BH ILYNX+DL

    # Commencal
    ("Commencal", "Meta Power SX Avinox"): "https://www.instagram.com/reel/DW5trbljGjK/",  # New Meta Power SX Avinox M2S E-Bike

    # Crestline
    ("Crestline", "RS 181.2"): "https://www.instagram.com/p/DKfPmsFs0Pn/",       # RS 181 Spectre Edition launch (DJI Avinox)

    # Crussis - no specific April Avinox post found; brand profile is best
    ("Crussis", "e-Hard 1.11"): "https://www.instagram.com/crussis_en/",
    ("Crussis", "e-Hard 11.11 PRO"): "https://www.instagram.com/crussis_en/",
    ("Crussis", "e-Full 11.11"): "https://www.instagram.com/crussis_en/",
    ("Crussis", "e-Full 12.11"): "https://www.instagram.com/crussis_en/",
    ("Crussis", "e-Full 12.11 PRO"): "https://www.instagram.com/crussis_en/",
    ("Crussis", "e-Full 12.11 PRO X"): "https://www.instagram.com/crussis_en/",

    # Forbidden
    ("Forbidden", "Druid E"): "https://www.instagram.com/p/DIRacewpaep/",        # "Introducing the Druid E Lineup"
    ("Forbidden", "Dreadnought E"): "https://www.instagram.com/forbiddenbikecompany/",  # No specific launch post yet (pre-order)

    # Forestal
    ("Forestal", "e-Siryon V2"): "https://www.instagram.com/forestalbikes/p/DG7k536MpFE/",  # Siryon Halo with upgrades

    # Lee Cougan
    ("Lee Cougan", "Flö"): "https://www.instagram.com/reel/DW5uEd8jVg0/",        # Lee Cougan Flö: Powered by Avinox M2S

    # MAXX
    ("MAXX", "FAB.4 ELA"): "https://www.instagram.com/p/DW6STKQllg7/",           # "Das neue Fab4 ELA ist da, unser erstes Carbon E..."

    # Megamo
    ("Megamo", "Reason"): "https://www.instagram.com/reel/DRubSw3DO2p/",         # Megamo REASON CRB 03 DJI riding reel
    ("Megamo", "Reason AIR"): "https://www.instagram.com/megamo_bicycles/",     # No specific Reason AIR avinox post

    # MMR
    ("MMR", "Lyth"): "https://www.instagram.com/mmrbikes/",                     # No specific launch post (UK pre-order May)

    # Mondraker
    ("Mondraker", "Zendit"): "https://www.instagram.com/p/DWWoP8MkiVp/",         # "Introducing the ZENDIT from @mondrakerbikes"

    # Olympia
    ("Olympia", "Hekton 160"): "https://www.instagram.com/olympiacicli/",       # No specific Hekton avinox post located
    ("Olympia", "Hekton 180"): "https://www.instagram.com/olympiacicli/",

    # Orange
    ("Orange", "Phase Evo Avinox"): "https://www.instagram.com/orangebikes/",   # No specific Phase Evo avinox post located

    # Pivot
    ("Pivot", "Shuttle AMP'd"): "https://www.instagram.com/reel/DWoi7walfI2/",   # "Escape the mundane with the all..." launch reel

    # Raymon
    ("Raymon", "Tarok"): "https://www.instagram.com/r__raymon/",                 # No specific Tarok avinox launch post located

    # Rotwild
    ("Rotwild", "R.EX"): "https://www.instagram.com/p/DUbM5fcCJvm/",             # "Our new Rotwild R.EX 900 with DJI Avinox"
    ("Rotwild", "R.EXC"): "https://www.instagram.com/rotwildbikes/",            # No specific R.EXC launch post yet

    # Steppenwolf
    ("Steppenwolf", "Tundra"): "https://www.instagram.com/steppenwolfbikes/",   # Brand profile (pre-order Autumn 2026)

    # Teewing
    ("Teewing", "Turbo Force"): "https://www.instagram.com/teewingbikes/",      # Brand profile (no specific launch URL)
    ("Teewing", "Flux One"): "https://www.instagram.com/teewingbikes/",         # Brand profile

    # Thömus
    ("Thömus", "Oberrider"): "https://www.instagram.com/reel/DVOaLVXiLT3/",      # NEW THÖMUS OBERRIDER launch reel

    # Unno
    ("Unno", "Mith"): "https://www.instagram.com/p/DIRTQMyRrYE/",               # New Unno Mith with DJI Avinox

    # Velduro
    ("Velduro", "Rogue R"): "https://www.instagram.com/p/DJXvLr5BHfN/",         # "Introducing the @veldurobikes Rogue"

    # Whyte
    ("Whyte", "Karve EVO"): "https://www.instagram.com/reel/DW5trRKIt9V/",      # "Introducing the all-new Karve EVO. For the toughest tracks..."

    # YT
    ("YT", "Decoy X"): "https://www.instagram.com/p/DW6cHYPCMLX/",              # YT Decoy X launch

    # Apache - no IG presence
    ("Apache", "Eagle"): "Not on Instagram (Czech distributor only)",

    # Canyon - confirmed Avinox partner, no model announced yet
    ("Canyon", "(unannounced)"): "https://www.instagram.com/canyon/",
}

# Secondary action post URLs (for inclusion in Notes column)
SECONDARY_IG = {
    ("Amflow", "PX Carbon"): "Also: https://www.instagram.com/p/DVZ9zWRjuMo/ (PR/PX promo)",
    ("Amflow", "PR Carbon"): "Also: https://www.instagram.com/p/DWCmgX5Ep3V/ (demo bikes)",
    ("Pivot", "Shuttle AMP'd"): "Also: https://www.instagram.com/p/DWpdnzGAeo6/ (Supersonic) ; https://www.instagram.com/reel/DWzPW3uj1eh/ (Pivot+Avinox)",
    ("Whyte", "Karve EVO"): "Also: https://www.instagram.com/p/DW3djr7iHkk/ (launch) ; https://www.instagram.com/p/DW57qJ0Fg6u/ (RS+RSX) ; https://www.instagram.com/p/DXCYlL8iILB/ (RSX studio)",
    ("Forbidden", "Druid E"): "Also: https://www.instagram.com/reel/DIR8QhCzUMC/ (everything you need to know reel)",
    ("Mondraker", "Zendit"): "Also: https://www.instagram.com/p/DW6dq27KTqm/ (German launch) ; https://www.instagram.com/reel/DWW_hB2kYaz/ (PERFORMANCE UNLEASHED)",
    ("Atherton", "S.170E"): "Also: https://www.instagram.com/p/DUI2HEJDG0i/ (Key Specs presale)",
    ("Megamo", "Reason"): "Also: https://www.instagram.com/reel/DSaayPvCu82/ (CRB 03 Feu Flamme) ; https://www.instagram.com/reel/DXOvS09DGJX/ (presentation)",
    ("Crestline", "RS 181.2"): "Also: https://www.instagram.com/reel/DMSFaK_uBGi/ (shipping) ; https://www.instagram.com/reel/DLMIcrOoDxL/ (Eurobike ride)",
    ("Velduro", "Rogue R"): "Also: https://www.instagram.com/veldurobikes/p/DJ3JivApJgb/ ; https://www.instagram.com/reel/DV_3OIWkd2b/ (first arrival)",
    ("Commencal", "Meta Power SX Avinox"): "Also: https://www.instagram.com/p/DW6CtdCjAQM/ (French announcement) ; https://www.instagram.com/reel/DSBLvpLjIKk/ (Spanish review)",
    ("BH", "iLynx+ DL"): "Also: https://www.instagram.com/reel/DJ9xOAtPw5j/ (older iLynx+ Enduro 9.7)",
    ("Forestal", "e-Siryon V2"): "Also: https://www.instagram.com/p/DNQ5w_OoYp_/ (Siryon in-house masterpiece)",
    ("Thömus", "Oberrider"): "Also: https://www.instagram.com/p/DVObKazkoOz/ (High-Pivot, High Power) ; https://www.instagram.com/p/DVObMVrkrOE/ ; https://www.instagram.com/reel/DXGjvlrsHpa/",
    ("Unno", "Mith"): "Also: https://www.instagram.com/mbrmagazine/p/DIRTKT3tnnt/ (MBR coverage)",
    ("YT", "Decoy X"): "Also: https://www.instagram.com/p/DW6nv_VClIc/ (Avinox is here)",
}

# Apply specific IG post URLs to bikes (overwrite column index 29 = IG)
for i, bike in enumerate(bikes):
    key = (bike[0], bike[1])
    if key in SPECIFIC_IG:
        bikes[i][29] = SPECIFIC_IG[key]
    if key in SECONDARY_IG:
        # append secondary URLs to notes column (index 30)
        existing_note = bikes[i][30] or ""
        bikes[i][30] = existing_note + " || " + SECONDARY_IG[key]

# Now write all bikes
brand_alt = False
current_brand = None

for row_idx, bike in enumerate(bikes, 2):
    brand = bike[0]
    if brand != current_brand:
        brand_alt = not brand_alt
        current_brand = brand

    base_fill_color = "F2F2F2" if brand_alt else "FFFFFF"

    motor = bike[5]
    peak_w = bike[6]
    removable = bike[10]
    notes = bike[30] if len(bike) > 30 else ""
    is_preorder = "PRE-ORDER" in (notes or "") or "TBA" in (bike[2] or "") or "unannounced" in (bike[2] or "")

    if is_preorder:
        row_fill = yellow_fill
    elif removable == "Yes":
        row_fill = green_fill
    elif motor == "M1":
        row_fill = red_fill
    elif peak_w == 1500:
        row_fill = blue_fill
    else:
        row_fill = PatternFill("solid", fgColor=base_fill_color)

    for col_idx, value in enumerate(bike, 1):
        c = ws.cell(row=row_idx, column=col_idx, value=value)
        c.font = data_font
        c.alignment = data_align
        c.border = border
        c.fill = row_fill
        # Make hyperlink columns blue and underlined
        if col_idx in (29, 30, 32):  # Photo Link, Instagram, Source URL
            if value and isinstance(value, str) and (value.startswith("http") or value.startswith("https")):
                c.font = Font(name="Arial", size=8, color="0563C1", underline="single")
                c.hyperlink = value
    ws.cell(row=row_idx, column=1).font = Font(name="Arial", size=8, bold=True)

# Column widths
widths = {
    'A': 12, 'B': 18, 'C': 22, 'D': 14, 'E': 6,
    'F': 6, 'G': 7, 'H': 7,
    'I': 8, 'J': 18, 'K': 8,
    'L': 8, 'M': 8,
    'N': 22, 'O': 18,
    'P': 8, 'Q': 22,
    'R': 22, 'S': 22, 'T': 22, 'U': 22, 'V': 22, 'W': 18,
    'X': 7, 'Y': 7, 'Z': 7, 'AA': 7, 'AB': 7,
    'AC': 32, 'AD': 30,
    'AE': 36, 'AF': 36
}
for col, w in widths.items():
    ws.column_dimensions[col].width = w

ws.row_dimensions[1].height = 36
for r in range(2, len(bikes) + 2):
    ws.row_dimensions[r].height = 50

# Number formatting
for r in range(2, len(bikes) + 2):
    for col_letter in ['X', 'Y', 'Z', 'AA', 'AB']:
        cell = ws[f"{col_letter}{r}"]
        cell.number_format = '#,##0;(#,##0);"-"'
    ws[f"I{r}"].number_format = '#,##0'
    ws[f"P{r}"].number_format = '0.0'

ws.freeze_panes = "F2"
ws.auto_filter.ref = ws.dimensions

# =========================================================================
# SHEET 2: Key & Methodology
# =========================================================================
ws2 = wb.create_sheet("Key & Methodology")
ws2.column_dimensions['A'].width = 24
ws2.column_dimensions['B'].width = 105

legend = [
    ("AVINOX BIKE COMPARISON — DEEP REFRESH", "April 2026, post-Avinox M2S launch event"),
    ("", ""),
    ("HOW TO READ THIS SHEET", ""),
    ("Multiple builds per model", "Each row is one specific build. Brands like Forbidden Druid E (8 configs across 4 tiers × 2 batteries) and Megamo Reason (10+ builds) are nested as separate rows."),
    ("Brand grouping", "Brands are color-banded (alternating white/grey backgrounds) to keep configs of the same model visually grouped."),
    ("Status flags", "NEW = added since April 11 refresh. UPD = existing model with refreshed motor/spec/pricing. EXIST = unchanged from previous list."),
    ("Photo Link column", "Each cell links to a manufacturer product page or direct CDN image URL where available. Click the cell (highlighted blue) to open. Where I had a direct image URL, I used that; otherwise I link to the model's spec page where the bike is pictured."),
    ("Instagram column", "Each cell links to the brand's official Instagram account. Action shots are best browsed by scrolling the brand feed — most have Avinox launch posts from April 9-11 2026 pinned or near the top. Instagram doesn't allow direct deep-linking to filter posts by bike model."),
    ("", ""),
    ("ROW HIGHLIGHT COLOURS (priority order)", ""),
    ("Yellow", "Pre-order / unannounced / unspecified config (e.g. Steppenwolf Tundra Autumn 2026, Forbidden Dreadnought E, Canyon)."),
    ("Green", "Removable battery — currently rare. Limited to: Amflow PR (RS800/RS600), MAXX FAB.4 ELA, Rotwild R.EX & R.EXC (864Wh custom), Forbidden Druid E (RS600/RS800)."),
    ("Light blue", "Full 1500W peak power — only achievable with the new FP700 700Wh integrated battery, not RS800 800Wh removable."),
    ("Light red", "Avinox M1 motor (older spec, 1000W/120Nm Boost) — Orange Phase Evo and Rotwild R.EX still on M1."),
    ("Plain", "Standard M2S/M2 with integrated 800Wh, capped at 1300W peak."),
    ("", ""),
    ("THE 1500W vs 1300W NUANCE — IMPORTANT", ""),
    ("M2S motor capability", "Avinox M2S Drive Unit: 130Nm continuous / 150Nm peak (60s Boost) / 1300W continuous / 1500W peak."),
    ("Battery determines peak", "M2S delivers full 1500W peak ONLY when paired with new FP700 (700Wh integrated) or compatible high-discharge battery. With standard RS800 800Wh battery, peak is capped at 1300W. The M2S can still pull 150Nm of torque at the wheel either way."),
    ("Practical impact", "Most riders won't notice the 1300W vs 1500W difference, since 1500W only kicks in during 60-second Boost bursts. The more meaningful spec is 130Nm continuous torque (vs M1's 105Nm)."),
    ("FP700 bikes", "Only Amflow PX series (700Wh slim battery), Atherton S.170E (700Wh), Raymon Tarok Ultra (700Wh) are confirmed FP700 = full 1500W. Everyone else with 800Wh = 1300W max."),
    ("M2 motor", "Lower-tier: 1100W peak / 110Nm continuous / 125Nm Boost. On Forbidden T3/T4, Amflow PR Carbon, Raymon Tarok Pro."),
    ("M1 motor", "Outgoing: 1000W peak / 105Nm continuous / 120Nm Boost. Still on Orange Phase Evo, Rotwild R.EX. NOT to be confused with M2S."),
    ("", ""),
    ("BATTERY VARIANTS", ""),
    ("FP700 (NEW)", "700Wh integrated, 220Wh/kg, 3.18kg. Unlocks full 1500W. Slim format. Apple Find My on Amflow PR/PX."),
    ("RS800 (NEW)", "800Wh removable, 200Wh/kg, ~4kg. Caps M2S at 1300W. Quick-release."),
    ("RS600 (NEW)", "600Wh removable, ~2.96kg. Can be used externally as dual-battery on some bikes."),
    ("Rotwild IPU 900", "Custom Rotwild 864Wh removable battery. Largest capacity in any Avinox bike. 200Wh/kg, ~3.58kg."),
    ("Standard 800Wh integrated", "Original Avinox 800Wh, fixed in frame. Most M2S bikes use this. Caps peak at 1300W."),
    ("Standard 600Wh integrated", "Cheaper/lighter alternative on entry-level builds (Crussis e-Hard 1.11, etc.)"),
    ("", ""),
    ("BRAND INSTAGRAM HANDLES (verified April 2026)", ""),
    ("Amflow", "@amflowbikes — https://www.instagram.com/amflowbikes/"),
    ("Atherton", "@athertonbikes (151K followers) — https://www.instagram.com/athertonbikes/"),
    ("BH Bikes", "@bh_bikes (276K followers) — https://www.instagram.com/bh_bikes/"),
    ("Canyon", "@canyon (2M followers) — https://www.instagram.com/canyon/"),
    ("Commencal", "@commencalbikes (498K) — https://www.instagram.com/commencalbikes/ ; US: @commencalusa"),
    ("Crestline", "@crestlinebikes (26K) — https://www.instagram.com/crestlinebikes/"),
    ("Crussis", "@crussis_en (English) or @crussis (Czech, 5K)"),
    ("Forbidden Bike Co.", "@forbiddenbikecompany (120K) — https://www.instagram.com/forbiddenbikecompany/"),
    ("Forestal", "@forestalbikes (23K) — https://www.instagram.com/forestalbikes/"),
    ("Lee Cougan", "@leecouganbicycles (18K) — https://www.instagram.com/leecouganbicycles/"),
    ("MAXX", "@maxxbikes (2.4K) — https://www.instagram.com/maxxbikes/"),
    ("Megamo", "@megamo_bicycles (69K) — https://www.instagram.com/megamo_bicycles/"),
    ("MMR", "@mmrbikes (57K) — https://www.instagram.com/mmrbikes/"),
    ("Mondraker", "@mondrakerbikes (188K) — https://www.instagram.com/mondrakerbikes/"),
    ("Olympia (Italy)", "@olympiacicli — https://www.instagram.com/olympiacicli/"),
    ("Orange Bikes", "@orangebikes (83K) — https://www.instagram.com/orangebikes/"),
    ("Pivot Cycles", "@pivotcycles (189K) — https://www.instagram.com/pivotcycles/ ; EU: @pivotcycleseu"),
    ("Raymon", "@r__raymon (25K) — https://www.instagram.com/r__raymon/"),
    ("Rotwild", "@rotwildbikes (31K) — https://www.instagram.com/rotwildbikes/"),
    ("Steppenwolf", "@steppenwolfbikes (3.4K) — https://www.instagram.com/steppenwolfbikes/"),
    ("Teewing", "@teewingbikes (2K) — https://www.instagram.com/teewingbikes/"),
    ("Thömus", "@thoemus (17K) — https://www.instagram.com/thoemus/"),
    ("Unno", "@rideunno (70K) — https://www.instagram.com/rideunno/"),
    ("Velduro", "@veldurobikes (6K) — https://www.instagram.com/veldurobikes/"),
    ("Whyte Bikes", "@whytebikes (33K) — https://www.instagram.com/whytebikes/"),
    ("YT Industries", "@yt_industries (852K) — https://www.instagram.com/yt_industries/"),
    ("Apache (Czech)", "No verified main IG account; brand uses Czech distributor channels."),
    ("", ""),
    ("PHOTO LINK NOTES", ""),
    ("Direct image URLs", "Where I have a direct CDN image URL (Amflow has them on their CDN, Lee Cougan exposes them via WordPress media), the cell links to a clean studio shot."),
    ("Product page links", "For most other brands, the cell links to the manufacturer's product page where you can scroll through all the bike's images and select your preferred one. Brands like Whyte, Forbidden, Pivot have particularly nice galleries."),
    ("Manufacturer best", "Highest-quality images are on the manufacturer's own product pages. Press images on Pinkbike/Bikerumor are screenshot-able but lower res."),
]

for r, (a, b) in enumerate(legend, 1):
    ws2.cell(row=r, column=1, value=a)
    ws2.cell(row=r, column=2, value=b)
    if r == 1:
        ws2.cell(row=r, column=1).font = Font(bold=True, size=14, name="Arial")
        ws2.cell(row=r, column=2).font = Font(italic=True, size=11, name="Arial")
    elif a in ["HOW TO READ THIS SHEET", "ROW HIGHLIGHT COLOURS (priority order)",
               "THE 1500W vs 1300W NUANCE — IMPORTANT", "BATTERY VARIANTS",
               "BRAND INSTAGRAM HANDLES (verified April 2026)",
               "PHOTO LINK NOTES"]:
        ws2.cell(row=r, column=1).font = Font(bold=True, size=11, name="Arial", color="1F4E79")
    else:
        ws2.cell(row=r, column=1).font = Font(bold=True, name="Arial", size=10)
        ws2.cell(row=r, column=2).font = Font(name="Arial", size=10)
    ws2.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws2.row_dimensions[r].height = 25 if b else 12

# =========================================================================
# SHEET 3: Sources
# =========================================================================
ws3 = wb.create_sheet("Sources")
ws3.column_dimensions['A'].width = 22
ws3.column_dimensions['B'].width = 95

sources = [
    ("PRIMARY MANUFACTURER SOURCES", ""),
    ("Amflow PX specs", "https://www.amflowbikes.com/px-carbon/specs"),
    ("Amflow PR specs", "https://www.amflowbikes.com/pr-carbon/specs"),
    ("Atherton S.170E", "https://athertonbikes.com"),
    ("BH iLynx+ DL", "https://www.bhbikes.com/en_GB/e-mtb/enduro/ilynx-plus-dl"),
    ("Crussis e-bikes 2026", "https://www.crussis.com/products/ebikes-2026"),
    ("Forbidden Druid E", "https://forbiddenbike.com/bikes/druid-e/"),
    ("Forestal e-Siryon V2", "https://forestal.com/en/products/siryon"),
    ("Lee Cougan Flö", "https://leecougan.com/en/bikes/e-bikes/flo"),
    ("MAXX FAB.4 ELA", "https://www.maxx.de/en/bikes/e-mtb/fab4_ela/"),
    ("Megamo Reason", "https://www.megamo.com/en/e-bike/e-full-suspension/reason"),
    ("Pivot Shuttle AMP'd", "https://pivotcycles.com/bike/shuttle-ampd/"),
    ("Rotwild R.EX Core", "https://www.rotwild.com/en/r.ex-core/20386"),
    ("Rotwild R.EXC Pro", "https://www.rotwild.com/en/r.exc-pro/20395"),
    ("Whyte Karve EVO RS", "https://whytebikes.com/products/karve-evo-rs-trail-enduro-electric-mountain-bike"),
    ("Whyte Karve EVO RSX", "https://whytebikes.com/products/karve-evo-rsx-trail-enduro-electric-mountain-bike"),
    ("Avinox official", "https://www.avinox-ebike.com"),
    ("", ""),
    ("INDUSTRY REVIEW & PRESS SOURCES", ""),
    ("Avinox launch press release", "https://theloamwolf.com/emtb/avinox-launches-m2s-and-m2-motors/"),
    ("BikeRadar 14-bike roundup", "https://www.bikeradar.com/news/bikes-with-avinox-m2-m2s-motors"),
    ("BikeMag complete brand list", "https://www.bikemag.com/news/brands-using-the-new-avinox-motors"),
    ("Bikerumor avalanche roundup", "https://bikerumor.com/an-avinox-avalanche-nine-of-the-many-new-emtbs-launching-with-the-avinox-m2s-drive-unit/"),
    ("E-MOUNTAINBIKE Amflow PR Carbon Pro", "https://ebike-mtb.com/en/amflow-pr-carbon-pro-test/"),
    ("E-MOUNTAINBIKE Megamo CRB 01 2027", "https://ebike-mtb.com/en/megamo-reason-crb-test-2027/"),
    ("E-MOUNTAINBIKE Pivot Shuttle AMP'd", "https://ebike-mtb.com/en/pivot-shuttle-ampd-test/"),
    ("E-MOUNTAINBIKE Rotwild R.EX Ultra", "https://ebike-mtb.com/en/rotwild-r-ex-ultra-in-test/"),
    ("Pinkbike Pivot first look", "https://www.pinkbike.com/news/first-look-pivot-shuttle-ampd-avinox.html"),
    ("Pinkbike Forbidden Druid E", "https://www.pinkbike.com/news/forbidden-druid-e-gets-avinox-m2s-and-m2-upgrades-for-2026.html"),
    ("Pinkbike BH iLynx+ DL", "https://www.pinkbike.com/news/bh-bikes-unveils-the-ilynx-dl-with-avinox-m2s.html"),
    ("Pinkbike Velduro Rogue", "https://www.pinkbike.com/news/first-ride-the-avinox-powered-velduro-rogue-r-is-dh-bike-in-an-enduro-bikes-clothing.html"),
    ("Singletrack 12 brands DJI", "https://singletrackworld.com/2025/06/12-bike-brands-using-the-dji-avinox-motor/"),
    ("Road.cc 18 bikes guide", "https://road.cc/offroad/feature/the-avinox-m2-is-here-18-e-mountain-bikes-we-know-that-come-with-avinoxs-newest-e-mtb-motor"),
    ("Velomotion Avinox bikes overview", "https://velomotion.net/2026/04/das-sind-die-bikes-mit-dem-neuen-avinox-m2-motor/"),
]

for r, (a, b) in enumerate(sources, 1):
    ws3.cell(row=r, column=1, value=a)
    ws3.cell(row=r, column=2, value=b)
    if r == 1 or a in ["INDUSTRY REVIEW & PRESS SOURCES"]:
        ws3.cell(row=r, column=1).font = Font(bold=True, size=12, name="Arial", color="1F4E79")
    else:
        ws3.cell(row=r, column=1).font = Font(bold=True, name="Arial", size=10)
        if b and b.startswith("http"):
            ws3.cell(row=r, column=2).font = Font(name="Arial", size=10, color="0563C1", underline="single")
            ws3.cell(row=r, column=2).hyperlink = b
        else:
            ws3.cell(row=r, column=2).font = Font(name="Arial", size=10)
    ws3.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws3.row_dimensions[r].height = 22

wb.move_sheet("Bikes Full Spec", offset=-2)

import os
os.makedirs('tmp', exist_ok=True)
out = 'tmp/Avinox_Bikes_Deep_Spec_Comparison_April_2026.xlsx'
wb.save(out)

print(f"Saved {out}")
print(f"Total rows: {len(bikes)}")
print(f"Brands covered: {len(set(b[0] for b in bikes))}")
