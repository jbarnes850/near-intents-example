# NEAR Intents AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python implementation for interacting with NEAR using intents for multichain financial products. This implementation provides an AI Agent that automates token swaps and other operations on the NEAR mainnet.

## Overview

NEAR Intents is a system for executing multichain transactions. An intent represents a user's desired state change (e.g., "I want to swap X NEAR for Y USDC") rather than a specific execution path. This allows for more flexible and efficient execution of financial operations.

### Protocol Architecture

```bash
NEAR Intents
├── Intent Settlement
│   ├── Solver Bus (off-chain message bus)
│   └── Verifier (on-chain smart contract)
└── Entities
    ├── Distribution Channels
    └── Solvers
```

### Implementation Architecture

Our implementation maps to the protocol components as follows:

```bash
near-intents-ai-agent/
├── src/near_intents/
│   ├── near_intents.py    # Core protocol interactions
│   │   ├── IntentRequest  # Creates intent requests
│   │   ├── Quote         # Handles quote creation/signing
│   │   └── ASSET_MAP     # Supported tokens configuration
│   │
│   └── ai_agent.py       # High-level interface
│       └── AIAgent       # Manages the full swap flow
│
├── examples/             # Usage examples
│   └── basic_swap.py    # Basic NEAR to USDC swap
│
└── tests/               # Test coverage
    └── test_ai_agent.py
```

### Component Mapping

1. **Solver Bus Integration** (`near_intents.py`):
   - Communicates with the off-chain Solver Bus
   - Fetches trading options and quotes
   - Publishes signed intents

2. **Intent Creation & Verification** (`near_intents.py`):
   - Creates and signs token diff intents
   - Interacts with the on-chain verifier contract
   - Handles token deposits and withdrawals

3. **AI Agent Interface** (`ai_agent.py`):
   - Provides high-level swap operations
   - Manages account setup and registration
   - Handles token storage and deposits

### Key Components

1. **Intent Settlement**:
   - **Solver Bus**: An off-chain message bus for communication between users and solvers
   - **Verifier**: Smart contract on NEAR that verifies and executes signed intents

2. **Key Players**:
   - **Users**: Participants who issue intents (e.g., "swap NEAR for USDC")
   - **Solvers**: Market participants who fulfill user intents
   - **Distribution Channels**: Applications connecting users with the intent system

## Architecture

### AI Agent (`ai_agent.py`)

The AI Agent serves as a high-level interface for executing intents on NEAR mainnet. It handles:

1. **Account Management**:
   - Loading NEAR accounts from key files
   - Registering public keys for intent operations
   - Managing token storage registration

2. **Core Operations**:
   - NEAR deposits for intent operations
   - Token swaps using the intent system
   - Error handling and logging

### NEAR Intents Library (`near_intents.py`)

The core library implementing the NEAR Intents protocol:

1. **Asset Management**:
   - Token mappings and identifiers
   - Decimal precision handling
   - Storage registration

2. **Intent Operations**:
   - Quote creation and signing
   - Intent submission and execution
   - Solver bus interaction

## Flow Diagram

```bash
User Request → AI Agent → NEAR Intents Library → Solver Bus → NEAR Blockchain
     ↑                                              ↓
     └──────────────── Response/Result ────────────┘
```

## Implementation Details

### 1. Intent Creation Flow

```python
# The complete flow from user request to execution:

# 1. Initialize AI Agent with account
agent = AIAgent("./account_file.json")
# - Loads NEAR account
# - Registers public key with intents contract
# - Verifies account state and balance

# 2. Deposit NEAR if needed
agent.deposit_near(1.0)
# - Checks current balance
# - Registers token storage
# - Deposits NEAR to intents contract

# 3. Execute a swap
result = agent.swap_near_to_token("USDC", 1.0)
# - Creates intent request
# - Fetches quotes from Solver Bus
# - Selects best quote
# - Signs and submits intent
# - Returns execution result
```

### 2. Under the Hood

