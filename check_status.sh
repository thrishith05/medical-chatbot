#!/bin/bash
echo "Checking initialization status..."
echo ""

# Check if process is running
if ps aux | grep -q "[i]nit_vector_db.py"; then
    echo "✓ Process is RUNNING"
    
    # Get elapsed time
    ps aux | grep "[i]nit_vector_db.py" | awk '{print "CPU: " $3 "% | Memory: " $4 "% | Time: " $10}'
    
    echo ""
    echo "Estimated time remaining: 10-15 more minutes"
else
    echo "✗ Process is NOT running"
    
    # Check if vector database exists
    if [ -d "chroma_db" ]; then
        echo "✓ Vector database EXISTS"
        echo "Files in chroma_db:"
        ls -lh chroma_db/ 2>/dev/null | head -5
        echo ""
        echo "✅ Initialization COMPLETE!"
    else
        echo "✗ Vector database NOT found"
        echo "Initialization may have failed or not completed yet"
    fi
fi

