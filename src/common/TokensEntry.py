from dataclasses import dataclass

@dataclass
class TokensEntry:
    user: str
    tokens: int
    coins: int
    needed_tokens: int

    def __str__(self) -> str:
        return f"TokensEntry: \n" \
               f"  User: {self.user}\n" \
               f"  Tokens: {self.tokens}\n" \
               f"  Coins: {self.coins}\n" \
               f"  Needed Tokens Per Coin: {self.needed_tokens}"