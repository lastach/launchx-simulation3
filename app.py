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
    "thermaloop": {
        "title": "ThermaLoop",
        "emoji": "🌬️",
        "one_liner": "Smart ventilation retrofit kits for older homes",
        "hook": (
            "Homes built before 2005 leak heat, trap stale air, and waste 20 to 40 percent of their energy. "
            "ThermaLoop is a smart ventilation retrofit kit that installs in a single afternoon and pays "
            "for itself in a couple of winters. The product works. Your challenge: figure out the "
            "business model that turns a great product into a real business."
        ),
        "levers": {
            "revenue": {
                "label": "Revenue Model",
                "description": "How does ThermaLoop make money?",
                "options": {
                    "hardware_only": {"label": "Hardware Only", "desc": "One time kit sale. Customer owns it, installs it, done. Classic product model."},
                    "hardware_plus_service": {"label": "Hardware + Monitoring", "desc": "Kit sale plus a monthly monitoring subscription (air quality, energy reports, alerts)."},
                    "saas_only": {"label": "Install Free, Monthly Fee", "desc": "Free or heavily subsidized install. All revenue from recurring monthly service."},
                    "install_partner": {"label": "Installer Network", "desc": "Certified HVAC contractors install and keep 60 percent. ThermaLoop takes a cut on each job."},
                },
            },
            "pricing": {
                "label": "Price Point",
                "description": "What does a customer pay?",
                "options": {
                    "low": {"label": "$399 kit + $9/mo", "desc": "Aggressive price. Drives adoption but thin margins."},
                    "mid": {"label": "$599 kit + $15/mo", "desc": "Payback in 2 to 3 winters. Sustainable margins."},
                    "high": {"label": "$899 kit + $25/mo", "desc": "Premium positioning. May feel expensive to budget buyers."},
                    "subscription_only": {"label": "$49/mo all in", "desc": "No upfront cost. Long payback period for ThermaLoop."},
                },
            },
            "channel": {
                "label": "Go to Market Channel",
                "description": "How do customers discover ThermaLoop?",
                "options": {
                    "direct_online": {"label": "Direct to Consumer Online", "desc": "Website, Amazon, paid ads. Homeowners find you and self install."},
                    "contractors": {"label": "HVAC Contractor Network", "desc": "Train and certify local HVAC pros. They recommend ThermaLoop on service calls."},
                    "utility": {"label": "Utility Rebate Partnerships", "desc": "Partner with energy utilities. Rebates built into the sale."},
                    "big_box": {"label": "Home Depot / Lowes", "desc": "Retail shelf space, in store demos, DIY weekend warriors."},
                },
            },
            "segment": {
                "label": "Target Customer",
                "description": "Who is ThermaLoop for first?",
                "options": {
                    "diy_homeowners": {"label": "DIY Homeowners", "desc": "Tinkerers who install their own thermostats and read energy blogs."},
                    "older_homes": {"label": "Owners of 30+ Year Old Homes", "desc": "Pain is real. Drafty rooms, high bills, no renovation budget for a full HVAC overhaul."},
                    "landlords": {"label": "Small Landlords", "desc": "Own 2 to 20 units. Want tenant comfort without full renovations."},
                    "commercial": {"label": "Small Commercial Buildings", "desc": "Offices, corner stores, small warehouses. Complex sales cycle but higher ticket."},
                },
            },
        },
        "fit_matrix": {
            "revenue": {"hardware_plus_service": 1.0, "install_partner": 0.60, "hardware_only": 0.45, "saas_only": 0.25},
            "pricing": {"mid": 1.0, "low": 0.55, "high": 0.40, "subscription_only": 0.30},
            "channel": {"contractors": 1.0, "utility": 0.70, "big_box": 0.50, "direct_online": 0.35},
            "segment": {"older_homes": 1.0, "landlords": 0.65, "diy_homeowners": 0.50, "commercial": 0.30},
        },
        "optimal": {"revenue": "hardware_plus_service", "pricing": "mid", "channel": "contractors", "segment": "older_homes"},
        "optimal_explanations": {
            "revenue": "Hardware plus monitoring is the strongest model. The kit covers COGS and install labor. The monthly service creates recurring revenue, gives you a reason to collect data, and improves retention because customers see ongoing value in their energy reports.",
            "pricing": "$599 plus $15 per month is the sweet spot. The kit pays back in two or three winters for most older homes. Lower prices erode margin and don't change demand much. Higher prices push buyers to wait for a full HVAC replacement.",
            "channel": "HVAC contractors are the best channel for retrofits. They're already in older homes, already trusted, and already selling. A certified installer network gives you local credibility and turns sales conversations into same day installs.",
            "segment": "Owners of 30+ year old homes feel the pain daily: cold rooms, noisy furnaces, energy bills climbing every year. They're not DIY hobbyists, they're motivated buyers. Start here and expand to landlords and commercial later.",
        },
        "base_metrics": {"signups": 60, "active_rate": 0.45, "revenue_per_active": 20, "retention": 0.50},
        "market_events": {
            2: "The federal Inflation Reduction Act expanded home energy tax credits. Homeowners are searching for qualifying retrofits and calling their HVAC contractors.",
            3: "A competitor just raised $8M Series A and is offering zero percent financing. Your prospects are asking if you will match.",
        },
    },
}


