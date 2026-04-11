import streamlit as st
import random

# =============================================================================
# Page config
# =============================================================================
st.set_page_config(
    page_title="Business Model Fit",
    page_icon="🧩",
    layout="wide",
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# =============================================================================
# VENTURE DEFINITIONS
# =============================================================================
VENTURES = {
    "studyhive": {
        "title": "StudyHive",
        "emoji": "📚",
        "one_liner": "AI powered study group matching for college students",
        "hook": (
            "College students waste hours trying to find good study partners. "
            "StudyHive uses AI to match students by course, learning style, and schedule "
            "into small groups that actually stick. Your challenge: figure out the business "
            "model that turns this useful tool into a real business."
        ),
        "levers": {
            "revenue": {
                "label": "Revenue Model",
                "description": "How does StudyHive make money?",
                "options": {
                    "freemium": {"label": "Freemium", "desc": "Free basic matching. Premium features (AI tutor, priority matching) for a monthly fee."},
                    "subscription": {"label": "Subscription", "desc": "Monthly subscription required for all features. No free tier."},
                    "per_session": {"label": "Pay Per Session", "desc": "Students pay a small fee each time they join a matched study group."},
                    "ad_supported": {"label": "Ad Supported", "desc": "Free for all students. Revenue from educational advertisers and sponsors."},
                },
            },
            "pricing": {
                "label": "Price Point",
                "description": "What does the paid tier cost?",
                "options": {
                    "free": {"label": "$0 (Ad Revenue Only)", "desc": "Completely free to students. Monetize through advertising and data partnerships."},
                    "low": {"label": "$5 per month", "desc": "Low barrier. Easy impulse purchase for students on a budget."},
                    "mid": {"label": "$12 per month", "desc": "Mid range. Positioned as valuable but accessible, less than a textbook."},
                    "high": {"label": "$25 per month", "desc": "Premium positioning. Signals high quality, but may deter budget conscious students."},
                },
            },
            "channel": {
                "label": "Go to Market Channel",
                "description": "How do students discover StudyHive?",
                "options": {
                    "social": {"label": "Social Media / TikTok", "desc": "Viral content strategy. Study tips, memes, and student influencer partnerships."},
                    "campus": {"label": "Campus Ambassadors", "desc": "Student reps at each school. Grassroots, dorm by dorm growth."},
                    "university": {"label": "University Partnerships", "desc": "Official school endorsement. Integrated into student portals and orientation."},
                    "appstore": {"label": "App Store / SEO", "desc": "Organic discovery through search and app store optimization."},
                },
            },
            "segment": {
                "label": "Target Customer",
                "description": "Which students does StudyHive focus on first?",
                "options": {
                    "all_students": {"label": "All College Students", "desc": "Cast a wide net. Anyone in college could use this."},
                    "stem": {"label": "STEM Students", "desc": "Engineering, CS, math, science. High collaboration needs, tough material."},
                    "premed": {"label": "Pre Med Students", "desc": "Extremely motivated, study constantly, willing to invest in tools."},
                    "graduate": {"label": "Graduate Students", "desc": "Smaller market but higher willingness to pay. Already serious about academics."},
                },
            },
        },
        "fit_matrix": {
            "revenue": {"freemium": 1.0, "subscription": 0.50, "per_session": 0.30, "ad_supported": 0.15},
            "pricing": {"mid": 1.0, "low": 0.55, "high": 0.25, "free": 0.20},
            "channel": {"campus": 1.0, "social": 0.50, "university": 0.60, "appstore": 0.30},
            "segment": {"stem": 1.0, "all_students": 0.35, "premed": 0.65, "graduate": 0.45},
        },
        "optimal": {"revenue": "freemium", "pricing": "mid", "channel": "campus", "segment": "stem"},
        "optimal_explanations": {
            "revenue": "Freemium works best because students need to experience the AI matching before they trust it enough to pay. A free tier drives adoption, and premium features (better matches, AI tutor) give a clear upgrade path.",
            "pricing": "$12/month hits the sweet spot. It is less than one textbook, which makes it feel like a deal. $5 undervalues the product and $25 prices out most students.",
            "channel": "Campus ambassadors create peer trust and dorm by dorm virality. Students trust recommendations from classmates far more than ads or institutional endorsements.",
            "segment": "STEM students have the highest need for collaborative study (problem sets, lab prep, coding projects) and naturally form study groups. They are the perfect beachhead market.",
        },
        "base_metrics": {"signups": 80, "active_rate": 0.55, "revenue_per_active": 8, "retention": 0.50},
        "market_events": {
            2: "A major university just announced expanded free tutoring centers on campus. Students are buzzing about alternatives to paid study tools.",
            3: "An edtech investor reached out after seeing your traction. They want to understand your unit economics and retention numbers before a meeting.",
        },
    },
    "localbite": {
        "title": "LocalBite",
        "emoji": "🍳",
        "one_liner": "Marketplace connecting talented home cooks with hungry neighbors",
        "hook": (
            "In every neighborhood, there are amazing home cooks whose food never reaches beyond their own kitchen. "
            "LocalBite connects them with neighbors who want fresh, homemade meals without the restaurant markup. "
            "Your challenge: find the business model that makes this marketplace work for both sides."
        ),
        "levers": {
            "revenue": {
                "label": "Revenue Model",
                "description": "How does LocalBite make money?",
                "options": {
                    "commission": {"label": "Commission Per Order", "desc": "Take a percentage of each meal order. Classic marketplace model."},
                    "cook_sub": {"label": "Cook Subscription", "desc": "Cooks pay a monthly fee to list their meals. Eaters order for free."},
                    "eater_sub": {"label": "Eater Membership", "desc": "Eaters pay monthly for access. Cooks list for free."},
                    "delivery_fee": {"label": "Delivery Fee", "desc": "Charge a flat delivery fee on every order. Food is priced by cooks."},
                },
            },
            "pricing": {
                "label": "Commission / Fee Level",
                "description": "How much does LocalBite take?",
                "options": {
                    "low": {"label": "10% Commission / $2 Fee", "desc": "Cook friendly. Attracts supply but thin margins for the platform."},
                    "mid": {"label": "15% Commission / $4 Fee", "desc": "Balanced take rate. Sustainable for both cooks and the platform."},
                    "high": {"label": "20% Commission / $6 Fee", "desc": "Higher platform margin. Risk of alienating cooks."},
                    "premium": {"label": "25% Commission / $8 Fee", "desc": "Maximum extraction. Could drive cooks to competing platforms."},
                },
            },
            "channel": {
                "label": "Go to Market Channel",
                "description": "How do people discover LocalBite?",
                "options": {
                    "social": {"label": "Instagram / Food Content", "desc": "Beautiful food photography, recipes, cook profiles. Visual marketing."},
                    "nextdoor": {"label": "Neighborhood Apps", "desc": "Nextdoor, local Facebook groups, community boards. Hyperlocal strategy."},
                    "farmers": {"label": "Farmers Market Events", "desc": "Set up at local markets. Let people taste the food, then download the app."},
                    "paid_ads": {"label": "Paid Digital Ads", "desc": "Facebook and Google ads targeting local food lovers."},
                },
            },
            "segment": {
                "label": "Target Customer",
                "description": "Who is the ideal first customer for LocalBite?",
                "options": {
                    "professionals": {"label": "Busy Professionals", "desc": "Time poor, money rich. Want quality meals without cooking or restaurant prices."},
                    "students": {"label": "College Students", "desc": "Tired of dining halls. Budget conscious but high volume."},
                    "families": {"label": "Health Conscious Families", "desc": "Want wholesome meals for their kids. Quality focused, willing to pay."},
                    "elderly": {"label": "Elderly / Limited Mobility", "desc": "Need based market. Difficulty cooking or leaving home."},
                },
            },
        },
        "fit_matrix": {
            "revenue": {"commission": 1.0, "cook_sub": 0.25, "eater_sub": 0.40, "delivery_fee": 0.50},
            "pricing": {"mid": 1.0, "low": 0.55, "high": 0.45, "premium": 0.20},
            "channel": {"nextdoor": 1.0, "social": 0.55, "farmers": 0.65, "paid_ads": 0.30},
            "segment": {"professionals": 1.0, "families": 0.60, "elderly": 0.45, "students": 0.30},
        },
        "optimal": {"revenue": "commission", "pricing": "mid", "channel": "nextdoor", "segment": "professionals"},
        "optimal_explanations": {
            "revenue": "Commission per order aligns incentives perfectly. Cooks only pay when they earn, so there is zero barrier to listing. The platform grows as order volume grows.",
            "pricing": "15% is the marketplace sweet spot. It covers platform costs while keeping cooks motivated. Higher rates push cooks to take orders off platform.",
            "channel": "Neighborhood apps match the hyperlocal nature of home cooking. People want meals from cooks nearby, and community platforms build that trust.",
            "segment": "Busy professionals have the highest order frequency and willingness to pay. They value convenience and quality over price, making them the ideal first customers.",
        },
        "base_metrics": {"signups": 60, "active_rate": 0.45, "revenue_per_active": 12, "retention": 0.45},
        "market_events": {
            2: "A popular local food blogger just featured the 'home cook economy' as the next big trend. Interest in your category is surging.",
            3: "The city health department announced new guidelines for home food businesses. Customers are asking about food safety certifications.",
        },
    },
    "gearshare": {
        "title": "GearShare",
        "emoji": "🏔️",
        "one_liner": "Peer to peer outdoor gear rental for adventure seekers",
        "hook": (
            "Americans spend $887 billion on outdoor recreation annually, but most gear sits in garages 95% of the time. "
            "GearShare lets people rent premium outdoor gear from neighbors: tents, kayaks, bikes, ski equipment, and more. "
            "Your challenge: find the model that turns occasional rentals into a sustainable business."
        ),
        "levers": {
            "revenue": {
                "label": "Revenue Model",
                "description": "How does GearShare make money?",
                "options": {
                    "membership": {"label": "Monthly Membership", "desc": "Members pay monthly for access. Includes insurance and a rental allowance."},
                    "per_rental": {"label": "Per Rental Fee", "desc": "Charge a platform fee on each rental transaction. Pay as you go."},
                    "commission": {"label": "Peer Commission", "desc": "Take a percentage of each peer to peer rental. Owners set their own prices."},
                    "bundle": {"label": "Gear + Experience Bundles", "desc": "Bundle gear rental with guided outdoor experiences and trips."},
                },
            },
            "pricing": {
                "label": "Price Point",
                "description": "What does GearShare cost?",
                "options": {
                    "low": {"label": "$10/mo or $15/rental", "desc": "Low barrier. Attracts casual users but thin margins."},
                    "mid": {"label": "$20/mo or $30/rental", "desc": "Mid range. Good value vs. buying, sustainable margins."},
                    "high": {"label": "$35/mo or $50/rental", "desc": "Premium positioning with full insurance and gear guarantee."},
                    "dynamic": {"label": "Dynamic Pricing", "desc": "Prices flex based on demand, season, and gear popularity."},
                },
            },
            "channel": {
                "label": "Go to Market Channel",
                "description": "How do outdoor enthusiasts discover GearShare?",
                "options": {
                    "instagram": {"label": "Instagram / Influencers", "desc": "Adventure content creators, gear reviews, aspirational outdoor content."},
                    "retail": {"label": "Outdoor Retailer Partners", "desc": "Partner with REI, local gear shops. In store signage and referrals."},
                    "events": {"label": "Adventure Events / Meetups", "desc": "Sponsor trail runs, paddle meetups, climbing events. Community first."},
                    "seo": {"label": "SEO / Content Marketing", "desc": "Blog content, gear guides, trail recommendations. Long term organic growth."},
                },
            },
            "segment": {
                "label": "Target Customer",
                "description": "Who is the ideal GearShare customer?",
                "options": {
                    "weekend": {"label": "Weekend Warriors", "desc": "Casual but consistent. Try new activities regularly. Do not own specialized gear."},
                    "hardcore": {"label": "Hardcore Adventurers", "desc": "Serious outdoor athletes. Want premium gear. Already own a lot."},
                    "families": {"label": "Outdoor Families", "desc": "Kids outgrow gear fast. Parents want to try activities before investing."},
                    "tourists": {"label": "Travelers / Tourists", "desc": "Visiting an area, want gear for a one time trip. High willingness to pay."},
                },
            },
        },
        "fit_matrix": {
            "revenue": {"membership": 1.0, "per_rental": 0.45, "commission": 0.55, "bundle": 0.35},
            "pricing": {"mid": 1.0, "low": 0.50, "high": 0.40, "dynamic": 0.55},
            "channel": {"retail": 1.0, "events": 0.60, "instagram": 0.50, "seo": 0.35},
            "segment": {"weekend": 1.0, "families": 0.55, "tourists": 0.45, "hardcore": 0.30},
        },
        "optimal": {"revenue": "membership", "pricing": "mid", "channel": "retail", "segment": "weekend"},
        "optimal_explanations": {
            "revenue": "Membership creates predictable recurring revenue and makes each rental feel 'free,' driving more usage. Casual renters prefer a flat fee over calculating per trip costs.",
            "pricing": "$20/month is a great deal vs. buying gear that costs hundreds. It is low enough to feel like a no brainer but high enough to build a real business.",
            "channel": "Outdoor retailer partnerships provide built in trust and foot traffic. When REI or a local shop recommends you, credibility is instant.",
            "segment": "Weekend warriors are the sweet spot. They try new activities often (need variety), do not own specialized gear (need rentals), and go out consistently (drive recurring revenue).",
        },
        "base_metrics": {"signups": 50, "active_rate": 0.40, "revenue_per_active": 18, "retention": 0.42},
        "market_events": {
            2: "REI just launched a limited gear rental pilot in 3 test markets. The outdoor community is debating whether big retailers can do rentals right.",
            3: "A competitor just raised $5M and is offering free first month memberships in your top market. Your current customers are asking if you will match the offer.",
        },
    },
}

# =============================================================================
# CUSTOMER QUOTE POOLS
# Each quote: (lever, signal_direction, optimal_values, text)
# signal_direction: "positive" means the current choice is working
#                   "negative" means the current choice is not working
# =============================================================================
QUOTE_POOLS = {
    "studyhive": {
        "revenue": [
            ("positive", ["freemium"], "I tried the free version for a week, fell in love with the matching, and upgraded to premium without thinking twice."),
            ("negative", ["subscription"], "I wanted to try it before paying. Asking for my credit card upfront made me close the app immediately."),
            ("negative", ["per_session"], "Paying each time I study feels like a toll booth. I study 4 times a week and it adds up way too fast."),
            ("negative", ["ad_supported"], "The ads during study sessions are honestly distracting. It kind of defeats the purpose of a focus tool."),
            ("positive", ["freemium", "subscription"], "Having a structured payment keeps me accountable. If I am paying for it, I actually use it."),
        ],
        "pricing": [
            ("positive", ["mid"], "Twelve dollars a month is less than one coffee a week. For something I use daily, that is a steal."),
            ("positive", ["low"], "At five bucks, it was a no brainer to sign up. Though honestly I would pay more if the matching got smarter."),
            ("negative", ["high"], "Twenty five a month? I already pay for Spotify, iCloud, and my phone plan. Something has got to go, and this would be it."),
            ("negative", ["free"], "It is free, so I downloaded it, but I do not really take it seriously. Free tools feel disposable."),
            ("positive", ["mid", "low"], "The price feels fair for how much value I get. I use it more than Netflix."),
        ],
        "channel": [
            ("positive", ["campus"], "My RA told everyone on our floor about it. Now our whole dorm uses it for exam prep."),
            ("negative", ["social"], "I saw it on TikTok once but forgot the name. Did not download it until a friend reminded me weeks later."),
            ("positive", ["university"], "My professor mentioned it in class. I trust it more knowing the school is behind it."),
            ("negative", ["appstore"], "I found it by accident in the App Store. Never heard of it from anyone at school."),
            ("positive", ["campus"], "The campus ambassador in my building set up a demo night. I signed up on the spot."),
        ],
        "segment": [
            ("positive", ["stem"], "As a CS major, finding people who actually understand recursion to study with is worth its weight in gold."),
            ("negative", ["all_students"], "My study group had a film major, an engineer, and an art student. We had absolutely nothing in common."),
            ("positive", ["premed"], "Pre med study groups are intense. This tool makes finding serious, committed partners so much easier."),
            ("negative", ["graduate"], "I am in a grad program with 20 people. I already know everyone. Not sure I need an app for that."),
            ("positive", ["stem", "premed"], "The material is so hard that studying alone is not an option. This tool is becoming essential."),
        ],
    },
    "localbite": {
        "revenue": [
            ("positive", ["commission"], "I love that I only pay the platform when I actually sell a meal. Zero risk to get started as a cook."),
            ("negative", ["cook_sub"], "Paying monthly just to list my meals feels backwards. What if nobody orders? I am out that money."),
            ("negative", ["eater_sub"], "A monthly membership to order food? I do not order often enough to justify that. Let me just pay per meal."),
            ("positive", ["delivery_fee"], "The delivery fee is transparent. I know exactly what I am paying and the cook gets their full price."),
            ("negative", ["cook_sub"], "I know three great cooks who would join, but they will not pay upfront. They need to see orders first."),
        ],
        "pricing": [
            ("positive", ["mid"], "Fifteen percent feels fair. The cook gets most of the money and the platform clearly adds value."),
            ("negative", ["premium"], "Twenty five percent?! At that rate, I would rather just post on Instagram and take orders directly."),
            ("positive", ["low"], "The low platform fee is why I started cooking here instead of other delivery apps. I actually keep my earnings."),
            ("negative", ["high"], "Some cooks are raising prices to cover the platform fee, which makes the food less competitive with restaurants."),
            ("positive", ["mid", "low"], "Compared to DoorDash taking 30%, this feels like a great deal for cooks."),
        ],
        "channel": [
            ("positive", ["nextdoor"], "I found my favorite cook through a Nextdoor post. It feels so much more trustworthy than a random app."),
            ("negative", ["paid_ads"], "I saw a Facebook ad but was not sure if the food was safe. I would need a personal recommendation."),
            ("positive", ["farmers"], "I tried a cook's food at the farmers market and immediately downloaded the app to order again."),
            ("negative", ["social"], "The Instagram photos looked great, but I want to know the cook is in my neighborhood, not across town."),
            ("positive", ["nextdoor"], "My neighbor recommended a cook on LocalBite. That personal connection made me trust it instantly."),
        ],
        "segment": [
            ("positive", ["professionals"], "After a 10 hour workday, having a home cooked meal waiting is literally life changing. Worth every penny."),
            ("negative", ["students"], "The meals are great quality, but $15 for lunch is steep on a student budget. I am back to ramen."),
            ("positive", ["families"], "My kids actually eat the food from LocalBite cooks. It is healthier and cheaper than ordering takeout."),
            ("positive", ["elderly"], "I cannot stand for long in the kitchen anymore. Having a neighbor cook for me has been a blessing."),
            ("negative", ["students"], "I would order more often but honestly I cannot afford it every day. Maybe once a week as a treat."),
        ],
    },
    "gearshare": {
        "revenue": [
            ("positive", ["membership"], "The monthly membership makes each rental feel free. I end up trying way more activities than I would otherwise."),
            ("negative", ["per_rental"], "Calculating the cost each time I want to rent something is annoying. I just want to grab gear and go."),
            ("positive", ["commission"], "I like setting my own rental price for my kayak. The platform just takes a small cut and handles everything else."),
            ("negative", ["bundle"], "I just want to rent a tent, not book a whole guided experience. The bundles feel like an upsell I did not ask for."),
            ("positive", ["membership"], "Knowing I can grab any gear whenever I want for a flat monthly fee makes me say yes to every weekend adventure."),
        ],
        "pricing": [
            ("positive", ["mid"], "Twenty bucks a month to access thousands of dollars of gear? That is the best deal in outdoor recreation."),
            ("negative", ["high"], "Thirty five a month is getting into gym membership territory. I would need to rent almost every weekend to justify that."),
            ("positive", ["low"], "At ten dollars a month, I signed up even though I was not sure I would use it. Now I rent something every other week."),
            ("negative", ["dynamic"], "The price changed three times while I was deciding. I just want to know what it costs without playing a guessing game."),
            ("positive", ["mid", "low"], "The pricing feels really fair compared to what this gear would cost to buy. My garage thanks me."),
        ],
        "channel": [
            ("positive", ["retail"], "The REI associate mentioned GearShare when I was looking at $400 tents. Signed up right there in the store."),
            ("negative", ["seo"], "I found a blog post about gear rentals but there were so many options that I got overwhelmed and gave up."),
            ("positive", ["events"], "I met the GearShare team at a trail run event. Tried a demo and signed up before I got home."),
            ("negative", ["instagram"], "I follow outdoor influencers but their sponsored posts all blur together. Hard to know what is legit."),
            ("positive", ["retail"], "My local gear shop has a GearShare display. Seeing the actual gear I could rent made it real for me."),
        ],
        "segment": [
            ("positive", ["weekend"], "I try a different activity almost every weekend. Buying all that gear would be insane. Renting is perfect."),
            ("negative", ["hardcore"], "I already own all my climbing gear and have strong brand preferences. I do not really need to rent anything."),
            ("positive", ["families"], "My kids want to try everything: kayaking, camping, skiing. With GearShare I can say yes without spending a fortune."),
            ("negative", ["tourists"], "I rented gear once on vacation and it was great, but I am not going to keep a membership for a once a year trip."),
            ("positive", ["weekend"], "I always wanted to try paddleboarding but did not want to buy a board first. GearShare let me test it risk free."),
        ],
    },
}


# =============================================================================
# SESSION STATE
# =============================================================================
def init_state():
    defaults = {
        "stage": "intro",
        "venture_key": None,
        "current_round": 1,
        "configs": {1: None, 2: None, 3: None},
        "results_cache": {1: None, 2: None, 3: None},
        "fit_history": [],
        "email": None,
        "email_skipped": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# =============================================================================
# HELPERS
# =============================================================================
def go(stage):
    st.session_state.stage = stage

def compute_fit(config, venture_key):
    """Compute overall fit score (0 to 1) for a given config."""
    v = VENTURES[venture_key]
    fm = v["fit_matrix"]
    weights = {"revenue": 0.30, "pricing": 0.25, "channel": 0.25, "segment": 0.20}
    total = 0.0
    for lever, w in weights.items():
        val = config.get(lever)
        if val and val in fm[lever]:
            total += w * fm[lever][val]
    return total


def generate_metrics(fit, venture_key, round_num):
    """Generate realistic market metrics based on fit score and round."""
    v = VENTURES[venture_key]
    base = v["base_metrics"]
    # Scale up each round (market awareness grows)
    round_multiplier = {1: 1.0, 2: 2.5, 3: 5.0}[round_num]
    noise = random.uniform(0.9, 1.1)

    signups = int(base["signups"] * (0.3 + 0.7 * fit) * round_multiplier * noise)
    active_rate = min(0.95, base["active_rate"] * (0.4 + 0.6 * fit) * random.uniform(0.92, 1.08))
    active_users = int(signups * active_rate)
    revenue_per = base["revenue_per_active"] * (0.5 + 0.5 * fit) * random.uniform(0.9, 1.1)
    revenue = int(active_users * revenue_per)
    retention = min(0.95, base["retention"] * (0.3 + 0.7 * fit) * random.uniform(0.92, 1.08))

    return {
        "signups": signups,
        "active_users": active_users,
        "revenue": revenue,
        "retention": round(retention * 100),
        "active_rate": round(active_rate * 100),
    }


def select_quotes(config, venture_key, round_num):
    """Select 3 relevant customer quotes based on current config fit."""
    v = VENTURES[venture_key]
    fm = v["fit_matrix"]
    pool = QUOTE_POOLS[venture_key]

    # Rank levers by fit (worst first)
    lever_fits = []
    for lever in ["revenue", "pricing", "channel", "segment"]:
        val = config.get(lever)
        score = fm[lever].get(val, 0.5)
        lever_fits.append((lever, score))
    lever_fits.sort(key=lambda x: x[1])

    random.seed(round_num * 100 + hash(str(config)) % 1000)
    quotes = []

    # Quote tuples are: (direction, values_list, text)
    # q[0] = "positive" or "negative"
    # q[1] = list of values this quote supports
    # q[2] = the quote text string

    # Quote 1: about the weakest lever (hint to change it)
    worst_lever = lever_fits[0][0]
    worst_val = config[worst_lever]
    candidates = [q for q in pool[worst_lever] if worst_val not in q[1]]
    if not candidates:
        candidates = [q for q in pool[worst_lever] if q[0] == "negative"]
    if candidates:
        q = random.choice(candidates)
        quotes.append({"text": q[2], "lever": worst_lever, "signal": "warning"})

    # Quote 2: about the strongest lever (positive reinforcement)
    best_lever = lever_fits[-1][0]
    best_val = config[best_lever]
    candidates = [q for q in pool[best_lever] if best_val in q[1] and q[0] == "positive"]
    if not candidates:
        candidates = [q for q in pool[best_lever] if q[0] == "positive"]
    if candidates:
        q = random.choice(candidates)
        quotes.append({"text": q[2], "lever": best_lever, "signal": "strong"})

    # Quote 3: about a middle lever
    mid_lever = lever_fits[1][0]
    mid_val = config[mid_lever]
    mid_fit = lever_fits[1][1]
    if mid_fit > 0.6:
        candidates = [q for q in pool[mid_lever] if q[0] == "positive"]
    else:
        candidates = [q for q in pool[mid_lever] if q[0] == "negative"]
    if candidates:
        q = random.choice(candidates)
        signal = "strong" if mid_fit > 0.6 else "weak"
        quotes.append({"text": q[2], "lever": mid_lever, "signal": signal})

    # Deduplicate
    seen = set()
    unique = []
    for q in quotes:
        if q["text"] not in seen:
            seen.add(q["text"])
            unique.append(q)

    # Ensure we always have at least 2 quotes by adding from unused levers
    if len(unique) < 2:
        for lever, _ in lever_fits:
            if any(q["lever"] == lever for q in unique):
                continue
            all_quotes = pool.get(lever, [])
            if all_quotes:
                q = random.choice(all_quotes)
                unique.append({"text": q[2], "lever": lever, "signal": "weak"})
            if len(unique) >= 3:
                break

    return unique[:3]


def compute_final_scores(venture_key):
    """Compute the final simulation scores."""
    configs = st.session_state.configs
    fits = []
    for r in [1, 2, 3]:
        if configs[r]:
            fits.append(compute_fit(configs[r], venture_key))
        else:
            fits.append(0)

    # 1. Final Model Fit (40 pts)
    final_fit_pts = fits[2] * 40

    # 2. Iteration Quality (35 pts)
    good_changes = 0
    bad_changes = 0
    total_changes = 0
    fm = VENTURES[venture_key]["fit_matrix"]

    for r_from, r_to in [(1, 2), (2, 3)]:
        if not configs[r_from] or not configs[r_to]:
            continue
        for lever in ["revenue", "pricing", "channel", "segment"]:
            if configs[r_from][lever] != configs[r_to][lever]:
                total_changes += 1
                old_fit = fm[lever].get(configs[r_from][lever], 0.5)
                new_fit = fm[lever].get(configs[r_to][lever], 0.5)
                if new_fit > old_fit:
                    good_changes += 1
                else:
                    bad_changes += 1

    if total_changes > 0:
        iteration_pts = 35 * (good_changes / total_changes)
    else:
        # No changes at all: partial credit if already good
        iteration_pts = 35 * fits[0] * 0.5

    # 3. Founder Focus (25 pts)
    focus_scores = []
    for r_from, r_to in [(1, 2), (2, 3)]:
        if not configs[r_from] or not configs[r_to]:
            focus_scores.append(0.5)
            continue
        n_changes = sum(
            1 for lever in ["revenue", "pricing", "channel", "segment"]
            if configs[r_from][lever] != configs[r_to][lever]
        )
        if n_changes == 0:
            focus_scores.append(0.6)
        elif n_changes == 1:
            focus_scores.append(1.0)
        elif n_changes == 2:
            focus_scores.append(0.85)
        elif n_changes == 3:
            focus_scores.append(0.45)
        else:
            focus_scores.append(0.20)

    focus_pts = 25 * (sum(focus_scores) / max(len(focus_scores), 1))

    total = min(100, round(final_fit_pts + iteration_pts + focus_pts))

    return {
        "total": total,
        "final_fit": round(final_fit_pts),
        "iteration": round(iteration_pts),
        "focus": round(focus_pts),
        "fits": fits,
        "total_changes": total_changes,
        "good_changes": good_changes,
        "bad_changes": bad_changes,
    }


def get_grade(score):
    if score >= 90:
        return "A", "Exceptional Founder Instincts"
    elif score >= 80:
        return "A-", "Strong Market Reader"
    elif score >= 70:
        return "B+", "Solid Iteration Skills"
    elif score >= 60:
        return "B", "Good Foundation"
    elif score >= 50:
        return "B-", "Building Your Instincts"
    else:
        return "C+", "Room to Grow"


def get_badges(scores, configs, venture_key):
    """Generate achievement badges based on performance."""
    badges = []
    fits = scores["fits"]

    if scores["total"] >= 85:
        badges.append(("🏆", "Model Master", "Achieved 85+ overall score"))
    if fits[2] >= 0.85:
        badges.append(("🎯", "Product Market Fit", "Final model fit score above 85%"))
    if len(fits) >= 2 and fits[1] - fits[0] >= 0.20:
        badges.append(("📈", "Quick Learner", "Improved fit by 20+ points in a single round"))
    if scores["good_changes"] > 0 and scores["bad_changes"] == 0:
        badges.append(("🧭", "Signal Reader", "Every change you made improved your model"))
    if scores["total_changes"] > 0 and scores["total_changes"] <= 4:
        badges.append(("🔬", "Lean Founder", "Made focused, disciplined changes"))
    if fits[0] >= 0.80:
        badges.append(("💡", "Natural Instinct", "Strong model fit from round one"))

    return badges


def generate_coaching(scores, configs, venture_key):
    """Generate personalized coaching notes."""
    notes = []
    fits = scores["fits"]
    v = VENTURES[venture_key]
    fm = v["fit_matrix"]
    optimal = v["optimal"]

    # Overall tier
    if scores["total"] >= 80:
        notes.append(
            "You demonstrated strong founder instincts in this simulation. "
            "You read market signals effectively and made focused, strategic changes. "
            "This ability to iterate based on evidence is what separates founders who find fit from those who run out of runway."
        )
    elif scores["total"] >= 60:
        notes.append(
            "You showed good instincts but left some value on the table. "
            "The signals were there in the customer feedback, and with sharper interpretation, "
            "you could have converged faster on the right model."
        )
    else:
        notes.append(
            "Finding business model fit is one of the hardest things a founder does, and this simulation "
            "shows why: the market gives you signals, but reading them correctly takes practice. "
            "The good news? This is a learnable skill."
        )

    # Iteration pattern
    if scores["total_changes"] == 0:
        notes.append(
            "You stuck with your initial model across all three rounds. "
            "While conviction is valuable, the best founders balance conviction with responsiveness. "
            "The customer feedback each round contained signals about what to adjust."
        )
    elif scores["total_changes"] >= 6:
        notes.append(
            "You made a lot of changes across rounds. Real founders call this 'thrashing': "
            "changing too many things at once makes it impossible to know what is working. "
            "Try changing just one or two levers per round so you can isolate what the market is telling you."
        )
    elif scores["bad_changes"] > scores["good_changes"]:
        notes.append(
            "Some of your changes moved away from what the market wanted. "
            "Reread the customer quotes from each round: the feedback often points directly at which lever to adjust. "
            "The key is distinguishing what customers are telling you about the MODEL vs. the PRODUCT."
        )

    # Specific lever insights
    final_config = configs[3] or configs[2] or configs[1]
    if final_config:
        weakest = min(
            ["revenue", "pricing", "channel", "segment"],
            key=lambda l: fm[l].get(final_config.get(l, ""), 0.5)
        )
        notes.append(
            f"Your biggest opportunity was in your {v['levers'][weakest]['label'].lower()} choice. "
            f"{v['optimal_explanations'][weakest]}"
        )

    return notes


# =============================================================================
# STEPPER (round progress indicator)
# =============================================================================
def render_stepper(active_round, show_results=False):
    steps = []
    for r in [1, 2, 3]:
        if r < active_round or (r == active_round and show_results):
            bg, color, border = "#6366f1", "#fff", "#6366f1"
        elif r == active_round:
            bg, color, border = "#ede9fe", "#6366f1", "#6366f1"
        else:
            bg, color, border = "#f1f5f9", "#94a3b8", "#e2e8f0"

        label = f"Round {r}"
        steps.append(
            f"<div style='flex:1;text-align:center;padding:10px 8px;background:{bg};"
            f"color:{color};border:2px solid {border};border-radius:8px;"
            f"font-weight:600;font-size:0.9rem;'>{label}</div>"
        )

    spacer = "<div style='width:8px;'></div>"
    html = f"<div style='display:flex;gap:0;margin-bottom:1.5rem;'>{spacer.join(steps)}</div>"
    st.markdown(html, unsafe_allow_html=True)


# =============================================================================
# FIT GAUGE
# =============================================================================
def render_fit_gauge(fit_score, label="Business Model Fit"):
    pct = int(fit_score * 100)
    if pct >= 75:
        bar_color = "#16a34a"
    elif pct >= 50:
        bar_color = "#d97706"
    else:
        bar_color = "#dc2626"

    html = f"""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin-bottom:1rem;">
        <div style="font-size:0.85rem;color:#64748b;margin-bottom:6px;">{label}</div>
        <div style="font-size:2.5rem;font-weight:700;color:{bar_color};">{pct}<span style="font-size:1.2rem;color:#94a3b8;">/100</span></div>
        <div style="background:#e2e8f0;border-radius:999px;height:12px;margin-top:8px;overflow:hidden;">
            <div style="background:{bar_color};height:100%;width:{pct}%;border-radius:999px;transition:width 0.5s ease;"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================
def render_footer():
    st.markdown(
        "<div style='text-align:center;color:#888;font-size:13px;margin-top:2rem;'>"
        "An Interactive Simulation"
        "</div>",
        unsafe_allow_html=True,
    )


# =============================================================================
# SCREEN: INTRO
# =============================================================================
def screen_intro():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%);
                    padding:3rem 2.5rem;border-radius:16px;color:#fff;text-align:center;margin-bottom:2rem;">
            <div style="font-size:3rem;margin-bottom:0.5rem;">🧠</div>
            <h1 style="margin:0;font-size:2.2rem;">Business Model Fit</h1>
            <p style="opacity:0.9;font-size:1.1rem;margin-top:0.75rem;">An Interactive Simulation</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:2rem;margin-bottom:1.5rem;">
            <h3 style="margin-top:0;color:#1e1b4b;">How This Works</h3>
            <p style="color:#334155;line-height:1.7;">
                A great product is not enough. You also need the right <strong>business model</strong>:
                how you make money, what you charge, how customers find you, and who you sell to first.
            </p>
            <p style="color:#334155;line-height:1.7;">
                In this simulation, you will run a startup through <strong>3 rounds</strong> of real market testing.
                Each round, you will set your business model, see how the market responds, read customer feedback,
                and decide what to change.
            </p>
            <p style="color:#334155;line-height:1.7;">
                <strong>Your goal:</strong> Find the business model that fits your market.
                The best founders do not guess: they iterate, read signals, and adapt.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#ede9fe;border-radius:12px;padding:1.25rem;margin-bottom:2rem;">
            <p style="color:#4c1d95;margin:0;font-size:0.95rem;">
                <strong>You will be scored on:</strong> Your final model fit, how smartly you iterated,
                and whether you stayed focused or changed too many things at once.
            </p>
            <p style="color:#6d28d9;margin:0.75rem 0 0 0;font-size:0.88rem;">
                23 Takes about 8 to 10 minutes to complete.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Choose Your Venture  →", use_container_width=True, type="primary"):
            go("choose")
            st.rerun()

        render_footer()


# =============================================================================
# SCREEN: CHOOSE VENTURE
# =============================================================================
def screen_choose():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center;margin-bottom:2rem;">
            <h2 style="color:#1e1b4b;margin-bottom:0.25rem;">Pick Your Startup</h2>
            <p style="color:#64748b;">Each venture has a different optimal business model. Choose the one that excites you.</p>
        </div>
        """, unsafe_allow_html=True)

        for key, v in VENTURES.items():
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">
                <div style="font-size:1.8rem;margin-bottom:0.25rem;">{v['emoji']}</div>
                <h3 style="margin:0 0 0.25rem 0;color:#1e1b4b;">{v['title']}</h3>
                <p style="color:#6366f1;font-weight:600;margin:0 0 0.75rem 0;font-size:0.95rem;">{v['one_liner']}</p>
                <p style="color:#475569;line-height:1.6;margin:0;font-size:0.93rem;">{v['hook']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Launch {v['title']}  →", key=f"pick_{key}", use_container_width=True):
                st.session_state.venture_key = key
                go("config")
                st.rerun()

        render_footer()


# =============================================================================
# SCREEN: CONFIGURE MODEL
# =============================================================================
def screen_config():
    vk = st.session_state.venture_key
    v = VENTURES[vk]
    rnd = st.session_state.current_round

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        render_stepper(rnd)

        round_titles = {
            1: ("Soft Launch", "Set your initial business model. Make your best guesses and see how the market responds."),
            2: ("Growth Push", "Review what the market told you last round. Adjust your model and push harder."),
            3: ("Scale Decision", "Final round. Lock in the model you believe fits this market best."),
        }
        title, subtitle = round_titles[rnd]

        st.markdown(f"""
        <div style="margin-bottom:1.5rem;">
            <h2 style="color:#1e1b4b;margin-bottom:0.25rem;">Round {rnd}: {title}</h2>
            <p style="color:#64748b;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

        # Show previous results summary for rounds 2+
        if rnd > 1:
            prev_fit = st.session_state.fit_history[-1] if st.session_state.fit_history else 0
            prev_pct = int(prev_fit * 100)
            fit_color = "#16a34a" if prev_pct >= 70 else "#d97706" if prev_pct >= 45 else "#dc2626"
            st.markdown(f"""
            <div style="background:#ede9fe;border:1px solid #c4b5fd;border-radius:10px;padding:1rem;margin-bottom:1.5rem;">
                <span style="color:#4c1d95;font-weight:600;">Last Round Fit Score:</span>
                <span style="color:{fit_color};font-weight:700;font-size:1.2rem;margin-left:8px;">{prev_pct}/100</span>
                <span style="color:#64748b;margin-left:8px;font-size:0.9rem;">Read the customer feedback below to guide your changes.</span>
            </div>
            """, unsafe_allow_html=True)

            # Show previous round's customer quotes as reference (expanded so students read them)
            prev_results = st.session_state.results_cache.get(rnd - 1)
            if prev_results and prev_results.get("quotes"):
                st.markdown(f"""
                <div style="background:#fefce8;border:1px solid #fde68a;border-radius:10px;padding:0.75rem 1rem;margin-bottom:0.5rem;">
                    <span style="font-weight:600;color:#92400e;">💬 Customer Feedback from Round {rnd - 1}</span>
                    <span style="color:#a16207;font-size:0.85rem;"> (Use this to guide your changes!)</span>
                </div>
                """, unsafe_allow_html=True)
                for q in prev_results["quotes"]:
                    if q["signal"] == "strong":
                        border, bg, icon = "#16a34a", "#f0fdf4", "🟢"
                    elif q["signal"] == "weak":
                        border, bg, icon = "#d97706", "#fffbeb", "🟡"
                    else:
                        border, bg, icon = "#dc2626", "#fef2f2", "🔴"
                    st.markdown(f"""
                    <div style="border-left:4px solid {border};background:{bg};padding:0.6rem 1rem;
                                border-radius:0 8px 8px 0;margin-bottom:0.5rem;">
                        <span style="font-size:0.85rem;">{icon}</span>
                        <span style="color:#334155;font-style:italic;font-size:0.93rem;"> \"{q['text']}\"</span>
                    </div>
                    """, unsafe_allow_html=True)

        # Get previous config as defaults
        prev_config = st.session_state.configs.get(rnd - 1, None) if rnd > 1 else None

        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
            <div style="font-size:1.3rem;margin-bottom:0.25rem;">{v['emoji']} {v['title']}</div>
            <div style="color:#64748b;font-size:0.9rem;">{v['one_liner']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Show current model summary for rounds 2+ so students can see what to change
        if rnd > 1 and prev_config:
            model_pills = ""
            for lever in ["revenue", "pricing", "channel", "segment"]:
                lever_label = v["levers"][lever]["label"]
                choice_label = v["levers"][lever]["options"][prev_config[lever]]["label"]
                model_pills += (
                    f"<span style='display:inline-block;background:#e0e7ff;border:1px solid #c7d2fe;"
                    f"border-radius:16px;padding:4px 12px;margin:3px;font-size:0.82rem;color:#3730a3;'>"
                    f"{lever_label}: <strong>{choice_label}</strong></span>"
                )
            st.markdown(f"""
            <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:1rem;margin-bottom:1.5rem;">
                <div style="font-size:0.85rem;color:#0369a1;font-weight:600;margin-bottom:6px;">
                    📋 Your Current Model (from Round {rnd - 1})
                </div>
                <div>{model_pills}</div>
                <div style="font-size:0.8rem;color:#0c4a6e;margin-top:8px;">
                    Tip: Focus on changing 1 or 2 levers based on customer feedback. Changing everything at once makes it hard to learn what works.
                </div>
            </div>
            """, unsafe_allow_html=True)

        config = {}
        left, right = st.columns(2)

        lever_order = ["revenue", "pricing", "channel", "segment"]
        cols = [left, right, left, right]

        for i, lever in enumerate(lever_order):
            info = v["levers"][lever]
            with cols[i]:
                st.markdown(f"**{info['label']}**")
                st.caption(info["description"])

                options = list(info["options"].keys())
                labels = [info["options"][o]["label"] for o in options]

                # Set default to previous config if available
                default_idx = 0
                if prev_config and prev_config.get(lever) in options:
                    default_idx = options.index(prev_config[lever])

                selected_label = st.radio(
                    info["label"],
                    labels,
                    index=default_idx,
                    key=f"r{rnd}_{lever}",
                    label_visibility="collapsed",
                )
                selected_key = options[labels.index(selected_label)]
                config[lever] = selected_key

                # Show description of selected option
                desc = info["options"][selected_key]["desc"]
                st.markdown(
                    f"<div style='color:#64748b;font-size:0.82rem;margin-top:-8px;margin-bottom:1rem;'>{desc}</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:1px;background:#e5e7eb;margin:1rem 0;'></div>", unsafe_allow_html=True)

        if st.button(f"🚀  Launch Round {rnd}", use_container_width=True, type="primary"):
            st.session_state.configs[rnd] = config
            fit = compute_fit(config, vk)
            st.session_state.fit_history.append(fit)

            random.seed(rnd * 1000 + hash(str(config)) % 10000)
            metrics = generate_metrics(fit, vk, rnd)
            quotes = select_quotes(config, vk, rnd)
            event = v["market_events"].get(rnd, None)

            st.session_state.results_cache[rnd] = {
                "fit": fit,
                "metrics": metrics,
                "quotes": quotes,
                "event": event,
            }
            go("results")
            st.rerun()

        render_footer()


# =============================================================================
# SCREEN: ROUND RESULTS
# =============================================================================
def screen_results():
    vk = st.session_state.venture_key
    v = VENTURES[vk]
    rnd = st.session_state.current_round
    res = st.session_state.results_cache[rnd]
    fit = res["fit"]
    metrics = res["metrics"]

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        render_stepper(rnd, show_results=True)

        round_titles = {1: "Soft Launch Results", 2: "Growth Push Results", 3: "Final Round Results"}
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:1rem;">
            <h2 style="color:#1e1b4b;margin-bottom:0.25rem;">Round {rnd}: {round_titles[rnd]}</h2>
            <p style="color:#64748b;">{v['emoji']} {v['title']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Fit gauge
        render_fit_gauge(fit)

        # Trend arrow for rounds 2+
        if rnd > 1 and len(st.session_state.fit_history) >= 2:
            prev_pct = int(st.session_state.fit_history[-2] * 100)
            curr_pct = int(fit * 100)
            delta = curr_pct - prev_pct
            if delta > 0:
                trend_html = f"<span style='color:#16a34a;font-weight:600;'>▲ +{delta} points from last round</span>"
            elif delta < 0:
                trend_html = f"<span style='color:#dc2626;font-weight:600;'>▼ {delta} points from last round</span>"
            else:
                trend_html = "<span style='color:#64748b;font-weight:600;'>No change from last round</span>"
            st.markdown(f"<div style='text-align:center;margin-bottom:1.5rem;'>{trend_html}</div>", unsafe_allow_html=True)

        # Key metrics
        st.markdown("""
        <div style="font-weight:600;color:#1e1b4b;margin-bottom:0.5rem;">📊 Key Metrics</div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Signups", f"{metrics['signups']:,}")
        m2.metric("Active Users", f"{metrics['active_users']:,}")
        m3.metric("Revenue", f"${metrics['revenue']:,}")
        m4.metric("Retention", f"{metrics['retention']}%")

        # Customer quotes
        st.markdown("""<div style="font-weight:600;color:#1e1b4b;margin-bottom:0.75rem;margin-top:1.5rem;">💬 What Customers Are Saying</div>""", unsafe_allow_html=True)

        quotes = res.get("quotes", [])
        for q in quotes:
            if q["signal"] == "strong":
                border, bg, icon = "#16a34a", "#f0fdf4", "🟢"
            elif q["signal"] == "weak":
                border, bg, icon = "#d97706", "#fffbeb", "🟡"
            else:
                border, bg, icon = "#dc2626", "#fef2f2", "🔴"

            st.markdown(f"""
            <div style="border-left:4px solid {border};background:{bg};padding:0.75rem 1rem;
                        border-radius:0 8px 8px 0;margin-bottom:0.75rem;">
                <span style="font-size:0.85rem;">{icon}</span>
                <span style="color:#334155;font-style:italic;font-size:0.95rem;"> \"{q['text']}\"</span>
            </div>
            """, unsafe_allow_html=True)

        # Market event
        event = res.get("event")
        if event:
            st.markdown(f"""
            <div style="background:#fef3c7;border:1px solid #fbbf24;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
                <div style="font-weight:600;color:#92400e;margin-bottom:0.5rem;">📰 Market News</div>
                <div style="color:#78350f;font-size:0.95rem;line-height:1.6;">{event}</div>
            </div>
            """, unsafe_allow_html=True)

        # Current model summary
        config = st.session_state.configs[rnd]
        model_rows = ""
        for lever in ["revenue", "pricing", "channel", "segment"]:
            label = v["levers"][lever]["label"]
            choice = v["levers"][lever]["options"][config[lever]]["label"]
            model_rows += f"<div style='padding:4px 0;'><strong>{label}:</strong> {choice}</div>"

        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#1e1b4b;margin-bottom:0.75rem;">🧠 Your Current Model</div>
            {model_rows}
        </div>
        """, unsafe_allow_html=True)

        # Next button
        if rnd < 3:
            if st.button(f"Continue to Round {rnd + 1}  →", use_container_width=True, type="primary"):
                st.session_state.current_round = rnd + 1
                go("config")
                st.rerun()
        else:
            if st.button("See Your Final Score  →", use_container_width=True, type="primary"):
                go("email")
                st.rerun()

        render_footer()


# =============================================================================
# SCREEN: EMAIL CAPTURE
# =============================================================================
def screen_email():
    vk = st.session_state.venture_key
    v = VENTURES[vk]
    # Compute a teaser score
    scores = compute_final_scores(vk)
    grade, grade_label = get_grade(scores["total"])
    score_color = "#16a34a" if scores["total"] >= 70 else "#d97706" if scores["total"] >= 50 else "#dc2626"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
                    padding:2.5rem;border-radius:16px;color:#fff;text-align:center;margin-bottom:2rem;">
            <div style="font-size:0.9rem;opacity:0.8;margin-bottom:0.5rem;">SIMULATION COMPLETE</div>
            <div style="font-size:4rem;font-weight:800;color:{score_color};line-height:1;">{scores['total']}</div>
            <div style="font-size:1rem;margin-top:0.5rem;opacity:0.9;">
                Grade: {grade} ({grade_label})
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:2rem;text-align:center;margin-bottom:1.5rem;">
            <h3 style="color:#1e1b4b;margin-top:0;">Unlock Your Full Results</h3>
            <p style="color:#475569;line-height:1.7;">
                See your detailed score breakdown, discover the optimal business model,
                get personalized coaching insights, and earn achievement badges.
            </p>
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input(
            "Enter your email to see your full results",
            placeholder="you@example.com",
            key="email_input",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("See My Results  →", use_container_width=True, type="primary"):
                if email and "@" in email and "." in email:
                    st.session_state.email = email
                    go("debrief")
                    st.rerun()
                else:
                    st.warning("Please enter a valid email address.")
        with col_b:
            if st.button("Skip for now", use_container_width=True):
                st.session_state.email_skipped = True
                go("debrief")
                st.rerun()

        render_footer()


# =============================================================================
# SCREEN: DEBRIEF
# =============================================================================
def screen_debrief():
    vk = st.session_state.venture_key
    v = VENTURES[vk]
    scores = compute_final_scores(vk)
    grade, grade_label = get_grade(scores["total"])
    badges = get_badges(scores, st.session_state.configs, vk)
    coaching = generate_coaching(scores, st.session_state.configs, vk)

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        # Hero score card
        score_color = "#16a34a" if scores["total"] >= 70 else "#d97706" if scores["total"] >= 50 else "#dc2626"
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
                    padding:2.5rem;border-radius:16px;color:#fff;text-align:center;margin-bottom:2rem;">
            <div style="font-size:0.9rem;opacity:0.8;margin-bottom:0.5rem;">YOUR BUSINESS MODEL FIT SCORE</div>
            <div style="font-size:4.5rem;font-weight:800;color:{score_color};line-height:1;">{scores['total']}</div>
            <div style="font-size:1.1rem;margin-top:0.5rem;">
                <span style="background:{score_color};padding:4px 16px;border-radius:20px;font-weight:600;">
                    Grade: {grade} ({grade_label})
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Badges
        if badges:
            badge_html = " ".join(
                f"<span style='display:inline-block;background:#ede9fe;border:1px solid #c4b5fd;"
                f"border-radius:20px;padding:6px 14px;margin:4px;font-size:0.85rem;'>"
                f"{b[0]} <strong>{b[1]}</strong></span>"
                for b in badges
            )
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:2rem;">
                <div style="font-size:0.85rem;color:#64748b;margin-bottom:8px;">Achievements Earned</div>
                {badge_html}
            </div>
            """, unsafe_allow_html=True)

        # Fit progression chart (single HTML block)
        fits = scores["fits"]
        progression_rows = ""
        for r in range(3):
            pct = int(fits[r] * 100)
            bar_color = "#16a34a" if pct >= 70 else "#d97706" if pct >= 45 else "#dc2626"
            progression_rows += f"""
            <div style="display:flex;align-items:center;margin-bottom:8px;">
                <div style="width:80px;font-weight:600;color:#475569;font-size:0.9rem;">Round {r+1}</div>
                <div style="flex:1;background:#e2e8f0;border-radius:999px;height:20px;overflow:hidden;margin-right:12px;">
                    <div style="background:{bar_color};height:100%;width:{pct}%;border-radius:999px;
                                transition:width 0.5s ease;"></div>
                </div>
                <div style="width:50px;text-align:right;font-weight:700;color:{bar_color};">{pct}</div>
            </div>"""

        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#1e1b4b;margin-bottom:0.75rem;">📈 Your Fit Score Progression</div>
            {progression_rows}
        </div>
        """, unsafe_allow_html=True)

        # Score breakdown (single HTML block)
        breakdown = [
            ("Final Model Fit", scores["final_fit"], 40,
             "How close your Round 3 model was to the optimal configuration."),
            ("Iteration Quality", scores["iteration"], 35,
             f"You made {scores['total_changes']} changes: {scores['good_changes']} improved fit, {scores['bad_changes']} did not."),
            ("Founder Focus", scores["focus"], 25,
             "Focused founders change 1 or 2 levers per round, not everything at once."),
        ]

        breakdown_rows = ""
        for name, pts, max_pts, explanation in breakdown:
            pct = int((pts / max_pts) * 100) if max_pts > 0 else 0
            bar_color = "#6366f1"
            breakdown_rows += f"""
            <div style="margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;">
                    <div style="font-weight:600;color:#334155;font-size:0.95rem;">{name}</div>
                    <div style="font-weight:700;color:#6366f1;">{pts}/{max_pts}</div>
                </div>
                <div style="background:#e2e8f0;border-radius:999px;height:8px;margin:6px 0;overflow:hidden;">
                    <div style="background:{bar_color};height:100%;width:{pct}%;border-radius:999px;"></div>
                </div>
                <div style="color:#64748b;font-size:0.82rem;">{explanation}</div>
            </div>"""

        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#1e1b4b;margin-bottom:0.75rem;">🏁 Score Breakdown</div>
            {breakdown_rows}
        </div>
        """, unsafe_allow_html=True)

        # Optimal model reveal
        optimal = v["optimal"]
        final_config = st.session_state.configs[3] or st.session_state.configs[2] or st.session_state.configs[1]

        # Build optimal model reveal as single HTML block
        reveal_rows = ""
        for lever in ["revenue", "pricing", "channel", "segment"]:
            lever_label = v["levers"][lever]["label"]
            optimal_val = optimal[lever]
            your_val = final_config[lever] if final_config else ""
            optimal_label = v["levers"][lever]["options"][optimal_val]["label"]
            your_label = v["levers"][lever]["options"].get(your_val, {}).get("label", "N/A") if your_val else "N/A"
            match = "✅" if your_val == optimal_val else "❌"
            match_bg = "#f0fdf4" if your_val == optimal_val else "#fef2f2"
            reveal_rows += f"""
            <div style="background:{match_bg};border-radius:8px;padding:0.75rem 1rem;margin-bottom:0.5rem;">
                <div style="font-weight:600;color:#334155;">{match} {lever_label}</div>
                <div style="font-size:0.9rem;color:#475569;margin-top:4px;">
                    Optimal: <strong>{optimal_label}</strong>
                    &nbsp;&nbsp;|&nbsp;&nbsp; Yours: <strong>{your_label}</strong>
                </div>
            </div>"""

        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#1e1b4b;margin-bottom:0.75rem;">🔑 The Optimal Model (Revealed)</div>
            {reveal_rows}
        </div>
        """, unsafe_allow_html=True)

        # Why it works (single HTML block)
        why_rows = ""
        for lever in ["revenue", "pricing", "channel", "segment"]:
            explanation = v["optimal_explanations"][lever]
            lever_label = v["levers"][lever]["label"]
            why_rows += f"<p style='color:#475569;line-height:1.6;'><strong>{lever_label}:</strong> {explanation}</p>"

        st.markdown(f"""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#1e1b4b;margin-bottom:0.75rem;">💡 Why This Model Works</div>
            {why_rows}
        </div>
        """, unsafe_allow_html=True)

        # Coaching (single HTML block)
        coaching_html = ""
        for note in coaching:
            coaching_html += f"<p style='color:#4c1d95;line-height:1.7;font-size:0.95rem;'>{note}</p>"

        st.markdown(f"""
        <div style="background:#ede9fe;border:1px solid #c4b5fd;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#4c1d95;margin-bottom:0.75rem;">🎓 Personalized Coaching</div>
            {coaching_html}
        </div>
        """, unsafe_allow_html=True)

        # Founder insight (replaces fake peer comparison)
        if scores["total_changes"] == 0:
            insight = "You kept your model unchanged across all rounds. Real founders balance conviction with curiosity. Try adjusting one lever next time to see how the market reacts differently."
        elif scores["total_changes"] <= 4 and scores["good_changes"] > scores["bad_changes"]:
            insight = "You showed real founder discipline: making focused changes and reading market signals carefully. This is exactly how the best startups iterate toward product market fit."
        elif scores["total_changes"] >= 6:
            insight = "You changed a lot between rounds. In the real world, this is called 'thrashing.' The best founders test one or two changes at a time so they can isolate what is working."
        elif scores["bad_changes"] > scores["good_changes"]:
            insight = "Some of your changes moved away from what the market wanted. The customer quotes each round contain directional hints. Try rereading them more carefully next time."
        else:
            insight = "You iterated thoughtfully across rounds. With more practice reading customer signals, you will converge on the right model even faster."

        st.markdown(f"""
        <div style="background:#f1f5f9;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#334155;margin-bottom:0.75rem;">🧠 Founder Insight</div>
            <div style="color:#475569;line-height:1.7;font-size:0.95rem;">{insight}</div>
        </div>
        """, unsafe_allow_html=True)
        col_play1, col_play2 = st.columns(2)
        with col_play1:
            if st.button("🔄  Try a Different Venture", use_container_width=True):
                email_backup = st.session_state.get("email")
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                init_state()
                if email_backup:
                    st.session_state.email = email_backup
                go("choose")
                st.rerun()
        with col_play2:
            if st.button("🔁  Replay This Venture", use_container_width=True):
                vk_backup = st.session_state.venture_key
                email_backup = st.session_state.get("email")
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                init_state()
                st.session_state.venture_key = vk_backup
                if email_backup:
                    st.session_state.email = email_backup
                go("config")
                st.rerun()

        render_footer()


# =============================================================================
# MAIN ROUTER
# =============================================================================
stage = st.session_state.stage

if stage == "intro":
    screen_intro()
elif stage == "choose":
    screen_choose()
elif stage == "config":
    screen_config()
elif stage == "results":
    screen_results()
elif stage == "email":
    screen_email()
elif stage == "debrief":
    screen_debrief()
else:
    screen_intro()
