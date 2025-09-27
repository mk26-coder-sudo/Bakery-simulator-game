import random 
import time 

star = "\U00002B50" 
gameState = True 
day = 1

#Available ingredients: quantity, price
pantry = {"Coffee Beans": {"quantity": 3, "price": 2}, 
          "Milk": {"quantity": 4, "price": 3}, 
          "Chocolate": {"quantity": 4, "price": 2.5}, 
          "Egg": {"quantity": 4, "price": 1}, 
          "Nutmeg": {"quantity": 4, "price": 2}, 
          "Flour": {"quantity": 2, "price": 3}, 
          "Sugar": {"quantity": 4, "price": 1}, 
          "Butter": {"quantity": 3, "price": 5}, 
          "Yeast": {"quantity": 2, "price": 2}, 
          "Strawberry": {"quantity": 4, "price": 3}, 
          "Apple": {"quantity": 4, "price": 3.5}, 
          "Condensed Milk": {"quantity": 4, "price": 5}, 
          "Tea Leaves": {"quantity": 2, "price": 2.5}, 
          "Cream": {"quantity": 4, "price": 2.5}
          #NOTE: Water is infinite and free 
          }

#Separate recipe catalogs
drinkRecipes={
    "Coffee \u2615": {"ingredients":("Coffee Beans", "Milk"), "time": 1, "price":7},
    "Hot Chocolate \U0001F964": {"ingredients":("Chocolate", "Milk"), "time": 3, "price":8},
    "Egg Nog \U0001F95A\U0001F95B": {"ingredients":("Egg", "Milk", "Nutmeg"), "time": 5, "price":10},
    "Strawberry Smoothie \U0001F964\U0001F353": {"ingredients":("Strawberry", "Water", "Cream"), "time": 4, "price":9},
    "Cold Coco \U0001F9CA\U0001F36B": {"ingredients":("Chocolate", "Condensed Milk"), "time": 5, "price":12},
    "Iced Coffee \U0001F9CA\u2615": {"ingredients":("Coffee Beans", "Water"), "time": 1, "price":4},
    "Apple Juice \U0001F34E": {"ingredients":("Apple", "Water"), "time": 3, "price":6},
    "Tea \U0001F375": {"ingredients":("Tea Leaves", "Milk"), "time": 2, "price":7}, 
    "Icecream Shake \U0001F366": {"ingredients":("Cream", "Sugar", "Condensed Milk"), "time": 7, "price":15},
    "Iced Tea \U0001F9CA\U0001F375": {"ingredients":("Tea Leaves", "Water"), "time": 3, "price":5}
    }
bakeRecipes={
    "Brownie \U0001F36B": {"ingredients":("Chocolate", "Flour", "Sugar", "Butter", "Egg"), "time": 4, "price":15},
    "Chocolate Cookie \U0001F36A": {"ingredients":("Chocolate", "Flour", "Sugar", "Milk", "Egg"), "time": 3, "price":15},
    "Croissant \U0001F950": {"ingredients":("Yeast", "Flour", "Sugar", "Butter"), "time": 4, "price":15},
    "Strawberry Donut \U0001F369\U0001F353": {"ingredients":("Flour", "Strawberry", "Sugar", "Butter", "Yeast"), "time": 5, "price":20},
    "Cheesecake \U0001F9C0": {"ingredients":("Condensed Milk", "Sugar", "Butter", "Egg"), "time": 4, "price":17},
    "Apple Pie \U0001F34E\U0001F967": {"ingredients":("Egg", "Milk", "Apple"), "time": 4, "price":10},
    "Candy Apple \U0001F36D\U0001F34E": {"ingredients":("Apple", "Sugar", "Butter"), "time": 5, "price":12},
    "Chocolate Pastry \U0001F36B\U0001F370": {"ingredients":("Chocolate", "Flour", "Sugar", "Butter", "Milk"), "time": 3, "price":18},
    "Pancake \U0001F95E": {"ingredients":("Flour", "Sugar", "Butter", "Egg"), "time": 6, "price":20},
    "Muffin \U0001F9C1": {"ingredients":("Strawberry", "Flour", "Sugar", "Butter", "Condensed Milk"), "time": 2, "price":22},
    "Swiss Roll \U0001F365": {"ingredients":("Strawberry", "Flour", "Sugar", "Nutmeg", "Egg"), "time": 5, "price":15},
    "Bomboloni \U0001F369": {"ingredients":("Chocolate", "Flour", "Milk", "Yeast"), "time": 6, "price":12}
}

