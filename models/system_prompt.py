# Системний промпт для аналітики
SYSTEM_PROMPT = (
    "You are a professional analyst specializing in the connections between global events and the cryptocurrency market. "
    "Your task is to analyze how political, economic, business, and technological factors influence the value of specific cryptocurrencies. "
    "Provide detailed explanations and build a table summarizing these factors and their impacts on cryptocurrency prices."
)

DEFAULT_DATA = [
    {
        "Factor": "Political",
        "Description": "Increased regulations in the US regarding cryptocurrency taxation.",
        "Cryptocurrency": "Bitcoin",
        "Impact on Price": "Negative - Reduced trading activity"
    },
    {
        "Factor": "Economic",
        "Description": "High inflation rates driving interest in stablecoins.",
        "Cryptocurrency": "USDT",
        "Impact on Price": "Positive - Increased demand for stability"
    },
    {
        "Factor": "Technological",
        "Description": "Ethereum's transition to Proof-of-Stake.",
        "Cryptocurrency": "Ethereum",
        "Impact on Price": "Positive - Lower energy costs, increased adoption"
    }
]


# Default queries for analysis
DEFAULT_QUERIES = [
    "Latest cryptocurrencies in the market",
    "What to buy right now?",
    "What to sell right now?",
    "Most interesting events in the crypto sphere"
]