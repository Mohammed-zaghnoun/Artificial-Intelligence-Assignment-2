import difflib
import re

# ---------------------------------------------------------
#  EXPANDED KNOWLEDGE BASE (20 Cars + full details)
# ---------------------------------------------------------
knowledge_base = {
    "BMW 3 Series": {
        "available": True, "price": 18000, "date": "2018", "mileage": 100000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Sedan",
        "color": "Black", "engine": "2.0L Turbo", "horsepower": 255
    },
    "Toyota Corolla": {
        "available": True, "price": 10000, "date": "2012", "mileage": 250000,
        "fuel_type": "Petrol", "transmission": "Manual", "body_type": "Sedan",
        "color": "White", "engine": "1.8L", "horsepower": 132
    },
    "Honda Civic": {
        "available": False, "price": 13000, "date": "2019", "mileage": 170000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Sedan",
        "color": "Blue", "engine": "2.0L", "horsepower": 158
    },
    "Tesla Model 3": {
        "available": True, "price": 35000, "date": "2021", "mileage": 20000,
        "fuel_type": "Electric", "transmission": "Automatic", "body_type": "Sedan",
        "color": "White", "engine": "Electric Motor", "horsepower": 258
    },
    "Mercedes C-Class": {
        "available": True, "price": 27000, "date": "2017", "mileage": 85000,
        "fuel_type": "Diesel", "transmission": "Automatic", "body_type": "Sedan",
        "color": "Silver", "engine": "2.0L Turbo", "horsepower": 241
    },
    "Audi A4": {
        "available": False, "price": 22000, "date": "2016", "mileage": 92000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Sedan",
        "color": "Grey", "engine": "2.0L Turbo", "horsepower": 252
    },
    "Ford Mustang": {
        "available": True, "price": 30000, "date": "2018", "mileage": 60000,
        "fuel_type": "Petrol", "transmission": "Manual", "body_type": "Coupe",
        "color": "Red", "engine": "5.0L V8", "horsepower": 460
    },
    "Chevrolet Camaro": {
        "available": True, "price": 28000, "date": "2017", "mileage": 70000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Coupe",
        "color": "Yellow", "engine": "6.2L V8", "horsepower": 455
    },
    "Nissan Altima": {
        "available": True, "price": 9000, "date": "2013", "mileage": 180000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Sedan",
        "color": "Blue", "engine": "2.5L", "horsepower": 182
    },
    "Hyundai Elantra": {
        "available": True, "price": 8500, "date": "2014", "mileage": 160000,
        "fuel_type": "Petrol", "transmission": "Manual", "body_type": "Sedan",
        "color": "White", "engine": "1.8L", "horsepower": 148
    },
    "Kia Optima": {
        "available": True, "price": 11000, "date": "2015", "mileage": 140000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Sedan",
        "color": "Grey", "engine": "2.4L", "horsepower": 192
    },
    "Volkswagen Passat": {
        "available": False, "price": 10500, "date": "2015", "mileage": 155000,
        "fuel_type": "Diesel", "transmission": "Manual", "body_type": "Sedan",
        "color": "Black", "engine": "2.0L", "horsepower": 150
    },
    "Subaru Impreza": {
        "available": True, "price": 12000, "date": "2016", "mileage": 130000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Hatchback",
        "color": "Red", "engine": "2.0L", "horsepower": 152
    },
    "Mazda 3": {
        "available": True, "price": 14000, "date": "2017", "mileage": 90000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Hatchback",
        "color": "Blue", "engine": "2.5L", "horsepower": 184
    },
    "Jeep Wrangler": {
        "available": True, "price": 32000, "date": "2018", "mileage": 50000,
        "fuel_type": "Petrol", "transmission": "Manual", "body_type": "SUV",
        "color": "Green", "engine": "3.6L V6", "horsepower": 285
    },
    "Toyota RAV4": {
        "available": True, "price": 26000, "date": "2020", "mileage": 40000,
        "fuel_type": "Hybrid", "transmission": "Automatic", "body_type": "SUV",
        "color": "White", "engine": "2.5L Hybrid", "horsepower": 219
    },
    "Honda CR-V": {
        "available": False, "price": 24000, "date": "2019", "mileage": 60000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "SUV",
        "color": "Silver", "engine": "1.5L Turbo", "horsepower": 190
    },
    "Ford F-150": {
        "available": True, "price": 30000, "date": "2018", "mileage": 80000,
        "fuel_type": "Petrol", "transmission": "Automatic", "body_type": "Truck",
        "color": "Black", "engine": "5.0L V8", "horsepower": 395
    },
    "Ram 1500": {
        "available": True, "price": 32000, "date": "2019", "mileage": 60000,
        "fuel_type": "Diesel", "transmission": "Automatic", "body_type": "Truck",
        "color": "White", "engine": "3.0L EcoDiesel", "horsepower": 260
    }
}

# ---------------------------------------------------------
# INTENT KEYWORDS
# ---------------------------------------------------------
intent_keywords = {
    "availability": ["available", "stock", "instock", "have", "sell"],
    "price": ["price", "cost", "how much", "value", "prize"],
    "date": ["date", "year", "model", "model year"],
    "mileage": ["mileage", "km", "kilometers", "odometer"],
    "details": ["details", "info", "information", "specs", "full"],
}

all_intent_words = []
for lst in intent_keywords.values():
    all_intent_words.extend(lst)
