run_result_seperate:
	(cat ../data_1.txt | python3 mapper.py & cat ../data_2.txt | python3 mapper.py & cat ../data_3.txt | python3 mapper.py & cat ../data_4.txt | python3 mapper.py & cat ../data_5.txt | python3 mapper.py) | sort -nk 1 | python3 reducer.py > Result_combine.txt
	cp Result_combine.txt ../