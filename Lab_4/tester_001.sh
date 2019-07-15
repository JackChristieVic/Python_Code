#!/bin/bash
# Points: 10
N=10

# create the test file
echo "SERVER TEST FILE" > test.txt

# create test folders
rm -rf test_*
mkdir test_server
cp server.py test_server
cp test.txt test_server
for i in 01 02 03 04 05 06 07 08 09 10
do
	mkdir test_${i}
	cp client.py test_${i}
done

# start the server
cd test_server
python3 server.py 11100 3 &
server_pid=$!
disown
sleep 2
cd ..

# run the clients
for i in 01 02 03 04 05 06 07 08 09 10
do
	cd test_${i}
	timeout 30s unbuffer python3 client.py 11100 CLIENT-${i} &
	pids+="$pids $!"
	cd ..
	sleep 0.2
done

wait $pids
for i in 01 02 03 04 05 06 07 08 09 10
do
	cd test_${i}
	if [ -e test.txt ]; then
		if diff test.txt ../test.txt > /dev/null ; then
			echo "CLIENT $i PASS"
		else
			echo "CLIENT $i FAIL"
		fi
	else
		echo "CLIENT $i FAIL"
	fi
	cd ..
done

kill $server_pid
