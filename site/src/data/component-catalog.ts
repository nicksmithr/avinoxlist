export interface ComponentPrices {
  gbp: number;
  eur: number;
  usd: number;
}

export interface ComponentCatalog {
  fork: Record<string, ComponentPrices>;
  shock: Record<string, ComponentPrices>;
  drivetrain: Record<string, ComponentPrices>;
  brakes: Record<string, ComponentPrices>;
  wheelset: Record<string, ComponentPrices>;
  dropper: Record<string, ComponentPrices>;
}

export type ComponentCategory = keyof ComponentCatalog;

// Canonical component → retail price map.
// Prices are approximate MSRP for aftermarket purchase (whole units, no pence/cents).
// Sources: manufacturer sites, chain reaction, bike-discount.de, worldwide cyclery.
export const catalog: ComponentCatalog = {
  fork: {
    // FOX Podium Factory (USD fork, top tier)
    "FOX Podium Factory": { gbp: 1450, eur: 1650, usd: 1800 },
    // FOX 38 Factory GRIP X2 (Kashima)
    "FOX 38 Factory": { gbp: 1050, eur: 1200, usd: 1300 },
    // FOX 38 Performance
    "FOX 38 Performance": { gbp: 700, eur: 800, usd: 870 },
    // FOX 38 (unspecified tier, assume Performance)
    "FOX 38": { gbp: 700, eur: 800, usd: 870 },
    // FOX 36 Factory GRIP X2
    "FOX 36 Factory": { gbp: 950, eur: 1090, usd: 1180 },
    // FOX 36 Performance
    "FOX 36 Performance": { gbp: 620, eur: 710, usd: 770 },
    // FOX 36 (unspecified, assume Performance)
    "FOX 36": { gbp: 620, eur: 710, usd: 770 },
    // FOX 36 Float SL Factory (lightweight)
    "FOX 36 Float SL Factory": { gbp: 1050, eur: 1200, usd: 1300 },
    // FOX 36 Float SL Performance
    "FOX 36 Float SL Performance": { gbp: 720, eur: 820, usd: 890 },
    // FOX 36 Rhythm
    "FOX 36 Rhythm": { gbp: 480, eur: 550, usd: 600 },
    // FOX 34 AWL (trail, lighter duty)
    "FOX 34 AWL": { gbp: 520, eur: 600, usd: 650 },
    // FOX AWL HD 36 (new gen heavy duty)
    "FOX AWL HD 36": { gbp: 650, eur: 740, usd: 800 },
    // FOX AWL HD (unspecified)
    "FOX AWL HD": { gbp: 600, eur: 680, usd: 740 },
    // FOX AWL HD Sport
    "FOX AWL HD Sport": { gbp: 480, eur: 550, usd: 600 },
    // FOX Podium AM upside-down
    "FOX Podium AM": { gbp: 1350, eur: 1540, usd: 1670 },
    // RockShox ZEB Ultimate
    "RockShox ZEB Ultimate": { gbp: 850, eur: 970, usd: 1050 },
    // RockShox ZEB Select+
    "RockShox ZEB Select+": { gbp: 580, eur: 660, usd: 720 },
    // RockShox ZEB Select
    "RockShox ZEB Select": { gbp: 480, eur: 550, usd: 600 },
    // RockShox ZEB (base)
    "RockShox ZEB": { gbp: 400, eur: 460, usd: 500 },
    // RockShox Lyrik Ultimate
    "RockShox Lyrik Ultimate": { gbp: 780, eur: 890, usd: 970 },
    // RockShox Lyrik Select+
    "RockShox Lyrik Select+": { gbp: 520, eur: 600, usd: 650 },
    // RockShox Lyrik Select
    "RockShox Lyrik Select": { gbp: 430, eur: 490, usd: 530 },
    // RockShox Lyrik (base)
    "RockShox Lyrik": { gbp: 380, eur: 430, usd: 470 },
    // RockShox Domain Gold R (entry enduro)
    "RockShox Domain": { gbp: 350, eur: 400, usd: 430 },
    // Generic/Configurable
    "_default": { gbp: 600, eur: 690, usd: 750 },
  },

  shock: {
    // FOX Float X2 Factory
    "FOX Float X2 Factory": { gbp: 650, eur: 740, usd: 800 },
    // FOX Float X2 (Performance/unspecified)
    "FOX Float X2": { gbp: 480, eur: 550, usd: 600 },
    // FOX Float X Factory
    "FOX Float X Factory": { gbp: 500, eur: 570, usd: 620 },
    // FOX Float X Performance
    "FOX Float X Performance": { gbp: 380, eur: 430, usd: 470 },
    // FOX Float X (unspecified)
    "FOX Float X": { gbp: 380, eur: 430, usd: 470 },
    // FOX Float X Live Valve Neo
    "FOX Float X Live Valve": { gbp: 700, eur: 800, usd: 870 },
    // FOX Float X Rhythm
    "FOX Float X Rhythm": { gbp: 300, eur: 340, usd: 370 },
    // FOX Float Performance (non-X)
    "FOX Float Performance": { gbp: 320, eur: 370, usd: 400 },
    // FOX Float Factory (non-X)
    "FOX Float Factory": { gbp: 450, eur: 510, usd: 560 },
    // FOX Float (unspecified)
    "FOX Float": { gbp: 300, eur: 340, usd: 370 },
    // FOX Rhythm
    "FOX Rhythm": { gbp: 250, eur: 290, usd: 310 },
    // FOX DHX2 SLS Coil
    "FOX DHX2": { gbp: 600, eur: 680, usd: 740 },
    // FOX X2 Factory
    "FOX X2 Factory": { gbp: 650, eur: 740, usd: 800 },
    // RockShox Super Deluxe Ultimate
    "RockShox Super Deluxe Ultimate": { gbp: 550, eur: 630, usd: 680 },
    // RockShox Super Deluxe Select+
    "RockShox Super Deluxe Select+": { gbp: 380, eur: 430, usd: 470 },
    // RockShox Super Deluxe Select
    "RockShox Super Deluxe Select": { gbp: 320, eur: 370, usd: 400 },
    // RockShox Super Deluxe (base)
    "RockShox Super Deluxe": { gbp: 280, eur: 320, usd: 350 },
    // RockShox Deluxe Select
    "RockShox Deluxe Select": { gbp: 250, eur: 290, usd: 310 },
    // RockShox Vivid Ultimate
    "RockShox Vivid Ultimate": { gbp: 580, eur: 660, usd: 720 },
    // RockShox Vivid Coil
    "RockShox Vivid Coil": { gbp: 420, eur: 480, usd: 520 },
    // RockShox Vivid Air Select+
    "RockShox Vivid Air Select+": { gbp: 380, eur: 430, usd: 470 },
    // RockShox Vivid Select Air
    "RockShox Vivid Select": { gbp: 350, eur: 400, usd: 430 },
    "_default": { gbp: 350, eur: 400, usd: 430 },
  },

  drivetrain: {
    // SRAM XX Eagle AXS T-Type (top tier wireless)
    "SRAM XX AXS": { gbp: 2200, eur: 2500, usd: 2700 },
    // SRAM XX/S1000 hybrid
    "SRAM XX S1000": { gbp: 2000, eur: 2280, usd: 2470 },
    // SRAM X0 Eagle AXS T-Type
    "SRAM X0 AXS": { gbp: 1500, eur: 1710, usd: 1850 },
    // SRAM S1000 Eagle AXS Transmission
    "SRAM S1000 AXS": { gbp: 1350, eur: 1540, usd: 1670 },
    // SRAM GX Eagle AXS T-Type
    "SRAM GX AXS": { gbp: 1050, eur: 1200, usd: 1300 },
    // SRAM Eagle 90 T-Type (mechanical, mid-range)
    "SRAM Eagle 90": { gbp: 550, eur: 630, usd: 680 },
    // SRAM Eagle 70 T-Type (mechanical, entry)
    "SRAM Eagle 70": { gbp: 380, eur: 430, usd: 470 },
    // SRAM mech AXS (mixed wireless/mechanical)
    "SRAM mech AXS": { gbp: 700, eur: 800, usd: 870 },
    // SRAM mech T-Type (mechanical T-Type unspecified)
    "SRAM mech": { gbp: 450, eur: 510, usd: 560 },
    // SRAM AXS (unspecified wireless)
    "SRAM AXS": { gbp: 1200, eur: 1370, usd: 1480 },
    // Shimano XTR Di2 (electronic top tier)
    "Shimano XTR Di2": { gbp: 2100, eur: 2400, usd: 2600 },
    // Shimano XTR (mechanical)
    "Shimano XTR": { gbp: 1200, eur: 1370, usd: 1480 },
    // Shimano XT Di2
    "Shimano XT Di2": { gbp: 1400, eur: 1600, usd: 1730 },
    // Shimano XT (mechanical 12sp)
    "Shimano XT": { gbp: 550, eur: 630, usd: 680 },
    // Shimano XT LinkGlide
    "Shimano XT LinkGlide": { gbp: 480, eur: 550, usd: 600 },
    // Shimano Deore (12sp mechanical)
    "Shimano Deore": { gbp: 280, eur: 320, usd: 350 },
    // Shimano CUES (11sp)
    "Shimano CUES": { gbp: 230, eur: 260, usd: 280 },
    // Shimano 12sp (unspecified)
    "Shimano 12sp": { gbp: 400, eur: 460, usd: 500 },
    "_default": { gbp: 600, eur: 690, usd: 750 },
  },

  brakes: {
    // SRAM Maven Ultimate (top tier, 4-pot)
    "SRAM Maven Ultimate": { gbp: 380, eur: 430, usd: 470 },
    // SRAM Maven Silver
    "SRAM Maven Silver": { gbp: 280, eur: 320, usd: 350 },
    // SRAM Maven Base
    "SRAM Maven Base": { gbp: 200, eur: 230, usd: 250 },
    // SRAM Maven (unspecified)
    "SRAM Maven": { gbp: 220, eur: 250, usd: 270 },
    // SRAM DB8 Stealth
    "SRAM DB8": { gbp: 160, eur: 180, usd: 200 },
    // SRAM DB4
    "SRAM DB4": { gbp: 120, eur: 140, usd: 150 },
    // Shimano XTR 4-pot
    "Shimano XTR": { gbp: 400, eur: 460, usd: 500 },
    // Shimano XT 4-pot
    "Shimano XT": { gbp: 220, eur: 250, usd: 270 },
    // Shimano Deore 4-pot
    "Shimano Deore": { gbp: 120, eur: 140, usd: 150 },
    // Shimano MT520
    "Shimano MT520": { gbp: 130, eur: 150, usd: 160 },
    // Magura Gustav Pro
    "Magura Gustav Pro": { gbp: 350, eur: 400, usd: 430 },
    // Magura MT5
    "Magura MT5": { gbp: 180, eur: 210, usd: 230 },
    // Magura MT7 Pro
    "Magura MT7 Pro": { gbp: 300, eur: 340, usd: 370 },
    // TRP DHR EVO / DH-R EVO PRO
    "TRP DHR EVO": { gbp: 240, eur: 270, usd: 300 },
    // Tektro (budget)
    "Tektro": { gbp: 80, eur: 90, usd: 100 },
    // Generic 4-pot
    "4-pot": { gbp: 150, eur: 170, usd: 190 },
    "_default": { gbp: 200, eur: 230, usd: 250 },
  },

  wheelset: {
    // DT Swiss HXC 1500/1501 Carbon
    "DT Swiss HXC 1500 carbon": { gbp: 1400, eur: 1600, usd: 1730 },
    // DT Swiss HXC 1700
    "DT Swiss HXC 1700": { gbp: 750, eur: 860, usd: 930 },
    // DT Swiss HX1700 hybrid
    "DT Swiss HX1700": { gbp: 700, eur: 800, usd: 870 },
    // DT Swiss HX1500 hybrid
    "DT Swiss HX1500": { gbp: 900, eur: 1030, usd: 1110 },
    // DT Swiss H1900 alloy
    "DT Swiss H1900": { gbp: 450, eur: 510, usd: 560 },
    // DT Swiss H1700
    "DT Swiss H1700": { gbp: 600, eur: 690, usd: 750 },
    // DT Swiss E532 alloy
    "DT Swiss E532": { gbp: 350, eur: 400, usd: 430 },
    // DT Swiss carbon (generic)
    "DT Swiss carbon": { gbp: 1100, eur: 1250, usd: 1360 },
    // DT Swiss carbon hybrid
    "DT Swiss carbon hybrid": { gbp: 1000, eur: 1140, usd: 1240 },
    // DT Swiss alloy (generic)
    "DT Swiss alloy": { gbp: 400, eur: 460, usd: 500 },
    // DT Swiss (unspecified)
    "DT Swiss": { gbp: 500, eur: 570, usd: 620 },
    // Crankbrothers Synthesis Carbon Enduro
    "Crankbrothers Carbon Enduro": { gbp: 1200, eur: 1370, usd: 1480 },
    // Crankbrothers Synthesis Carbon
    "Crankbrothers Synthesis Carbon": { gbp: 1100, eur: 1250, usd: 1360 },
    // Crankbrothers Alloy 2.0
    "Crankbrothers Alloy 2.0": { gbp: 500, eur: 570, usd: 620 },
    // Crankbrothers Alloy 1.0
    "Crankbrothers Alloy 1.0": { gbp: 380, eur: 430, usd: 470 },
    // Crankbrothers Synthesis Alloy (generic)
    "Crankbrothers Synthesis Alloy": { gbp: 450, eur: 510, usd: 560 },
    // Amflow XMC-30 Carbon
    "Amflow carbon": { gbp: 900, eur: 1030, usd: 1110 },
    // Amflow XMA-30 Alloy
    "Amflow alloy": { gbp: 400, eur: 460, usd: 500 },
    // Megamo carbon
    "Megamo carbon": { gbp: 700, eur: 800, usd: 870 },
    // Megamo alloy
    "Megamo alloy": { gbp: 300, eur: 340, usd: 370 },
    // Ursus alloy
    "Ursus alloy": { gbp: 350, eur: 400, usd: 430 },
    // Crussis alloy
    "Crussis alloy": { gbp: 250, eur: 290, usd: 310 },
    // Generic Carbon
    "Carbon": { gbp: 800, eur: 910, usd: 990 },
    // Generic Alloy
    "Alloy": { gbp: 300, eur: 340, usd: 370 },
    // Generic/unspecified
    "Generic": { gbp: 300, eur: 340, usd: 370 },
    "_default": { gbp: 400, eur: 460, usd: 500 },
  },

  dropper: {
    // RockShox Reverb AXS (wireless electronic)
    "RockShox Reverb AXS": { gbp: 480, eur: 550, usd: 600 },
    // RockShox Reverb V2
    "RockShox Reverb V2": { gbp: 250, eur: 290, usd: 310 },
    // FOX Transfer Factory (Kashima)
    "FOX Transfer Factory": { gbp: 350, eur: 400, usd: 430 },
    // FOX Transfer (Performance)
    "FOX Transfer": { gbp: 250, eur: 290, usd: 310 },
    // FOX Transfer NEO Factory
    "FOX Transfer NEO Factory": { gbp: 400, eur: 460, usd: 500 },
    // FOX Transfer Neo
    "FOX Transfer Neo": { gbp: 320, eur: 370, usd: 400 },
    // OneUp V3
    "OneUp V3": { gbp: 200, eur: 230, usd: 250 },
    // OneUp Dropper (older gen)
    "OneUp Dropper": { gbp: 180, eur: 210, usd: 230 },
    // OneUp (unspecified)
    "OneUp": { gbp: 180, eur: 210, usd: 230 },
    // TranzX Reverse
    "TranzX Reverse": { gbp: 120, eur: 140, usd: 150 },
    // KS 900i / Ragei
    "KS": { gbp: 130, eur: 150, usd: 160 },
    // Lee Cougan dropper
    "Lee Cougan dropper": { gbp: 120, eur: 140, usd: 150 },
    // Eightpins NGS 3.0
    "Eightpins": { gbp: 250, eur: 290, usd: 310 },
    // Megamo dropper
    "Megamo": { gbp: 100, eur: 120, usd: 130 },
    // Amflow dropper
    "Amflow Dropper": { gbp: 150, eur: 170, usd: 190 },
    // Generic/unspecified
    "Generic": { gbp: 120, eur: 140, usd: 150 },
    "_default": { gbp: 150, eur: 170, usd: 190 },
  },
};

