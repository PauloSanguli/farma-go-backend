from src.domain.security import check_password_hashed, hash_password

pwd = "gomes100"
pwd_hashed = hash_password(pwd)
print(pwd_hashed)
# print(check_password_hashed("gomes100", "\x243262243132246d526a715551547a31493644476131316f6c6c5864656a713856737238325a376973333431716d2e58552e6b44415330323363472e"))
