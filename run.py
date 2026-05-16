#!/usr/bin/env python3
"""
CV Manager Web - Entry Point
"""

import sys
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get port from command line or use default
    port = 5001
    if len(sys.argv) > 1 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    
    print(f"\n{'='*60}")
    print(f"CV Manager Web is running!")
    print(f"Open your browser and go to: http://localhost:{port}")
    print(f"{'='*60}\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
