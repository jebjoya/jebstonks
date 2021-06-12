import tradier

t = tradier.Tradier(access_token="mXhjLekLobWQaSzrScdIkMXR4wf0")

options_expirations = t.get_options_expirations("GME",strikes=True)['expirations']['expiration']

all_strikes = set()

for expiration in options_expirations:
    date = expiration['date']
    strikes = expiration['strikes']['strike']
    all_strikes = all_strikes.union(set(strikes))

print(all_strikes)