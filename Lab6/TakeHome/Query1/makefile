run_result_seperate:
	(cat ../ChatLogs/day1.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day2.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day3.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day4.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day5.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day6.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day7.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day8.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day9.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py;wait & \
	cat ../ChatLogs/day10.txt | python3 mapper.py | sort -t ',' -k1,1n -k2,2n | python3 combiner.py) | sort -t ',' -k1,1n -k2,2n  | python3 reducer.py>network.txt
	cp network.txt ../