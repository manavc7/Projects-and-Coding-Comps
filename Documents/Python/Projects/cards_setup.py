cards = []
# a list of all the suits 
Suits = ['CLUB', 'DIAMOND', 
         'Heart', 'SPADE'] 
# a list of all the ranks 
Ranks = ['A', '2', '3', '4', 
         '5', '6', '7', '8', 
         '9', '10', 'J', 'Q', 'K'] 
  
# Matching all the suits with all the ranks 
for rank in Ranks: 
  
    for suit in Suits: 
                cards.append(f'{rank} of {suit}') 
  
    # Spacer 

print(cards)