# =============================================================================
# UNIT ECONOMICS PARAMETERS
# Each lever choice maps to dollar/percent values that feed a real unit-
# economics calculation. Learners see computed CAC, margin, LTV, payback,
# and LTV:CAC live as they toggle their business-model choices.
# =============================================================================
UNIT_ECON_PARAMS = {
    "thermaloop": {
        "pricing": {
            "low":               {"upfront": 399, "monthly":  9, "gross_margin_base": 0.42},
            "mid":               {"upfront": 599, "monthly": 15, "gross_margin_base": 0.55},
            "high":              {"upfront": 899, "monthly": 25, "gross_margin_base": 0.60},
            "subscription_only": {"upfront":   0, "monthly": 49, "gross_margin_base": 0.45},
        },
        "revenue": {
            # margin_adj applied to pricing GM; churn_monthly is the baseline.
            "hardware_only":          {"margin_adj":  0.05, "churn_monthly": 0.040},
            "hardware_plus_service":  {"margin_adj":  0.00, "churn_monthly": 0.020},
            "saas_only":              {"margin_adj": -0.08, "churn_monthly": 0.050},
            "install_partner":        {"margin_adj": -0.15, "churn_monthly": 0.015},
        },
        "channel": {
            "contractors":    {"cac":  80},
            "utility":        {"cac":  50},
            "direct_online":  {"cac": 180},
            "big_box":        {"cac": 120},
        },
        "segment": {
            "older_homes":     {"churn_adj":  0.000, "volume_index": 1.00},
            "landlords":       {"churn_adj": -0.005, "volume_index": 0.70},
            "diy_homeowners":  {"churn_adj":  0.030, "volume_index": 0.50},
            "commercial":      {"churn_adj": -0.010, "volume_index": 0.30},
        },
    },
}


def compute_unit_economics(config: dict, venture_key: str) -> dict:
    """Translate a lever config into concrete unit economics: CAC, margin,
    churn, LTV, payback, LTV:CAC. Deterministic — purely from the parameter
    table above. This is what makes the business-model simulation 'real':
    the learner sees dollar math, not a rubric score.
    """
    p = UNIT_ECON_PARAMS.get(venture_key)
    if not p:
        return {}
    pr = p["pricing"][config["pricing"]]
    rv = p["revenue"][config["revenue"]]
    ch = p["channel"][config["channel"]]
    seg = p["segment"][config["segment"]]

    upfront = pr["upfront"]
    monthly = pr["monthly"]
    gm = max(0.05, min(0.90, pr["gross_margin_base"] + rv["margin_adj"]))
    monthly_churn = max(0.005, min(0.30, rv["churn_monthly"] + seg["churn_adj"]))
    cac = ch["cac"]

    # Contribution dollars
    upfront_cm = upfront * gm
    monthly_cm = monthly * gm
    retention_months = 1 / monthly_churn if monthly_churn > 0 else 60

    # LTV = upfront CM + monthly CM × expected lifetime
    ltv = upfront_cm + monthly_cm * retention_months

    # Payback: first recover CAC from upfront CM, rest from monthly CM
    if monthly_cm > 0:
        if upfront_cm >= cac:
            payback_months = 0.0  # CAC recovered on first transaction
        else:
            payback_months = (cac - upfront_cm) / monthly_cm
    else:
        # No recurring revenue: payback depends on whether upfront CM exceeds CAC
        payback_months = 0.0 if upfront_cm >= cac else 999

    ltv_cac = ltv / cac if cac > 0 else 0

    return {
        "upfront_price":     upfront,
        "monthly_price":     monthly,
        "gross_margin":      gm,
        "monthly_churn":     monthly_churn,
        "retention_months":  retention_months,
        "cac":               cac,
        "upfront_cm":        upfront_cm,
        "monthly_cm":        monthly_cm,
        "ltv":               ltv,
        "ltv_cac":           ltv_cac,
        "payback_months":    payback_months,
        "volume_index":      seg["volume_index"],
    }


