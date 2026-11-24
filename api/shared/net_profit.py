def get_deal_net_profit(deal):
  return (
    deal.profit
    + deal.swap
    + getattr(deal, "commission", 0.0)
    + getattr(deal, "fee", 0.0)
  )