all_intent_words.append("car")

# ---------------------------------------------------------
# HELP MENU
# ---------------------------------------------------------
def help_menu():
    return (
        "🆘 **HOW CAN I HELP YOU?**\n"
        "You can ask things like:\n"
        "• *price BMW 3 Series*\n"
        "• *Honda Civic mileage*\n"
        "• *Toyota Corolla available?*\n"
        "• *full details Tesla Model 3*\n"
        "\nAvailable cars:\n"
        + ", ".join(knowledge_base.keys()) +
        "\n\nTry typing: **price Toyota** or **details Ford Mustang**"
    )

# ---------------------------------------------------------
# SPELLING CORRECTION FOR INTENT WORDS
# ---------------------------------------------------------
def correct_word(word):
    match = difflib.get_close_matches(word.lower(), all_intent_words, n=1, cutoff=0.65)
    return match[0] if match else word

# ---------------------------------------------------------
# SUGGESTION FOR WRONG CAR NAMES (IMPROVED FOR ALL CARS)
# ---------------------------------------------------------
def suggest_cars(query_word):
    car_list = list(knowledge_base.keys())
    # 1️⃣ Use difflib to find close matches for typos
    suggestions = difflib.get_close_matches(query_word, car_list, n=5, cutoff=0.6)
    # 2️⃣ Also include partial matches in any word of the car names
    for car in car_list:
        for word in car.lower().split():
            if query_word in word and car not in suggestions:
                suggestions.append(car)
    return suggestions

# ---------------------------------------------------------
# IDENTIFY CAR (TYPO-TOLERANT FOR ALL CARS)
# ---------------------------------------------------------
def identify_car(user_text):
    words = re.findall(r"[a-zA-Z0-9-]+", user_text.lower())
    for w in words:
        # Exact match first
        for car in knowledge_base.keys():
            if w in car.lower():
                return car, None
        # Typo-tolerant suggestions
        suggestions = suggest_cars(w)
        if suggestions:
            return None, suggestions
    return None, None

# ---------------------------------------------------------
# INTENT DETECTOR
# ---------------------------------------------------------
def detect_intent(query):
    words = query.lower().split()
    corrected = [correct_word(w) for w in words]
    text = " ".join(corrected)
    for intent, keys in intent_keywords.items():
        for k in keys:
            if k in text:
                return intent
    return None

# ---------------------------------------------------------
# FULL DETAILS
# ---------------------------------------------------------
def full_details(car):
    d = knowledge_base[car]
    return (
        f"📘 **Full Details for {car}:**\n"
        f"• Availability: {'Available' if d['available'] else 'Out of stock'}\n"
        f"• Price: ${d['price']:,}\n"
        f"• Year: {d['date']}\n"
        f"• Mileage: {d['mileage']:,} km\n"
        f"• Fuel Type: {d['fuel_type']}\n"
        f"• Transmission: {d['transmission']}\n"
        f"• Body Type: {d['body_type']}\n"
        f"• Color: {d['color']}\n"
        f"• Engine: {d['engine']}\n"
        f"• Horsepower: {d['horsepower']} HP\n"
    )

# ---------------------------------------------------------
# MAIN CHATBOT LOGIC
# ---------------------------------------------------------
pending_suggestions = []

def chatbot(query):
    global pending_suggestions

    # HELP keyword detection
    if query.lower() in ["help", "assist", "guide", "how", "what can you do"]:
        return help_menu()

    # If user is selecting from suggestions
    if pending_suggestions:
        choice = query.strip()
        for car in pending_suggestions:
            if choice.lower() in car.lower():
                pending_suggestions = []
                return (
                    f"👍 Selected: **{car}**\n"
                    "What would you like to know?\n"
                    "• price\n• mileage\n• availability\n• year\n• full details"
                )
        return "❌ That doesn't match any suggestion. Try again."

    # Identify car
    car, suggestions = identify_car(query)

    # Strange/unrelated words → give guidance
    if not car and not suggestions:
        return (
            "🤔 I’m not sure what you mean.\n"
            "Type **help** to see what I can do, or try asking:\n"
            "• price Toyota\n"
            "• Honda Civic mileage\n"
            "• details Ford Mustang\n"
        )

    # If suggestions found
    if suggestions:
        pending_suggestions = suggestions
        formatted = "\n".join([f"• {s}" for s in suggestions])
        return f"❓ Did you mean:\n{formatted}\n\n👉 Type one of the names."

    # Detect intent
    intent = detect_intent(query)

    if not intent:
        return (
            f"🔍 Car found: **{car}**\n"
            "What info do you need?\n"
            "• price\n• availability\n• mileage\n• year\n• full details\n"
        )

    d = knowledge_base[car]

    if intent == "availability":
        return f"📦 **{car} is {'Available' if d['available'] else 'Out of stock'}**"

    if intent == "price":
        return f"💰 **Price of {car}:** ${d['price']:,}"

    if intent == "date":
        return f"📅 **Year:** {d['date']}"

    if intent == "mileage":
        return f"📊 **Mileage:** {d['mileage']:,} km"

    if intent == "details":
        return full_details(car)

    return "❓ Something unexpected happened. Try again."

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
def main():
    print("🤖 CarBot with HELP + SMART SUGGESTION READY — type 'help' or 'exit'\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        print(f"Chatbot: {chatbot(user)}\n")


main()
