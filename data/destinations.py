"""
=============================================================
Static Data  —  Destinations, Options, Dropdown Lists
=============================================================
Day 1  |  Part 1A  (data layer)

All hardcoded lists that power the trip planning form dropdowns
and the home page destination cards live here.
=============================================================
"""

# ── Popular destination cards (shown on Home page) ────────────────────────────
POPULAR_DESTINATIONS = [
    {"name": "Goa",        "flag": "🏖️", "country": "India",     "highlight": "Beaches & Nightlife"},
    {"name": "Manali",     "flag": "🏔️", "country": "India",     "highlight": "Mountains & Adventure"},
    {"name": "Jaipur",     "flag": "🏰", "country": "India",     "highlight": "History & Culture"},
    {"name": "Kerala",     "flag": "🌿", "country": "India",     "highlight": "Backwaters & Nature"},
    {"name": "Agra",       "flag": "🕌", "country": "India",     "highlight": "Taj Mahal & Heritage"},
    {"name": "Varanasi",   "flag": "🙏", "country": "India",     "highlight": "Spiritual & Culture"},
    {"name": "Rishikesh",  "flag": "🧘", "country": "India",     "highlight": "Yoga & Adventure"},
    {"name": "Darjeeling", "flag": "🍵", "country": "India",     "highlight": "Tea Gardens & Hills"},
    {"name": "Paris",      "flag": "🗼", "country": "France",    "highlight": "Romance & Art"},
    {"name": "Bali",       "flag": "🌺", "country": "Indonesia", "highlight": "Beaches & Temples"},
    {"name": "Dubai",      "flag": "🌆", "country": "UAE",       "highlight": "Luxury & Shopping"},
    {"name": "Singapore",  "flag": "🦁", "country": "Singapore", "highlight": "Food & Culture"},
]


# ── Form dropdown options ──────────────────────────────────────────────────────

INTERESTS_LIST = [
    "Beaches", "Adventure", "Nature", "History", "Culture",
    "Food", "Shopping", "Nightlife", "Photography", "Wildlife",
    "Spiritual", "Relaxation",
]

TRAVEL_STYLES = [
    "Budget", "Standard", "Luxury",
    "Backpacker", "Family", "Couple", "Solo", "Friends",
]

ACCOMMODATION_OPTIONS = [
    "Hostel", "Budget Hotel", "3-Star Hotel",
    "4-Star Hotel", "5-Star Hotel", "Resort", "Homestay",
]

TRANSPORTATION_OPTIONS = [
    "Public Transport (Metro / Bus)",
    "Bus",
    "Train",
    "Taxi / Cab",
    "Rental Car",
    "Bike / Scooter",
    "Mixed (Auto + Metro + Cab)",
]

FOOD_PREFERENCES = [
    "Vegetarian",
    "Non-Vegetarian",
    "Vegan",
    "Jain",
    "Local Street Food",
    "Fine Dining",
    "All Cuisines",
]

# Currency label → currency code (used in format_currency)
CURRENCIES: dict[str, str] = {
    "INR — Indian Rupee (₹)":      "INR",
    "USD — US Dollar ($)":          "USD",
    "EUR — Euro (€)":               "EUR",
    "GBP — British Pound (£)":      "GBP",
    "JPY — Japanese Yen (¥)":       "JPY",
    "AUD — Australian Dollar (A$)": "AUD",
    "CAD — Canadian Dollar (C$)":   "CAD",
}
