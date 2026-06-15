"""
WhatsApp Cardamom Bot
Built with Flask + Twilio
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# ──────────────────────────────────────────────
# KNOWLEDGE BASE  (from your cardamom PDF)
# ──────────────────────────────────────────────

KNOWLEDGE = {
    "overview": """🌿 *Small Cardamom (Elettaria cardamomum)*

• Family: Zingiberaceae | Chromosome: 2n=48
• Origin: Western Ghats, South India
• Also called: *Queen of Spices / True Cardamom*
• One of the most expensive & oldest spices in the world
• Shade-loving plant (pseophyte)
• Pollinator: Honey bee (_Apis cerana indica_)
• Cultivated for dried fruits (capsules)

Type */menu* to see all topics.""",

    "varieties": """🌱 *Important Cardamom Varieties*

*IISR Avinash* – 847 kg/ha avg yield, rhizome rot resistant, dark green capsules, 6.7% oil. Best for valleys.

*IISR Vijetha* – Resistant to Katte (mosaic) disease. Good for moderate rainfall & shaded areas.

*Appangala-2* – Hybrid, 9.27–29.8 kg/ha, mosaic virus resistant. Suitable 600–1000m altitude.

*ICRI-5* – 1543 kg/ha, drought tolerant, 68% bold capsules. Kerala & Tamil Nadu.

*ICRI-6* – 1900 kg/ha, highest yielder, moderately tolerant to rot, thrips & drought.

*PV-1* – Early maturing, elongated capsules. All Kerala tracts.
*PV-2* – Vazhukka type, 982 kg/ha. Kerala Hill Reserves.
*PV-3* – 1120 kg/ha, parrot green, tolerant to thrips & borer.

Type */cultivars* for Malabar/Mysore/Vazhukka info.""",

    "cultivars": """🗂️ *Three Main Cultivar Types*

*Malabar*
• Prostrate panicle
• Elevation: 600–1200 m
• Spacing: 1.8×1.8 m or 2×2 m (~2500–3000 plants/ha)
• Popular in Karnataka

*Mysore*
• Erect panicle
• Elevation: 900–1200 m
• Spacing: 3×3 m (~1111 plants/ha)
• Grown in Kerala & Tamil Nadu

*Vazhukka*
• Semi-erect panicle
• Elevation: 900–1400 m
• Spacing: 2.4×2.4 m (~1736 plants/ha)
• Popular in Kerala""",

    "climate": """🌦️ *Climate & Soil Requirements*

*Climate:*
• Annual rainfall: 1500–2500 mm (well distributed)
• Temperature: 15°C – 35°C
• Elevation: 600–1200 m above MSL
• Humidity: Tropical humid ideal

*Soil:*
• Forest loam soils, generally acidic
• pH: 5.5 – 6.5
• Humus-rich, low to medium phosphorus
• Medium to high potassium""",

    "propagation": """🌱 *Propagation Methods*

*1. Vegetative (most preferred)*
• Through suckers/rhizomes
• True to parent type
• Bears 1 year earlier than seedlings
• Avoid katte-infected mother clumps!

*2. Seedling Nursery*
• Primary nursery → Secondary nursery (bed or polybag)
• Seeds from Sept harvest (Karnataka) / Nov–Jan (Kerala/TN)
• Germination in 20–25 days
• Polybag nursery reduces nursery period by 5–6 months

*3. Tissue Culture*
• Rapid clonal multiplication (developed by IISR Calicut)

Type */nursery* for detailed nursery steps.""",

    "nursery": """🪴 *Nursery Management*

*Primary Nursery:*
• Beds: 6×1×0.2 m, humus-rich forest soil
• Seed rate: 30–50 g per bed
• Sow in rows of 10 cm spacing, 1–2 cm within row
• Cover with sand + paddy straw mulch
• Germination: 20–25 days
• Transplant at 3–4 leaf stage

*Secondary Nursery (Bed):*
• Transplant spacing: 20–25 cm
• Fertilizer: 90:60:120 g NPK per 6×1 m bed
• Apply in 3 splits at 45-day intervals
• Ready in 8–10 months

*Polybag Nursery:*
• Bag size: 20×20 cm, 100-gauge
• Mix: Top soil : cow dung : sand = 3:1:1
• One seedling per bag""",

    "planting": """🌾 *Main Field Planting*

*Pit Size:*
• Malabar: 45×45×45 cm
• Mysore/Vazhukka: 90×90×45 cm or 90×90×90 cm

*Timing:*
• Planting: June–July with SW monsoon
• Shade trees planted before cardamom in open areas

*Shade Trees Used:*
Vernonia arborea, Toona ciliata, Albizia, Erythrina, Syzygium cumini, Jack tree

*Planting Tips:*
• Avoid deep planting
• Apply 50g rock phosphate + FYM at pit
• Provide stakes against wind
• Trench system (60×30 cm) preferred over pit system""",

    "fertilizer": """🌿 *Fertilizer Recommendations*

