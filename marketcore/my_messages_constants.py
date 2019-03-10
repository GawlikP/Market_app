from datetime import datetime
def MM_title_generator(product):
    return "You have buy " +product.name+" at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def MM_content_generator(seller_name,product):
    return "You buy "+product.name+" from " +seller_name+". Price was: "+str(product.price)+"$ and it was description "+ product.description

def MM_Stitle_generator(product):
    return "Your "+product.name+" has been sold!"
def MM_Scontent_generator(buyer,product):
    return "Your "+product.name+ "has been sold to" +buyer.username+" for " + str(product.price)+ " at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S");