# =============================================================================
# CUSTOMER QUOTE POOLS
# Each quote: (lever, signal_direction, optimal_values, text)
# signal_direction: "positive" means the current choice is working
#                   "negative" means the current choice is not working
# =============================================================================
QUOTE_POOLS = {
    "thermaloop": {
        "revenue": [
            ("positive", ["hardware_plus_service"], "The monthly app showed me my bedroom was still leaking heat in month two. I never would have caught it without the monitoring."),
            ("negative", ["hardware_only"], "I installed the kit and then... nothing. I have no idea if it is actually working. I want data, not just a quiet fan."),
            ("negative", ["saas_only"], "Paying monthly forever for something bolted to my house feels wrong. I want to own it."),
            ("positive", ["install_partner"], "My HVAC guy installed it in a couple hours, signed me up for monitoring, and now he checks in every season. Easiest upgrade I have ever done."),
            ("negative", ["saas_only"], "If I ever stop paying, does the fan stop working? That is a really weird way to buy a home appliance."),
        ],
        "pricing": [
            ("positive", ["mid"], "Six hundred bucks plus fifteen a month to stop my drafty rooms? That is a fraction of what a full HVAC job quoted."),
            ("positive", ["low"], "At four hundred dollars, I did not even think about it. Best impulse purchase for my house this year."),
            ("negative", ["high"], "Nine hundred dollars plus twenty five a month is creeping into new furnace territory. I will just wait and replace the whole system."),
            ("negative", ["subscription_only"], "Forty nine a month forever? That is six hundred a year. I would rather pay upfront and own it."),
            ("positive", ["mid", "low"], "The math works out. Two winters of savings and this thing has paid for itself."),
        ],
        "channel": [
            ("positive", ["contractors"], "My HVAC tech mentioned ThermaLoop when he came out for a tune up. He said it was the easiest retrofit he had seen. Installed it the next week."),
            ("negative", ["direct_online"], "I saw an Instagram ad and almost bought, but I have no idea how to install it. Would I mess up my ducts? Too risky without a pro."),
            ("positive", ["utility"], "My utility sent a flyer about energy rebates and ThermaLoop was on the list. Knowing my power company vetted it gave me real confidence."),
            ("negative", ["big_box"], "I saw the box at Home Depot but the associate had never heard of it. I put it back and bought a smart thermostat instead."),
            ("positive", ["contractors"], "The certified installer gave me a quote on the spot and did it the same visit. That is the only reason I actually pulled the trigger."),
        ],
        "segment": [
            ("positive", ["older_homes"], "My house is from 1978. I have three rooms that are basically unusable in January. ThermaLoop fixed two of them in one day."),
            ("negative", ["diy_homeowners"], "I am handy and wanted to install it myself, but the install guide assumes a contractor is doing it. I returned it."),
            ("positive", ["landlords"], "I own four small rental houses, all built before 2000. Tenant complaints about drafts have dropped to zero. Huge retention win."),
            ("negative", ["commercial"], "We looked at it for our office but the sales cycle was six months and we needed a full commercial air handler anyway. Wrong fit for us."),
            ("positive", ["older_homes"], "Our 1960s house was leaking heat like a sieve. First winter with ThermaLoop, our gas bill dropped by a third."),
        ],
    },
}