*Rainfed:* N:P₂O₅:K₂O = 75:75:150 kg/ha (2 splits)
*Irrigated:* 125:125:250 kg/ha (3 splits)

*Application Timing:* May/June and September/October

*Organic Manures:*
• FYM/compost @ 5 kg/plant (June–July)
• Neem cake @ 1–2 kg/plant
• Vermicompost @ 1 kg/plant

*Micronutrients:*
• Zinc sulphate @ 250 g/100 L (April/May & Sept/Oct)
• Borax @ 7.5 kg/ha (soil application)
• Dolomite @ 2 kg/plant/year if pH < 5.5

*Foliar Spray:* IISR Cardamom Special @ 5 g/L, 3 times/year""",

    "irrigation": """💧 *Irrigation*

• Critical period: January to May (pre-monsoon)
• Interval: 10–15 days till monsoon onset

*Methods:*
• Sprinkler: 25 mm once in 12–15 days
• Drip: 4–9 litres/plant/day
• Mini-sprinkler: 2 hours daily in summer

*Water Conservation:*
• Silt pits (1×0.5×0.6 m) between 4 plants on gentle slopes
• Stone pitching walls at 10–20 m intervals on steep slopes""",

    "pests": """🐛 *Major Pests of Cardamom*

*1. Cardamom Thrips (Sciothrips cardamomi)*
• Most serious pest; damage up to 80%
• High in summer (Feb–May)
• Control: Quinalphos 0.025% spray in Mar–May, Aug–Sep
• Fipronil 0.005% or Spinosad 0.0135% also effective

*2. Shoot & Capsule Borer (Conogethes punctiferalis)*
• Larvae bore pseudostems → 'dead heart' symptom
• Control: Quinalphos 0.075% twice (Feb–Mar, Sep–Oct)

*3. Cardamom Whitefly*
• Nymphs secrete honeydew → sooty mould
• Control: Yellow sticky traps + Neem oil 500 ml + Triton 500 ml/100 L water

*4. Root Grubs (Basilepta fulvicorne)*
• C-shaped grubs feed on roots → yellowing & death
• Control: Entomopathogenic nematodes (Heterorhabditis indica) @ 4 cadavers/plant

Type */diseases* for disease information.""",

    "diseases": """🦠 *Major Diseases of Cardamom*

*1. Katte / Mosaic Disease (Cardamom Mosaic Virus)*
• Transmitted by aphid _Pentalonia nigronervosa_
• Symptoms: Light green stripes on leaves (mosaic pattern)
• Control: Rogue infected plants; use IISR Vijetha variety; destroy alternate hosts

*2. Azhukal (Phytophthora sp.)*
• Occurs during rainy season
• Water-soaked lesions on leaves & capsules; foul smell
• Control: Bordeaux mixture 1% spray; Fosetyl-Al 0.1% drench

*3. Rhizome/Clump Rot (Pythium sp., Rhizoctonia)*
• Yellowing → brittle shoots → foul smell
• Control: Copper oxychloride 2 g/L drench; Trichoderma + Mycorrhiza

*4. Leaf Blight (Colletotrichum gloeosporioides)*
• Reddish-brown patches; burnt appearance
• Control: Bordeaux 1% prophylactic; Carbendazim + Mancozeb 0.1%

*5. Kokke Kandu / Vein Clearing Disease*
• Hook-like tillers; 62–84% yield loss in first year
• Caused by CdVCV; no chemical cure – rogue plants""",

    "harvesting": """🌿 *Harvesting & Processing*

*Bearing Age:*
• Suckers: 2 years after planting
• Seedlings: 3 years after planting
• Capsules ripen 120–135 days after formation

*Harvest Season:*
• Kerala/Tamil Nadu: June–July to Jan–Feb
• Karnataka: August to Dec–January
• Interval: Every 15–30 days

*Maturity Indicators:*
• Dark green rind + black seeds

*Curing Methods:*
1. *Sun Drying* – 5–6 days; poor green colour retention
2. *Flue Curing* (best) – 24–30 hours at 45–55°C; retains green colour
3. *LPG/Diesel dryers* – 16–18 hours; high quality output

*Blanching Innovation:*
Soak in 2% washing soda for 10 min before drying → extends colour retention from 3 to 10 months

*Storage:* Keep at <10% moisture in 300-gauge black polythene lined gunny bags.""",

    "standards": """📋 *FSSAI Standards for Cardamom*

*Whole Cardamom:*
• Extraneous matter: ≤ 1.0%
• Empty/malformed capsules: ≤ 3.0%
• Immature/shrivelled capsules: ≤ 3.0%
• Moisture: ≤ 13.0%
• Total ash (dry basis): ≤ 9.5%
• Volatile oil (dry basis): ≥ 3.5% v/w
• Insect damaged matter: ≤ 1.0%

*Cardamom Seeds:*
• Moisture: ≤ 13.0%
• Total ash: ≤ 9.5%
• Volatile oil: ≥ 3.5%

