# python script to simulate clients for a rental business

# clients are modelled as having a number of states: tier 1, tier 2, tier 3, off
# each states brings in money on a certain timestep
# the simulation steps through at a rate of 1 day / timestep

import random
import matplotlib.pyplot as plt

# vars
NEW_PHONE_COST = -500
SUBSCRIPTION = 19
MINIMUM_EXCESS = 1 # number of phones to be kept in reserve

def phone_cost_function(phone):
  return NEW_PHONE_COST - 4 * phone.age

def subscription_function(phone):
  return SUBSCRIPTION - 0.2 * phone.age

# client object
class Client(object):
  def __init__(self, initial_state, id):
    self.id = id
    self.day_counter = 0
    self.state = initial_state
    self.total_income = 0
    self.phone = None

class Phone(object):
  def __init__(self, client, id):
    self.id = id
    self.age = 0
    self.day_counter = 0
    self.client = client
    self.available = False
    self.sold = False

  def __str__(self):
    return '{}: {}'.format(self.age, 'available' if self.available else 'unavailable')

# states
states = (
  'new_phone',
  'discount_phone',
  'keep',
  'off',
)

# run
money = 1000
clients = [Client('new_phone', id=0)]
phones = []

def client_id():
  return len(clients)

def phone_id():
  return len(phones)

money_history = []

for day in range(2000):
  # 1. total money for this day
  day_money = 0

  # 2. update clients
  for client in clients:
    # check client day
    if client.day_counter == 0:
      # check client state
      if client.state == 'new_phone':
        # buy new phone for client
        # charge highest subscription

        # save old phone
        if client.phone is not None:
          current_phone = client.phone
          current_phone.client = None
          current_phone.available = True

        # make new phone
        client.phone = Phone(client, id=phone_id())
        # print('new phone {}'.format(NEW_PHONE_COST))
        phones.append(client.phone)

      elif client.state == 'discount_phone':
        pass

      elif client.state == 'keep':
        pass

      elif client.state == 'off':
        pass

      # reset day_counter
      client.day_counter = 1

      # pay
      day_money += phone_cost_function(client.phone) + subscription_function(client.phone)

    elif client.day_counter == 28:
      client.day_counter = 0

    else:
      client.day_counter += 1

  # 3. randomly add clients
  if random.randint(0,10)==1:
    client = Client('new_phone', id=client_id())
    client.phone = Phone(client, id=phone_id())
    clients.append(client)

  # 4. update phones
  # get difference of available phones from minimum excess
  difference = len(filter(lambda x: x.available, phones)) - MINIMUM_EXCESS
  for phone in filter(lambda phone: not phone.sold, phones):
    # phone age
    if phone.day_counter == 28:
      phone.day_counter = 0

      # update age
      phone.age += 1

    else:
      phone.day_counter += 1

    # sell excess
    if phone.available and difference > 0:
      if random.randint(0,1)==1:
        day_money -= phone_cost_function(phone)
        phone.sold = True
        phone.available = False
        difference -= 1

  # 5. pay money
  money += day_money
  if day_money != 0:
    print(money, len(clients))
  money_history.append(money)

plt.plot(money_history)
plt.show()
