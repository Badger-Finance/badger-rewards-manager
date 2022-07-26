from random import seed
from random import random

EPOCHS_RANGE = 10
EPOCHS_MIN = 1
SHARES_DECIMALS = 18
RANGE = 10_000 ## Shares can be from 1 to 10k with SHARES_DECIMALS
MIN_SHARES = 1_000 ## Min shares per user
SECONDS_PER_EPOCH = 604800

REWARD_PER_EPOCH = 10_000 * 10 ** SHARES_DECIMALS ## 10 k ETH example
USERS_RANGE = 100
USERS_MIN = 3

def simple_users_sim():

  number_of_epochs = int(random() * EPOCHS_RANGE) + EPOCHS_MIN
  number_of_users = int(random() * USERS_RANGE) + USERS_MIN

  total_user_deposits = 0

  claiming = [] ## Is the user strat to claim each week
  claimers = 0
  initial_balances = []
  balances = []
  points = []
  total_supply = 0
  total_points = 0
  claimed = [] ## How much did each user get
  for user in range(number_of_users):
    is_claiming = random() >= 0.5
    claimers += 1 if is_claiming else 0
    claiming.append(is_claiming)
    balance = int(random() * RANGE) + MIN_SHARES
    balances.append(balance)


    initial_balances.append(balance)
    total_user_deposits += balance
    claimed.append(0)

    user_points = balance * SECONDS_PER_EPOCH
    points.append(user_points)

    total_supply += balance
    
  total_rewards = REWARD_PER_EPOCH * number_of_epochs
  contract_points = total_rewards * SECONDS_PER_EPOCH
  contract_points_per_epoch = REWARD_PER_EPOCH * SECONDS_PER_EPOCH

  total_supply += total_rewards

  total_points = total_supply * SECONDS_PER_EPOCH

  ## Simulation of user claiming each epoch and contract properly re-computing divisor
  total_dust = 0
  total_claimed = 0

  cached_contract_points = contract_points
  ## SETUP total_claimed_per_epoch
  total_claimed_per_epoch = []

  for epoch in range(number_of_epochs):
    total_claimed_per_epoch.append(0)

  for epoch in range(number_of_epochs):
    for user in range(number_of_users):
      ## Skip for non-claimers
      if not (claiming[user]):
        continue
      
      print("User percent of total")
      print(points[user] / total_points * 100)

      user_total_rewards_unfair = REWARD_PER_EPOCH * points[user] // total_points
      user_dust_unfair = REWARD_PER_EPOCH * points[user] % total_points

      print("user_total_rewards_unfair")
      print(user_total_rewards_unfair)
      print("user_dust_unfair")
      print(user_dust_unfair)

      divisor = (total_points - (contract_points - contract_points_per_epoch * epoch))

      user_total_rewards_fair = REWARD_PER_EPOCH * points[user] // divisor
      user_total_rewards_dust = REWARD_PER_EPOCH * points[user] % divisor


      temp_user_points = points[user]
      ## Add new rewards to user points for next epoch
      points[user] = temp_user_points + user_total_rewards_fair * SECONDS_PER_EPOCH
      balances[user] += user_total_rewards_fair 

      claimed[user] += user_total_rewards_fair

      print("user_total_rewards_fair")
      print(user_total_rewards_fair)
      print("user_total_rewards_dust")
      print(user_total_rewards_dust)
      total_claimed += user_total_rewards_fair
      total_dust += user_total_rewards_dust
      total_claimed_per_epoch[epoch] += user_total_rewards_fair
    
    ## Subtract points at end of epoch
    contract_points -= total_claimed_per_epoch[epoch] * SECONDS_PER_EPOCH
  
  ## After the weekly claimers sim, reset
  contract_points = cached_contract_points


  ## Simulation of user claiming all epochs at end through new math
  ## They will use the updated balances, without reducing them (as they always claim at end of entire period)
  for epoch in range(number_of_epochs):
    for user in range(number_of_users):
      ## Skip for claimers // Already done above
      if (claiming[user]):
        continue
      
      print("User percent of total")
      print(points[user] / total_points * 100)

      user_total_rewards_unfair = REWARD_PER_EPOCH * points[user] // total_points
      user_dust_unfair = REWARD_PER_EPOCH * points[user] % total_points

      print("user_total_rewards_unfair")
      print(user_total_rewards_unfair)
      print("user_dust_unfair")
      print(user_dust_unfair)

      divisor = (total_points - (contract_points - contract_points_per_epoch * epoch))

      user_total_rewards_fair = REWARD_PER_EPOCH * points[user] // divisor
      user_total_rewards_dust = REWARD_PER_EPOCH * points[user] % divisor

      # contract_points -= user_total_rewards_fair * REWARD_PER_EPOCH

      temp_user_points = points[user]
      ## Add new rewards to user points for next epoch
      points[user] = temp_user_points + user_total_rewards_fair * SECONDS_PER_EPOCH
      balances[user] += user_total_rewards_fair 

      claimed[user] += user_total_rewards_fair

      print("user_total_rewards_fair")
      print(user_total_rewards_fair)
      print("user_total_rewards_dust")
      print(user_total_rewards_dust)
      total_claimed += user_total_rewards_fair
      total_dust += user_total_rewards_dust
    
    contract_points -= total_claimed_per_epoch[epoch] * SECONDS_PER_EPOCH


  print("number_of_users")
  print(number_of_users)

  print("claimers")
  print(claimers)

  print("total_rewards")
  print(total_rewards)

  print("total_dust points")
  print(total_dust)

  print("total_claimed")
  print(total_claimed)

  print("total epochs")
  print(number_of_epochs)

  print("actual dust rewards")
  print(abs(total_rewards - total_claimed))

  print("Percent distributed over dusted")
  print((total_rewards - total_claimed) / total_rewards)

  
  ## 2 things about fairness
  ## Consistency -> Predictable unfairness is better than unpredictable fairness as it can be gamed to user advantage
  ## Always rounding down -> Any round up will break the accounting, it's extremely important we are "fair" but "stingy" in never giving more than what's correct

  for user in range(number_of_users):
    print("User %s", user)
    print("Deposit Ratio")
    print(initial_balances[user] / total_user_deposits * 100)
    print("Rewards Ratio")
    print(claimed[user] / total_rewards * 100)


  ## 


def main():
  simple_users_sim()