*Cardamom Powder:*
• Moisture: ≤ 11.0%
• Total ash: ≤ 8.0%
• Volatile oil: ≥ 3.0%""",

    "farmers": """👨‍🌾 *Famous Farmer Varieties*

• *Njallani Green Gold* – Vazhukka; 80% capsules >7mm (Idukki)
• *Wonder Cardamom* – Panicles 1.5–2.0m long; 3–4 kg dry/plant (Idukki)
• *Elarajan* – 80–90% capsules 8–9mm; 2500 kg/ha yield (Kerala)
• *Pappalu* – 2000–2500 kg/ha; 25% dry recovery; long panicles (Idukki)
• *Arjun* – Suitable at 3000 ft MSL; 2000–3000 kg dry/ha (Idukki)
• *Pachaikkai* – 2000 kg/ha; bright green; drought tolerant (Theni, TN)
• *PNS Vaigai* – 900–1400 kg/acre; 60–70% produce ≥7mm (Theni, TN)""",
}

MENU = """🌿 *Cardamom Info Bot – Main Menu*

Choose a topic by typing the command:

🔹 */overview* – Introduction & basics
🔹 */varieties* – Improved varieties & yields
🔹 */cultivars* – Malabar, Mysore, Vazhukka
🔹 */climate* – Climate & soil requirements
🔹 */propagation* – Propagation methods
🔹 */nursery* – Nursery management
🔹 */planting* – Main field planting
🔹 */fertilizer* – Fertilizer & manure
🔹 */irrigation* – Water management
🔹 */pests* – Pest management
🔹 */diseases* – Disease management
🔹 */harvesting* – Harvest & processing
🔹 */standards* – FSSAI quality standards
🔹 */farmers* – Famous farmer varieties

Type */menu* anytime to return here."""

WELCOME = """🌿 *Welcome to the Cardamom Info Bot!*

I can answer your questions about Small Cardamom (Elettaria cardamomum) — cultivation, varieties, diseases, standards & more.

""" + MENU


# ──────────────────────────────────────────────
# WEBHOOK ROUTE
# ──────────────────────────────────────────────

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Map incoming text to a reply
    if any(word in incoming_msg for word in ["hi", "hello", "start", "hey"]):
        reply = WELCOME
    elif "/menu" in incoming_msg or incoming_msg == "menu":
        reply = MENU
    elif "/overview" in incoming_msg or "overview" in incoming_msg:
        reply = KNOWLEDGE["overview"]
    elif "/varieties" in incoming_msg or "variet" in incoming_msg:
        reply = KNOWLEDGE["varieties"]
    elif "/cultivars" in incoming_msg or "cultivar" in incoming_msg or "malabar" in incoming_msg or "mysore" in incoming_msg or "vazhukka" in incoming_msg:
        reply = KNOWLEDGE["cultivars"]
    elif "/climate" in incoming_msg or "climate" in incoming_msg or "soil" in incoming_msg:
        reply = KNOWLEDGE["climate"]
    elif "/propagation" in incoming_msg or "propagat" in incoming_msg or "sucker" in incoming_msg:
        reply = KNOWLEDGE["propagation"]
    elif "/nursery" in incoming_msg or "nursery" in incoming_msg:
        reply = KNOWLEDGE["nursery"]
    elif "/planting" in incoming_msg or "planting" in incoming_msg or "spacing" in incoming_msg:
        reply = KNOWLEDGE["planting"]
    elif "/fertilizer" in incoming_msg or "fertilizer" in incoming_msg or "manure" in incoming_msg or "npk" in incoming_msg:
        reply = KNOWLEDGE["fertilizer"]
    elif "/irrigation" in incoming_msg or "irrigation" in incoming_msg or "water" in incoming_msg:
        reply = KNOWLEDGE["irrigation"]
    elif "/pests" in incoming_msg or "pest" in incoming_msg or "thrips" in incoming_msg or "borer" in incoming_msg:
        reply = KNOWLEDGE["pests"]
    elif "/diseases" in incoming_msg or "disease" in incoming_msg or "katte" in incoming_msg or "azhukal" in incoming_msg:
        reply = KNOWLEDGE["diseases"]
    elif "/harvesting" in incoming_msg or "harvest" in incoming_msg or "curing" in incoming_msg or "process" in incoming_msg:
        reply = KNOWLEDGE["harvesting"]
    elif "/standards" in incoming_msg or "standard" in incoming_msg or "fssai" in incoming_msg or "quality" in incoming_msg:
        reply = KNOWLEDGE["standards"]
    elif "/farmers" in incoming_msg or "farmer" in incoming_msg or "njallani" in incoming_msg:
        reply = KNOWLEDGE["farmers"]
    else:
        reply = """❓ I didn't understand that.

Type */menu* to see all available topics, or try keywords like:
_varieties, diseases, pests, harvesting, fertilizer, irrigation, standards_"""

    msg.body(reply)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
