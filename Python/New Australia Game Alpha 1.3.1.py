from main import MAIN
import traceback
import sys

try:
	MAIN()
except Exception as e:
    # Print the exception traceback
    traceback.print_exc()
    # Prompt the user to press a key to continue
    if hasattr(sys, 'ps1') or sys.stdin.isatty():
        input("Press Enter to continue...")