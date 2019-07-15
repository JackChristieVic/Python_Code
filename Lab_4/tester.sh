timeout 120s ./tester_001.sh &> results.txt
python3 post_process.py
