import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from near_intents.ai_agent import AIAgent

class TestAIAgent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_account = MagicMock()
        with patch('near_intents.ai_agent.account') as mock_account_func:
            mock_account_func.return_value = self.mock_account
            self.agent = AIAgent("dummy_account.json")

    def test_deposit_near(self):
        """Test NEAR deposit functionality."""
        # Mock the account state
        self.mock_account.state.return_value = {
            'amount': str(int(2 * 10**24))  # 2 NEAR in yoctoNEAR
        }
        
        # Test deposit
        deposit_amount = 1.0
        self.agent.deposit_near(deposit_amount)
        
        # Verify the deposit was called
        self.mock_account.function_call.assert_called()

    def test_swap_near_to_token(self):
        """Test NEAR to token swap functionality."""
        # Mock the account state
        self.mock_account.state.return_value = {
            'amount': str(int(2 * 10**24))  # 2 NEAR in yoctoNEAR
        }
        
        # Mock the solver bus response
        with patch('near_intents.ai_agent.fetch_options') as mock_fetch:
            mock_fetch.return_value = [{
                'amount_out': '1000000',  # 1 USDC
                'quote_hash': 'dummy_hash'
            }]
            
            # Test swap
            result = self.agent.swap_near_to_token("USDC", 1.0)
            
            # Verify the swap was called
            self.mock_account.function_call.assert_called()

    def test_insufficient_balance(self):
        """Test handling of insufficient balance."""
        # Mock the account state with low balance
        self.mock_account.state.return_value = {
            'amount': str(int(0.1 * 10**24))  # 0.1 NEAR in yoctoNEAR
        }
        
        # Test deposit with amount greater than balance
        with self.assertRaises(ValueError):
            self.agent.deposit_near(1.0)

if __name__ == '__main__':
    unittest.main() 