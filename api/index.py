import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from snapskiee.app import app

# Handler export for Vercel serverless functions
handler = app
