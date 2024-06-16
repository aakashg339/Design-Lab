run_result_seperate:
	cat ../data_0.txt | python3 mapper.py | sort -n | python3 reducer.py > result_0.txt
	cat ../data_1.txt | python3 mapper.py | sort -n | python3 reducer.py > result_1.txt
	cat ../data_2.txt | python3 mapper.py | sort -n  | python3 reducer.py > result_2.txt
	cat ../data_3.txt | python3 mapper.py | sort -n  | python3 reducer.py > result_3.txt
	cat ../data_4.txt | python3 mapper.py | sort -n  | python3 reducer.py > result_4.txt
	cat ../data_5.txt | python3 mapper.py | sort -n  | python3 reducer.py > result_5.txt
	cat ../data_5.txt | python3 mapper.py | sort -n  | python3 reducer.py > result_5.txt
	(cat ../data_0.txt | python3 mapper.py & cat ../data_1.txt | python3 mapper.py & cat ../data_2.txt | python3 mapper.py & cat ../data_3.txt | python3 mapper.py & cat ../data_4.txt | python3 mapper.py & cat ../data_5.txt | python3 mapper.py) | sort -n | python3 reducer.py > result_6.txt