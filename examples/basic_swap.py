#!/usr/bin/env python3
"""
Basic example of using the NEAR Intents AI Agent to swap NEAR for USDC.
This example demonstrates the simplest way to perform a token swap.
"""

import os
import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from near_intents.ai_agent import AIAgent

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    try:
        # Initialize the AI Agent
        agent = AIAgent("./account_file.json")
        
        # Deposit 1 NEAR for intent operations
        deposit_amount = 1.0
        logging.info(f"Depositing {deposit_amount} NEAR")
        agent.deposit_near(deposit_amount)
        
        # Swap 0.5 NEAR to USDC
        swap_amount = 0.5
        logging.info(f"Swapping {swap_amount} NEAR to USDC")
        result = agent.swap_near_to_token("USDC", swap_amount)
        
        logging.info("Swap completed successfully!")
        logging.info(f"Result: {result}")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 