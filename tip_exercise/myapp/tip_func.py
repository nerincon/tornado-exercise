# Tip calc function without conditional statements. 
# Could add in multiple service types without the need to add addtl conditionals.
# Note: No error handlers have been added for this simple tip calc. Inputs must be logical.


def get_tip():
    service_type = {"bad":0.1, "fair":0.15, "good":0.2}
    bill = int(input("Total bill amount? "))
    service = input("Level of service (good, fair or bad)? ").lower()
    tip_type = service_type.get(service)
    total_tip = tip_type * bill
    print("Tip Amount: ${:.2f}".format(total_tip))
    print("Total Amount: ${:.2f}".format(bill + total_tip))

get_tip()