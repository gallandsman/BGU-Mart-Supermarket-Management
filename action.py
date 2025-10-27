from persistence import *

import sys

def main(args : list[str]):
   inputfilename : str = args[1]
   with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            product_id, quantity, activator_id, date= int(splittedline[0]), int(splittedline[1]), int(splittedline[2]), splittedline[3]
            oldQuantity = (repo.products.find(id = product_id)[0]).quantity        
            if oldQuantity + quantity >= 0 :
                repo.update_product(product_id, oldQuantity + quantity)
                activitie = Activitie(product_id, quantity, activator_id, date)
                repo.activities.insert(activitie)

if __name__ == '__main__':
    main(sys.argv)
  