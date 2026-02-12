from dataclasses import dataclass

@dataclass
class TokensEntry:
    user_id: int
    tokens: int
    coins: int
    needed_tokens: int

    def __str__(self) -> str:
        return f"TokensEntry: \n" \
               f"  User_ID: {self.user_id}\n" \
               f"  Tokens: {self.tokens}\n" \
               f"  Coins: {self.coins}\n" \
               f"  Needed Tokens Per Coin: {self.needed_tokens}"