intro_message = '''
🔹Хотите заказать Биг Мак, Баскет из KFC или любую вещь из Казани? 
Попросите людей, которые сейчас там, захватить ваш заказ по пути в Инно (за небольшую сумму или по договорённости). 
А поискать людей и выставить заказ можно в @DeliverInnoBot :)

🔹Едете из Казани в Инно с пустыми руками? 
Захватите чей-то заказ по пути, заработайте немного денег и сделайте доброе дело)  
А взять заказ можно в @DeliverInnoBot :)

📌Есть вопрос или предложение? Что-то сломалось и не работает? Пишите @dimtsaplia
'''

choosing_market = '''
Let's begin with choosing the name of the catering where you want to order some food (for example, McDonalds, KFC, Tatmak)
'''

choosing_item = '''
Now describe your order:
'''

set_bounty = '''
Now you can specify bounty (how much could you pay to the deliverer)
Or just say "by arrangement":
'''

print_offer = "Do you want to add this offer:\nshop: {}\nitem: {}\nbounty: {}"

confirm_offer = "You confirm your offer\nYou can check it in 'My offers'"
drop_offer = "You drop this offer\nYou can add new using 'Add offer'"

published_offer = "#{}\nshop: {}\nitem: {}\nbounty: {}"
taken_published_offer = "#{}\ntaken by: @{}\nshop: {}\nitem: {}\nbounty: {}"

list_my_taken_offers = "Alias of reciever: @{}\nshop: {}\nitem: {}\nbounty:{}"
list_other_taken_offers = "Alias of responder: @{}\nshop: {}\nitem: {}\nbounty:{}"

delet_offer_from_published = 'You delete offer #{} from you published offer list.'

list_offers = 'shop: {}\nitem: {}\nbounty:{}'

empty_list = 'This list of offers is empty'

performer_message = '''You take offer of user @{} .\n 
Now you can contact with him and arrange your delivery.\n
You can track your taken offers in section: Offers list -> My offers -> Taken offers
'''

recipient_message = '''Your offer #{} was taken by @{} .
Now you can contact with him and arrange your delivery.
'''

number_to_delete = 'Enter number of offer that you want to delete'

no_offers_to_delete = "You haven't offers to delete"

offer_not_exists = 'You trying to delete offer that does not exists'

choose_section = 'Choose section'

profile_message = 'Published offers: {}\nTaken offers: {}'

arrive_message = 'Your status changed. From now you will recieve notifications for all new offers'

left_message = 'Your status changed. From now you will not recieve notifications'