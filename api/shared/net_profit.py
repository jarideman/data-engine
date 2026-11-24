def get_deal_net_profit(deal):
  return (
    deal.profit
    + deal.swap
    + deal.commission
    + getattr(deal, "fee", 0.0)
  )