The swap process involves several steps:

1. **Quote Creation**:

   ```python
   # Create intent request
   request = IntentRequest()
       .set_asset_in("NEAR", amount_in)
       .set_asset_out("USDC")
   
   # Get quotes from Solver Bus
   options = fetch_options(request)
   best_option = select_best_option(options)
   ```

2. **Intent Execution**:

   ```python
   # Create and sign quote
   quote = create_token_diff_quote(
       account, "NEAR", amount_in, "USDC", best_option['amount_out']
   )
   
   # Submit to Solver Bus
   response = publish_intent(quote)
   ```

## Setup and Configuration

### Prerequisites

- Python 3.8+
- NEAR account with sufficient balance
- Account credentials in JSON format

### Environment Variables

```bash
NEAR_ACCOUNT_FILE=./account_file.json
NEAR_DEPOSIT_AMOUNT=1.0
TARGET_TOKEN=USDC
SWAP_AMOUNT=1.0
```

### Account File Format

```json
{
    "account_id": "your-account.near",
    "private_key": "ed25519:..."
}
```

## Quick Start

### Option 1: Interactive Setup (Recommended for New Users)

Run our interactive setup script:

```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

This script will:

1. Check and install prerequisites
2. Guide you through NEAR wallet creation
3. Set up your development environment
4. Configure your account and environment
5. Execute your first swap

### Option 2: Manual Setup

If you prefer to set things up manually:

1. **Clone the repository**

```bash
git clone https://github.com/jbarnes850/near-intents-example
cd near-intents-example
```

2. **Set up your Python environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure your environment**

```bash
cp .env.example .env
cp account_file.example.json account_file.json
```

4. **Set up your NEAR account**

- Create a NEAR account (here's a [wallet portal](https://wallet.near.org) if you don't have one)
- Export your private key from the NEAR wallet
- Update `account_file.json` with your account details:
  - Replace `your-account.near` with your actual account ID
  - Replace `your-private-key-here` with your actual private key

5. **Configure your environment variables**

Edit `.env` file and adjust the values according to your needs:

```bash
NEAR_DEPOSIT_AMOUNT=1.0  # Amount you want to deposit
SWAP_AMOUNT=1.0         # Amount you want to swap
```

6. **Run your first swap**

```bash
python intents/ai_agent.py
```

## Usage Examples

### 1. Basic Token Swap

```python
from ai_agent import AIAgent

# Initialize agent
agent = AIAgent("./account_file.json")

# Deposit NEAR for operations
agent.deposit_near(1.0)

# Swap NEAR to USDC
result = agent.swap_near_to_token("USDC", 1.0)
```

### 2. Advanced Usage with Error Handling

```python
try:
    agent = AIAgent("./account_file.json")
    
    # Check account state
    account_state = agent.account.state()
    balance_near = float(account_state['amount']) / 10**24
    
    if balance_near > 1.0:
        # Deposit and swap
        agent.deposit_near(1.0)
        result = agent.swap_near_to_token("USDC", 0.5)
        print(f"Swap completed: {result}")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Supported Assets

Currently supported tokens in this demo:

- NEAR (Native token)
- USDC (a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near)

## Error Handling

The implementation includes comprehensive error handling for:

- Insufficient balances
- Storage registration issues
- Network communication errors
- Invalid responses from solver bus
- Transaction execution failures

## Best Practices

1. **Always check balances** before operations
2. **Register storage** for new tokens
3. **Use appropriate gas limits** for transactions
4. **Handle errors** gracefully
5. **Monitor solver bus responses** for best execution

## Security Considerations

1. **Private Key Management**:
   - Store private keys securely
   - Use environment variables for sensitive data
   - Never commit credentials to version control

2. **Transaction Safety**:
   - Verify transaction amounts
   - Check recipient addresses
   - Monitor execution status

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [NEAR Intents Documentation](https://docs.near-intents.org)
- [NEAR Protocol Documentation](https://docs.near.org)