overallStats = {
    'totalSales': 0.0,
    'totalCost': 0.0,
    'totalProfit': 0.0,
    'totalTips': 0.0,
    'playerMoney': 0.0,
    'ratings': []
}
perDayStats = {}

#Save the game-data
def saveGame(): 
  data = {'overall': overallStats, 
          'perDay': perDayStats, 
          'pantry': pantry,
          'day': day
  } 
  with open('savefile.txt','w') as f:
     f.write(str(data))
     print('Game saved to savefile.txt')

#Calculate and return the average of a list of ratings. Returns 0.0 if the list is empty
def getAverageRating(ratings): 
   if not ratings: 
    return 0.0 
   total = 0 
   for r in ratings: 
    total += r 
   average = total / len(ratings) 
   return average

#Randomly decide if the customer orders a drink, bake, or both. Returns drink, bakery item
def takeOrder(custID): 
  choice = random.choice(["drink","bake","both"]) 
  if choice == "drink": 
    drink = random.choice(list(drinkRecipes.keys())) 
    bake = None 
    print(f"Customer #{custID} orders: {drink}")
  elif choice == "bake": 
    drink = None
    bake = random.choice(list(bakeRecipes.keys())) 
    print(f"Customer #{custID} orders: {bake}")
  else:
     drink = random.choice(list(drinkRecipes.keys())) 
     bake = random.choice(list(bakeRecipes.keys())) 
     print(f"Customer #{custID} orders: {drink} + {bake}") 
  return drink, bake
 
#Simulate prep time. Returns start-time
def prepOrder(drink, bake):
    totalTime = 0  
    if drink: 
      totalTime += drinkRecipes[drink]['time'] 
    if bake: 
      totalTime += bakeRecipes[bake]['time'] 
    print('Preparing order... ⏱') 
    time.sleep(totalTime) 
    return time.time()

#Check & decrement pantry (ignoring Water). Returns False if any out of stock, otherwise True
def checkPantry(drink, bake):  
  ingredients = [] 
  if drink: 
    ingredients.extend(drinkRecipes[drink]['ingredients']) 
  if bake:
    ingredients.extend(bakeRecipes[bake]['ingredients'])
  for ing in ingredients: 
    if ing == 'Water': 
      continue 
    if pantry[ing]['quantity'] > 0: 
      pantry[ing]['quantity'] -= 1 
    else: 
      return False 
  return True

#Calculate the delay in serving the order. Returns number of stars given by customer
def serveOrder(start): 
  delay = time.time() - start
  if delay <= 3: 
    return 5 
  if delay <= 5: 
    return 4 
  if delay <= 8: 
    return 3 
  if delay <= 10: 
    return 2 
  return 1

#Calculate sale price, profit, and tips; update stats 
def getMoney(drink, bake, rating): 
  salePrice = 0.0 
  cost = 0.0 
  if drink:
    salePrice += drinkRecipes[drink]['price'] 
    for ing in drinkRecipes[drink]['ingredients']: 
      if ing != 'Water': 
        cost += pantry[ing]['price'] 
  if bake: 
    salePrice += bakeRecipes[bake]['price'] 
    for ing in bakeRecipes[bake]['ingredients']: 
      if ing != 'Water': 
        cost += pantry[ing]['price']
  profit = salePrice - cost 
  overallStats['totalProfit'] += profit 
  overallStats['totalSales'] += salePrice
  overallStats['totalCost'] += cost

  #Calculate tips according to rating of customer 
  if rating < 3: 
    tips = 0
  elif rating == 3: 
    tips = 0.1 * salePrice 
  elif rating == 4: 
    tips = 0.2 * salePrice 
  else: 
    tips = 0.5 * salePrice 
  overallStats['totalTips'] += tips
  overallStats['playerMoney'] += (salePrice + tips - cost) 
  return salePrice, tips, profit

