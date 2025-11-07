knowledge_base = {
    "BMW": {
        "available": True,
        "price": 180000,
        "date": "2018",
        "mileage": 100000,
    },
    "Toyota": {
        "available": True,
        "price": 10000,
        "date": "2012",
        "mileage": 250000,
    },
    "Honda": {
        "available": False,
        "price": 30000,
        "date": "2019",
        "mileage": 170000,
    },
}


def chatbot(query):
    response = "Specify what you want"

    car = None
    for item in knowledge_base.keys():
        if item.lower() in query:
            car = item
            break

    # ✅ If car not in database
    if car is None:
        return "I don't have this car."

    if "available" in query:
        available = knowledge_base[car]["available"]
        if available:
            response = f"{car} is available."
        elif not available:
            response = f"{car} is currently out of stock."
        else:
            response = "I don't have this car"

    elif "price" in query:
        price = knowledge_base[car]["price"]
        if price:
            response = f"The {car} costs ${price}."
        else:
            response = "I don't have pricing for this car"

    elif "date" in query:
        date = knowledge_base[car]["date"]
        if date:
            response = f"{car} is from {date}."
        else:
            response = "I don't have date for this car"

    elif "mileage" in query:
        mileage = knowledge_base[car]["mileage"]
        if mileage:
            response = f"The mileage of {car} is {mileage}."
        else:
            response = "I don't have mileage for this car"

    return response


while True:
    user = input("You: ").lower()
    if user == "exit" or len(user) == 0:
        break
    bot_reply = chatbot(user)
    print(f"Chatbot: {bot_reply}")