// Alias map: raw component string → canonical catalog key.
// Matching order: exact catalog key → alias → longest prefix match → _default.
export const aliases: Record<ComponentCategory, Record<string, string>> = {
  fork: {
    "FOX 38 Factory GRIP X2": "FOX 38 Factory",
    "FOX 38 Factory Kashima": "FOX 38 Factory",
    "FOX 38 Factory, GRIP X2": "FOX 38 Factory",
    "FOX 38 Factory, 180mm, GRIP X2": "FOX 38 Factory",
    "Fox 38 Factory, 180mm, GRIP X2": "FOX 38 Factory",
    "FOX 38 Performance E-Optimised": "FOX 38 Performance",
    "FOX 38 Performance, GRIP": "FOX 38 Performance",
    "FOX 36 Factory MY27, GRIP X2 damper, HSC/LSC/HSR/LSR": "FOX 36 Factory",
    "FOX 36 Factory, 160mm, GRIP X2": "FOX 36 Factory",
    "FOX Float 36 Factory GRIP X2": "FOX 36 Factory",
    "FOX 36 Performance MY27, GRIP damper, 160mm": "FOX 36 Performance",
    "FOX 36 Performance GRIP": "FOX 36 Performance",
    "FOX 36 Performance, 160mm, GRIP": "FOX 36 Performance",
    "FOX 36 Float SL Factory 140mm": "FOX 36 Float SL Factory",
    "FOX 36 Float SL Performance 140mm": "FOX 36 Float SL Performance",
    "FOX Float 36 Rhythm 160mm": "FOX 36 Rhythm",
    "FOX 34 Float AWL 140mm": "FOX 34 AWL",
    "FOX AWL 34": "FOX 34 AWL",
    "FOX AWL HD 36 GRIP X": "FOX AWL HD 36",
    "FOX AWL HD Sport MY27, RAIL 2.0 damper, 160mm": "FOX AWL HD Sport",
    "FOX Podium Factory (USD)": "FOX Podium Factory",
    "FOX Podium Factory upside-down": "FOX Podium Factory",
    "FOX Podium Factory, 160mm, GRIP X2": "FOX Podium Factory",
    "Fox Podium Factory": "FOX Podium Factory",
    "FOX Podium AM (upside-down) GRIP X2": "FOX Podium AM",
    "FOX Podium upside-down": "FOX Podium Factory",
    "FOX Float X2 Factory or Podium": "FOX Podium Factory",
    "RockShox ZEB Ultimate Charger 3.2": "RockShox ZEB Ultimate",
    "RockShox Zeb Ultimate, 180mm, Charger 3.2 RC2": "RockShox ZEB Ultimate",
    "RockShox Zeb Ultimate 2027, 170mm, Charger 3.2 RC2": "RockShox ZEB Ultimate",
    "RockShox ZEB Select+, 180mm, Charger 3.2 RC2": "RockShox ZEB Select+",
    "RockShox ZEB, 180mm": "RockShox ZEB",
    "RockShox Domain Gold R, 170mm": "RockShox Domain",
    "FOX/RockShox": "FOX 38",
    "FOX/RockShox Performance": "FOX 38 Performance",
    "Configurable (typ. FOX 38 / RockShox ZEB)": "FOX 38 Factory",
    "Configurable": "FOX 38 Factory",
  },
  shock: {
    "FOX Float X Factory MY27, 210x55, LSC & LSR adjust": "FOX Float X Factory",
    "FOX Float X Factory, 230x60mm": "FOX Float X Factory",
    "Fox Float X Factory": "FOX Float X Factory",
    "FOX Float X / X2 Factory": "FOX Float X Factory",
    "FOX Float X Performance MY27, 210x55, 2-pos lever": "FOX Float X Performance",
    "FOX Float X Performance, 230x60mm": "FOX Float X Performance",
    "FOX Float Rhythm MY27, custom tune, 210x55": "FOX Float",
    "FOX Float Rhythm": "FOX Float",
    "FOX Float X Rhythm 185x55": "FOX Float X Rhythm",
    "FOX Float X Live Valve Neo": "FOX Float X Live Valve",
    "FOX Float X2 (custom-tuned)": "FOX Float X2 Factory",
    "FOX Float X2 Factory, 230x60mm": "FOX Float X2 Factory",
    "Fox Float X2 Factory": "FOX Float X2 Factory",
    "FOX Float Factory X2": "FOX Float X2 Factory",
    "FOX X2 Factory": "FOX Float X2 Factory",
    "FOX DHX2 SLS Coil": "FOX DHX2",
    "RockShox Super Deluxe Ultimate (custom tune)": "RockShox Super Deluxe Ultimate",
    "RockShox Super Deluxe Base": "RockShox Super Deluxe",
    "RockShox Super Deluxe Select 2027, 230x60mm": "RockShox Super Deluxe Select",
    "RockShox Deluxe Select, 230x60mm": "RockShox Deluxe Select",
    "RockShox Vivid Air Select+": "RockShox Vivid Air Select+",
    "RockShox Vivid Select Air": "RockShox Vivid Select",
    "FOX/RockShox": "FOX Float X",
    "Configurable (typ. FOX Float X / RS SD)": "FOX Float X Factory",
    "Configurable": "FOX Float X Factory",
    "n/a": "_skip",
    "n/a (hardtail)": "_skip",
  },
  drivetrain: {
    "SRAM XX Eagle AXS T-Type": "SRAM XX AXS",
    "SRAM XX Eagle Transmission AXS, Praxis Carbon eCranks 155mm 34T": "SRAM XX AXS",
    "SRAM XX T-Type AXS": "SRAM XX AXS",
    "SRAM XX/S1000 hybrid T-Type": "SRAM XX S1000",
    "SRAM X0 Eagle AXS T-Type": "SRAM X0 AXS",
    "SRAM X0 Eagle T-Type AXS": "SRAM X0 AXS",
    "SRAM X0 Eagle T-Type AXS 12sp, 34T, 10-52T": "SRAM X0 AXS",
    "SRAM X0 Eagle Transmission AXS 1x12, 38T, 10-52T XS-1295": "SRAM X0 AXS",
    "SRAM X0 Eagle Transmission AXS": "SRAM X0 AXS",
    "SRAM X0 Eagle Transmission AXS, Praxis Alloy 155mm": "SRAM X0 AXS",
    "SRAM X0 AXS T-Type": "SRAM X0 AXS",
    "SRAM X0 AXS T-Type 12-sp": "SRAM X0 AXS",
    "SRAM X0 T-Type AXS": "SRAM X0 AXS",
    "SRAM X0 T-Type AXS, 34T, 10-52T": "SRAM X0 AXS",
    "SRAM AXS X0": "SRAM X0 AXS",
    "SRAM S1000 Eagle Transmission AXS 1x12, 38T, 10-52T": "SRAM S1000 AXS",
    "SRAM S1000 Eagle AXS Transmission": "SRAM S1000 AXS",
    "SRAM S1000 Eagle AXS T-Type": "SRAM S1000 AXS",
    "SRAM S1000 AXS T-Type": "SRAM S1000 AXS",
    "SRAM GX Eagle AXS T-Type": "SRAM GX AXS",
    "SRAM GX AXS T-Type": "SRAM GX AXS",
    "SRAM GX Eagle T-Type AXS": "SRAM GX AXS",
    "SRAM GX Eagle T-Type AXS 12sp, 34T, 10-52T": "SRAM GX AXS",
    "SRAM GX T-Type AXS": "SRAM GX AXS",
    "SRAM GX T-Type AXS, 34T, 10-52T": "SRAM GX AXS",
    "SRAM GX Eagle Transmission AXS": "SRAM GX AXS",
    "SRAM GX Eagle Transmission, Praxis Alloy 155mm crank, 34T": "SRAM GX AXS",
    "SRAM AXS Eagle 1x12 T-Type": "SRAM AXS",
    "SRAM AXS Transmission": "SRAM AXS",
    "SRAM AXS T-Type": "SRAM AXS",
    "SRAM Eagle 90 T-Type": "SRAM Eagle 90",
    "SRAM Eagle 90 T-Type 12sp, 34T, 10-52T": "SRAM Eagle 90",
    "SRAM Eagle 90 T-Type, 34T, 10-52T": "SRAM Eagle 90",
    "SRAM Eagle 90 T-Type 1x12": "SRAM Eagle 90",
    "SRAM 90 T-Type": "SRAM Eagle 90",
    "SRAM 90 Eagle 12-sp": "SRAM Eagle 90",
    "SRAM Eagle 70 T-Type": "SRAM Eagle 70",
    "SRAM Eagle 70 T-Type, 34T, 10-52T": "SRAM Eagle 70",
    "SRAM Eagle 70 mech T-Type": "SRAM Eagle 70",
    "SRAM mech AXS T-Type": "SRAM mech AXS",
    "SRAM mech AXS path": "SRAM mech AXS",
    "SRAM mech T-Type": "SRAM mech",
    "SRAM mech": "SRAM mech",
    "Shimano XT mech": "Shimano XT",
    "Shimano XT M8100 12sp": "Shimano XT",
    "Shimano XT M8200 12sp": "Shimano XT",
    "Shimano XT 12-sp": "Shimano XT",
    "Shimano XT LinkGlide 11sp, 34T, 11-50T": "Shimano XT LinkGlide",
    "Shimano Deore 12sp": "Shimano Deore",
    "Shimano Deore mech": "Shimano Deore",
    "Shimano 12sp": "Shimano 12sp",
    "Shimano CUES 11-sp": "Shimano CUES",
    "Shimano/SRAM mech": "SRAM mech",
    "Configurable (Shimano XT / SRAM T-Type)": "SRAM AXS",
    "Configurable": "SRAM AXS",
  },
  brakes: {
    "SRAM Maven Ultimate, 200mm": "SRAM Maven Ultimate",
    "SRAM Maven Ultimate, 200/200mm": "SRAM Maven Ultimate",
    "SRAM Maven Ultimate, HS2 rotors": "SRAM Maven Ultimate",
    "SRAM Maven Ultimate 4-pot, 200mm HS2": "SRAM Maven Ultimate",
    "SRAM Maven Silver, 200mm": "SRAM Maven Silver",
    "SRAM Maven Silver 4-pot, 200mm": "SRAM Maven Silver",
    "SRAM Maven Silver 4-pot, 200mm HS2 rotors": "SRAM Maven Silver",
    "SRAM Maven Silver, Centerline rotors": "SRAM Maven Silver",
    "SRAM Maven Base 4-pot, 200mm": "SRAM Maven Base",
    "SRAM Maven Base 4-pot, 200mm HS2": "SRAM Maven Base",
    "SRAM Maven Base 4-pot, 200mm Centerline": "SRAM Maven Base",
    "SRAM Maven Base, 200mm rotors": "SRAM Maven Base",
    "SRAM Maven Base, Centerline rotors": "SRAM Maven Base",
    "SRAM Maven, 200/200mm": "SRAM Maven",
    "SRAM Maven 4-pot": "SRAM Maven",
    "SRAM DB8 Stealth 4-pot, 200mm": "SRAM DB8",
    "SRAM DB8 Stealth, 200mm": "SRAM DB8",
    "SRAM DB4, Centerline rotors": "SRAM DB4",
    "Shimano XT 4-pot": "Shimano XT",
    "Shimano XT 4-Piston": "Shimano XT",
    "Shimano XT 4-pot, 200mm": "Shimano XT",
    "Shimano XT 4-pot, 203mm Galfer Shark": "Shimano XT",
    "Shimano XTR 4-pot, 200mm": "Shimano XTR",
    "Shimano XTR 4-Piston": "Shimano XTR",
    "Shimano Deore 4-pot": "Shimano Deore",
    "Shimano MT520 4-pot": "Shimano MT520",
    "Shimano 4-pot": "Shimano XT",
    "Magura Gustav Pro 4-pot, 203mm Sensor rotors": "Magura Gustav Pro",
    "Magura Gustav Pro 4-pot": "Magura Gustav Pro",
    "Magura MT5 4-pot": "Magura MT5",
    "TRP DHR EVO 4-pot, 220/203mm": "TRP DHR EVO",
    "TRP DH-R EVO PRO 4-pot, 220/203mm": "TRP DHR EVO",
    "Tektro TKD173 4-pot, 203mm rotors": "Tektro",
    "4-pot hydraulic": "4-pot",
    "4-pot, 200mm rotors": "4-pot",
    "SRAM 4-pot": "SRAM Maven Base",
    "SRAM/Magura 4-pot": "SRAM Maven Base",
    "Magura/SRAM 4-pot": "SRAM Maven Base",
    "Configurable (Magura/SRAM/Shimano)": "SRAM Maven Silver",
    "Configurable": "SRAM Maven Silver",
  },
  wheelset: {
    "DT Swiss HXC 1501 carbon + Maxxis Assegai/DHR II Doubledown": "DT Swiss HXC 1500 carbon",
    "DT Swiss Hybrid HXC1501 carbon + Conti Kryptotal Enduro": "DT Swiss HXC 1500 carbon",
    "DT Swiss HXC 1500": "DT Swiss HXC 1500 carbon",
    "DT Swiss HXC 1700": "DT Swiss HXC 1700",
    "DT Swiss HX1700 hybrid": "DT Swiss HX1700",
    "DT Swiss HX1700 30mm": "DT Swiss HX1700",
    "DT Swiss Hybrid HX1501 MX + Conti Kryptotal Enduro": "DT Swiss HX1500",
    "DT Swiss HX1500 hybrid": "DT Swiss HX1500",
    "DT Swiss H1900 30mm": "DT Swiss H1900",
    "DT Swiss H 1900 alloy": "DT Swiss H1900",
    "DT Swiss H1900": "DT Swiss H1900",
    "DT Swiss H1700": "DT Swiss H1700",
    "DT Swiss E532 alloy + Continental Kryptotal Enduro": "DT Swiss E532",
    "DT Swiss + Maxxis Doubledown": "DT Swiss",
    "DT Swiss + Maxxis": "DT Swiss",
    "DT Swiss + Maxxis Assegai/DHR II": "DT Swiss",
    "DT Swiss/in-house alloy": "DT Swiss alloy",
    "DT Swiss/Megamo carbon": "DT Swiss carbon",
    "Crankbrothers Carbon Enduro 31.5mm": "Crankbrothers Carbon Enduro",
    "Crankbrothers Alloy 2.0 31mm": "Crankbrothers Alloy 2.0",
    "Crankbrothers Alloy 1.0 31.5mm": "Crankbrothers Alloy 1.0",
    "Crankbrothers Synthesis Alloy 29 + Schwalbe Albert Gravity 29x2.5": "Crankbrothers Synthesis Alloy",
    "Crankbrothers Synthesis Alloy 2.0": "Crankbrothers Alloy 2.0",
    "Amflow XMC-30 carbon 30mm, SAPIM E-Light": "Amflow carbon",
    "Amflow XMA-30 alloy 30mm, SAPIM E-Light, Maxxis tires": "Amflow alloy",
    "Amflow XMA-30 alloy 30mm, Maxxis Assegai/DHR II": "Amflow alloy",
    "Amflow XMA-30 alloy 30mm, Schwalbe Magic Mary/Albert Gravity Pro": "Amflow alloy",
    "Megamo alloy + reinforced tires": "Megamo alloy",
    "Megamo own brand": "Megamo alloy",
    "Megamo carbon": "Megamo carbon",
    "Ursus Pura M Alu + Continental Kryptotal Enduro": "Ursus alloy",
    "Ursus + Continental Kryptotal": "Ursus alloy",
    "Crussis alloy": "Crussis alloy",
    "Crussis alloy + Maxxis Assegai/DHR II": "Crussis alloy",
    "Crussis alloy + Maxxis Assegai/DHR II 2.5": "Crussis alloy",
    "Carbon bars + alloy wheels": "Alloy",
    "Carbon bars": "Alloy",
    "Alloy + Vee/Maxxis tires": "Alloy",
    "Alloy/DT Swiss + Maxxis": "DT Swiss alloy",
    "Configurable": "DT Swiss",
  },
  dropper: {
    "OneUp V3 31.6mm": "OneUp V3",
    "OneUp Dropper V3 150-240mm size-specific": "OneUp V3",
    "OneUp V3 150-240mm size-specific": "OneUp V3",
    "OneUp/RockShox": "OneUp V3",
    "Amflow Dropper, M/L 190mm, XL 210mm, XXL 230mm": "Amflow Dropper",
    "Amflow Dropper, M 190mm, L/XL 210mm, XXL 230mm": "Amflow Dropper",
    "FOX Transfer Kashima 120/150/180mm": "FOX Transfer Factory",
    "FOX Transfer Kashima": "FOX Transfer Factory",
    "FOX Transfer Factory 175mm": "FOX Transfer Factory",
    "FOX Transfer NEO Factory 31.6mm": "FOX Transfer NEO Factory",
    "KS 900i": "KS",
    "KS Ragei": "KS",
    "Lee Cougan dropper, 150mm S, 170mm M/L": "Lee Cougan dropper",
    "Eightpins NGS 3.0 up to 225mm": "Eightpins",
    "Eightpins NGS 3.0": "Eightpins",
    "Megamo dropper": "Megamo",
    "Megamo own": "Megamo",
    "RockShox Reverb V2 200mm L": "RockShox Reverb V2",
    "Adjustable-travel dropper, size-specific": "Generic",
    "Adjustable-travel dropper": "Generic",
    "TranzX Reverse": "TranzX Reverse",
    "Configurable": "OneUp V3",
  },
};