#Display menu-option along with pantry details
def displayPantry():
   print("0: Exit Restocking")
   itemNum = 1
   for item in pantry:
      details = pantry[item]
      print(f"{itemNum}: {item} - Quantity: {details['quantity']}, Price: {details['price']}")
      itemNum += 1
   print("15: Show Available Pantry Items")

#Restock pantry manually, after completing the level
def restockPantry():
  funds = overallStats['playerMoney']

  print("\n\nToday's day is over! Showing current pantry...")
  displayPantry()
  choice = input("Would you like to restock your pantry? (y/n) ")

  while choice!='y' and choice!='n':
     choice = input("Invalid choice. Please enter 'y' or 'n': ")
     
  if choice == 'y':
    while True: #(i)
        print(f"Your current funds: ${funds}")
        itemRestock = int(input("Which item do you want to restock? Enter its listed number: "))
        if itemRestock==0:
           break
        if itemRestock==15:
           displayPantry()

        itemNum = 1
        found = False  #Flag to check if the item number is valid
        for item in pantry: #(ii)
            if itemRestock == itemNum:
                found = True
                print(f"The item you want to restock is: {item}")

                while True:
                    quantity = int(input(f"Your funds are ${funds}. Enter the quantity you want to restock: "))
                    while quantity < 0:
                      quantity=int(input("Please enter a valid quantity: "))

                    totalCost = pantry[item]['price'] * quantity
                    if totalCost > funds:
                        print(f"Insufficient funds! You need ${totalCost}, but only have ${funds}.")
                    else:
                        pantry[item]['quantity'] += quantity
                        funds -= totalCost
                        overallStats['playerMoney'] = funds
                        print(f"Restocked {item}! New quantity: {pantry[item]['quantity']}")
                        break  #Exit restock for-loop (ii)
                break  #Exit item search while-loop (i)
            itemNum += 1
        
        if not found:
            print("Invalid item number.")    

#Main-Game Loop
print("\u2615\U0001F370WELCOME TO BAKERY SIMULATOR\U0001F370\u2615\n")
while gameState: 
  print(f"=== DAY {day} ===") 
  dailyRatings = [] 
  dailyProfit = dailySales = dailyTips = 0.0

  numCust = random.randint(2, 2+ (day//2))
  for custID in range(1, numCust+1):
    input(f"Press ENTER to take customer #{custID}'s order...")

    #Take order
    drink, bake = takeOrder(custID)

    #Check pantry before preparing
    if not checkPantry(drink, bake):
        print("Out of ingredients! Customer leaves unhappy.")
        rating = 1
        salePrice = 0.0
        tips = 0.0
        profit = 0.0
    else:
        #Prepare and serve
        start = prepOrder(drink, bake)
        input("Press ENTER to serve...")
        rating = serveOrder(start)
        salePrice, tips, profit = getMoney(drink, bake, rating)

    #Show results
    print(f"Customer #{custID} rating: {star * rating}")
    print(f"Sale price: ${salePrice:.2f}, Tips: ${tips:.2f}")
    print("-" * 30)

    dailyRatings.append(rating)
    overallStats['ratings'].append(rating)
    dailySales+= salePrice
    dailyProfit += profit
    dailyTips += tips

  #End-of-day summary
  avgDayRate = getAverageRating(dailyRatings)
  time.sleep(1)
  print("-" * 30)
  print(f"Day {day} complete\u2705 \n-->Avg Rating: {avgDayRate:.2f} stars\n-->Today's Sales: ${dailySales}\n-->Today's Profit: ${dailyProfit:.2f}\n-->Your tips: ${dailyTips:.2f} (Thanks to your service!)")

  perDayStats[day] = {
      'profit': dailyProfit,
      'avgRating': avgDayRate
  }

  #Restock pantry after level is over
  time.sleep(1)
  restockPantry()

  #Continue or exit game, after restocking
  choice = input("1) Continue  2) Save & Exit > ")
  while choice.strip() != '1' and choice.strip() != '2':
    choice = input("Invalid choice. Please enter '1' or '2': ")
  if choice.strip() == '1':
      day += 1
      print("\n\nMoving to next day...")
  elif choice.strip() == '2':
      saveGame()
      gameState = False