# =============================================================================
# SESSION STATE
# =============================================================================
def init_state():
    defaults = {
        "stage": "intro",
        "venture_key": "thermaloop",
        "current_round": 1,
        "configs": {1: None, 2: None, 3: None},
        "results_cache": {1: None, 2: None, 3: None},
        "fit_history": [],
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

    # 1. Final Model Fit + Unit Economics (34 pts combined)
    # Half the weight on fit, half on whether the final config produces healthy unit econ.
    final_fit_pts = fits[2] * 17
    final_config = configs[3] or configs[2] or configs[1]
    if final_config:
        final_ue = compute_unit_economics(final_config, venture_key)
    else:
        final_ue = {}
    ue_score = 0.0
    if final_ue:
        # LTV:CAC component (0-1)
        lc = final_ue.get("ltv_cac", 0)
        if lc >= 3: lc_norm = 1.0
        elif lc >= 2: lc_norm = 0.75
        elif lc >= 1: lc_norm = 0.4
        else: lc_norm = 0.1 if lc > 0 else 0.0
        # Payback component (0-1)
        pb = final_ue.get("payback_months", 999)
        if pb == 0: pb_norm = 1.0
        elif pb < 12: pb_norm = 0.85
        elif pb < 24: pb_norm = 0.5
        elif pb < 999: pb_norm = 0.25
        else: pb_norm = 0.0
        ue_score = (lc_norm + pb_norm) / 2
    unit_econ_pts = ue_score * 17
    final_fit_pts = final_fit_pts + unit_econ_pts  # combined out of 34

    # 2. Iteration Quality (30 pts)
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
        iteration_pts = 30 * (good_changes / total_changes)
    else:
        # No changes at all: partial credit if already good
        iteration_pts = 30 * fits[0] * 0.5

    # 3. Founder Focus (21 pts)
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

    focus_pts = 21 * (sum(focus_scores) / max(len(focus_scores), 1))

    # 4. Strategic Narrative (15 pts)
    # Award points based on whether the founder can articulate why their choices made sense
    # For now, award full points if they made intentional changes (good_changes > 0)
    if total_changes > 0:
        narrative_pts = 15 * max(0.5, (good_changes / total_changes) * 0.9)
    else:
        narrative_pts = 15 * 0.6  # Some credit for sticking with initial choice

    total = min(100, round(final_fit_pts + iteration_pts + focus_pts + narrative_pts))

    return {
        "total": total,
        "final_fit": round(final_fit_pts),
        "iteration": round(iteration_pts),
        "focus": round(focus_pts),
        "narrative": round(narrative_pts),
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
                Takes about 8 to 10 minutes to complete.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Round 1  →", use_container_width=True, type="primary"):
            st.session_state.venture_key = "thermaloop"
            go("config")
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

        # ---- Live Unit Economics ----
        ue = compute_unit_economics(config, vk)
        if ue:
            ltv_cac_color = "#16a34a" if ue["ltv_cac"] >= 3 else "#d97706" if ue["ltv_cac"] >= 1 else "#dc2626"
            pb_color = ("#16a34a" if 0 <= ue["payback_months"] < 12
                        else "#d97706" if ue["payback_months"] < 24
                        else "#dc2626")
            churn_pct = ue["monthly_churn"] * 100
            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin:1rem 0;">
                <div style="font-weight:700;color:#1e1b4b;margin-bottom:0.5rem;">📐 Unit Economics at This Configuration</div>
                <div style="color:#64748b;font-size:0.85rem;margin-bottom:0.75rem;">
                    Computed from your pricing, revenue model, channel, and segment choices. Updates live.
                </div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.75rem;">
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">Upfront Price</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#1f2937;">${ue['upfront_price']:,.0f}</div>
                    </div>
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">Monthly Price</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#1f2937;">${ue['monthly_price']:,.0f}</div>
                    </div>
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">Gross Margin</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#1f2937;">{ue['gross_margin']*100:.0f}%</div>
                    </div>
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">CAC</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#1f2937;">${ue['cac']:,.0f}</div>
                    </div>
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">Monthly Churn</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#1f2937;">{churn_pct:.1f}%</div>
                    </div>
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">LTV</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#1f2937;">${ue['ltv']:,.0f}</div>
                    </div>
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">LTV : CAC</div>
                        <div style="font-size:1.1rem;font-weight:700;color:{ltv_cac_color};">{ue['ltv_cac']:.1f} : 1</div>
                    </div>
                    <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.75rem;">
                        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;">Payback</div>
                        <div style="font-size:1.1rem;font-weight:700;color:{pb_color};">
                            {("Immediate" if ue['payback_months'] == 0 else f"{ue['payback_months']:.1f} mo" if ue['payback_months'] < 999 else "Never")}
                        </div>
                    </div>
                </div>
                <div style="margin-top:0.75rem;font-size:0.83rem;color:#475569;">
                    <strong>Formulas:</strong> LTV = upfront contribution + monthly contribution × (1/churn). Payback = (CAC − upfront contribution) / monthly contribution. Healthy SaaS has LTV:CAC ≥ 3 and payback &lt; 12 months.
                </div>
            </div>
            """, unsafe_allow_html=True)

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

        # Final Unit Economics panel — what your Round 3 model produces
        final_cfg = st.session_state.configs.get(3) or st.session_state.configs.get(2) or st.session_state.configs.get(1)
        if final_cfg:
            fue = compute_unit_economics(final_cfg, vk)
            if fue:
                lc = fue.get("ltv_cac", 0)
                pb = fue.get("payback_months", 999)
                lc_color = "#16a34a" if lc >= 3 else "#d97706" if lc >= 1 else "#dc2626"
                pb_color = "#16a34a" if 0 <= pb < 12 else "#d97706" if pb < 24 else "#dc2626"
                if lc >= 3 and (pb < 12):
                    ue_verdict = "🟢 <strong>Healthy unit economics.</strong> LTV:CAC ≥ 3 and payback under a year — this is the zone where customer acquisition creates value."
                elif lc >= 1.5:
                    ue_verdict = "🟡 <strong>Fragile unit economics.</strong> You are making marginal money per customer, but the buffer is thin. Small shocks (higher CAC, churn spike) flip it negative."
                elif lc > 0:
                    ue_verdict = "🔴 <strong>Negative unit economics.</strong> Each customer costs more than they return. Fix CAC (channel/segment) or price/margin/churn before scaling."
                else:
                    ue_verdict = "⚫ Unit economics could not be computed."
                churn_pct = fue["monthly_churn"] * 100
                st.markdown(f"""
                <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
                    <div style="font-weight:700;color:#1e1b4b;margin-bottom:0.5rem;">📐 Your Final Unit Economics</div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:0.75rem;">
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">CAC</div>
                            <div style="font-size:1rem;font-weight:700;color:#1f2937;">${fue['cac']:,.0f}</div>
                        </div>
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">GM</div>
                            <div style="font-size:1rem;font-weight:700;color:#1f2937;">{fue['gross_margin']*100:.0f}%</div>
                        </div>
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">Churn/mo</div>
                            <div style="font-size:1rem;font-weight:700;color:#1f2937;">{churn_pct:.1f}%</div>
                        </div>
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">LTV</div>
                            <div style="font-size:1rem;font-weight:700;color:#1f2937;">${fue['ltv']:,.0f}</div>
                        </div>
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">LTV : CAC</div>
                            <div style="font-size:1rem;font-weight:700;color:{lc_color};">{lc:.1f} : 1</div>
                        </div>
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">Payback</div>
                            <div style="font-size:1rem;font-weight:700;color:{pb_color};">
                                {"Immediate" if pb == 0 else f"{pb:.1f}mo" if pb < 999 else "Never"}
                            </div>
                        </div>
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">Upfront $</div>
                            <div style="font-size:1rem;font-weight:700;color:#1f2937;">${fue['upfront_price']:,.0f}</div>
                        </div>
                        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:0.6rem;">
                            <div style="font-size:0.7rem;color:#6b7280;text-transform:uppercase;">Monthly $</div>
                            <div style="font-size:1rem;font-weight:700;color:#1f2937;">${fue['monthly_price']:,.0f}</div>
                        </div>
                    </div>
                    <div style="font-size:0.9rem;color:#475569;">{ue_verdict}</div>
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
            ("Final Model Fit + Unit Economics", scores["final_fit"], 34,
             "Half: how close your Round 3 model is to optimal fit. Half: whether it produces healthy LTV:CAC and payback."),
            ("Iteration Quality", scores["iteration"], 30,
             f"You made {scores['total_changes']} changes: {scores['good_changes']} improved fit, {scores['bad_changes']} did not."),
            ("Founder Focus", scores["focus"], 21,
             "Focused founders change 1 or 2 levers per round, not everything at once."),
            ("Strategic Narrative", scores["narrative"], 15,
             "Your ability to articulate why your choices made sense in the market."),
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

        # --- Named theoretical frameworks (HBS-rigor grounding) ---
        st.markdown("""
        <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
            <div style="font-weight:600;color:#9a3412;margin-bottom:0.75rem;">📚 Theoretical grounding for what you just did</div>
            <ul style="color:#7c2d12;line-height:1.7;font-size:0.93rem;margin:0;padding-left:1.2rem;">
                <li><strong>Business Model Canvas (Osterwalder &amp; Pigneur, 2010):</strong> You iterated on four of the nine canvas blocks — revenue streams, pricing, channels, and customer segments. In real practice, a change in one block forces consistency checks across all nine.</li>
                <li><strong>Lean Startup (Ries, 2011):</strong> Each round was a <em>pivot-or-persevere</em> decision. The customer signals between rounds were your <em>validated learning</em>.</li>
                <li><strong>Product/Market Fit (Andreessen, 2007):</strong> "Fit" here is operationalized as the distance between your 4-lever configuration and the market's optimal. Andreessen's original definition — &quot;when the market is pulling the product out of the startup&quot; — corresponds to sustained Round-3 fit ≥ 70% with healthy unit economics.</li>
                <li><strong>SaaS unit-economics (Skok, 2012):</strong> The LTV:CAC ≥ 3 and payback &lt; 12 months thresholds your debrief used are the Bessemer/Skok benchmarks that gate Series A readiness.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # --- Worst-case unit-econ teaching moment ---
        # If final unit economics came out negative or fragile, add a specific teaching block
        try:
            final_cfg_tm = st.session_state.configs[3] or st.session_state.configs[2] or st.session_state.configs[1]
            if final_cfg_tm:
                vk_tm = st.session_state.venture_key
                ue_tm = compute_unit_economics(final_cfg_tm, vk_tm)
                teach = None
                if ue_tm and ue_tm.get("ltv_cac") is not None:
                    ltv_cac = ue_tm["ltv_cac"]
                    payback = ue_tm.get("payback", 999)
                    if ltv_cac < 1.0:
                        teach = (
                            "<strong>Negative unit economics — this is the most common cause of startup death.</strong> "
                            "Your LTV:CAC is below 1.0, meaning every customer you acquire destroys value. "
                            "The fix is never 'grow faster'; growth multiplies losses. The fix is one of three levers: "
                            "(a) lower CAC via a different <em>channel or segment</em>, (b) raise LTV via <em>price, retention, or expansion</em>, or "
                            "(c) improve gross margin. Test these levers one at a time — a classic trap is changing "
                            "everything and losing the attribution. (See Blank, <em>Four Steps to the Epiphany</em>, Ch. 4.)"
                        )
                    elif ltv_cac < 3.0 or payback >= 18:
                        teach = (
                            "<strong>Fragile unit economics — survivable but not fundable.</strong> "
                            "Your LTV:CAC is between 1 and 3, or payback exceeds 18 months. You can operate here, "
                            "but you cannot raise a priced Series A here. Skok's benchmark (LTV:CAC ≥ 3, payback &lt; 12 mo) "
                            "is the default diligence screen for institutional investors. If this were a real venture, "
                            "the next two quarters should be entirely focused on a single CAC-efficiency experiment."
                        )
                if teach:
                    st.markdown(f"""
                    <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
                        <div style="font-weight:700;color:#991b1b;margin-bottom:0.75rem;">⚠️ Teaching moment: your unit economics</div>
                        <div style="color:#7f1d1d;line-height:1.7;font-size:0.93rem;">{teach}</div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception:
            pass

        if st.button("🔁  Replay Simulation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            init_state()
            st.session_state.venture_key = "thermaloop"
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
    # Venture selection removed — ThermaLoop is locked in. Redirect to config.
    st.session_state.venture_key = "thermaloop"
    st.session_state.stage = "config"
    screen_config()
elif stage == "config":
    screen_config()
elif stage == "results":
    screen_results()
elif stage == "email":
    # Email capture removed — route directly to debrief.
    st.session_state.stage = "debrief"
    screen_debrief()
elif stage == "debrief":
    screen_debrief()
else:
    screen_intro()
