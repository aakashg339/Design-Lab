TEMP_FILE_PREFIX = TempFile

result_split_5:
	@echo "Starting result_split_5"
	@shuf ../../network.txt | split -d -n r/5 - $(TEMP_FILE_PREFIX);
	@echo "Shuffle and split done";
	@/usr/bin/time -f "%e seconds" sh -c '\
		for file in $(TEMP_FILE_PREFIX)*; do \
			cat $$file | python3 mapper.py | sort | python3 combiner.py; \
		done | sort | python3 reducer.py > result_q2_t1_k5.txt; \
		echo "result_q2_t1_k5.txt is generated"; \
	'
	@echo "Ending result_split_5"
	rm -f $(TEMP_FILE_PREFIX)*

result_split_10:
	@echo "Starting result_split_10"
	@shuf ../../network.txt | split -d -n r/10 - $(TEMP_FILE_PREFIX);
	@echo "Shuffle and split done";
	@/usr/bin/time -f "%e seconds" sh -c '\
		for file in $(TEMP_FILE_PREFIX)*; do \
			cat $$file | python3 mapper.py | sort | python3 combiner.py; \
		done | sort | python3 reducer.py > result_q2_t1_k10.txt; \
		echo "result_q2_t1_k10.txt is generated"; \
	'
	@echo "Ending result_split_10"
	rm -f $(TEMP_FILE_PREFIX)*

result_split_15:
	@echo "Starting result_split_15"
	@shuf ../../network.txt | split -d -n r/15 - $(TEMP_FILE_PREFIX);
	@echo "Shuffle and split done";
	@/usr/bin/time -f "%e seconds" sh -c '\
		for file in $(TEMP_FILE_PREFIX)*; do \
			cat $$file | python3 mapper.py | sort | python3 combiner.py; \
		done | sort | python3 reducer.py > result_q2_t1_k15.txt; \
		echo "result_q2_t1_k15.txt is generated"; \
	'
	@echo "Ending result_split_15"
	rm -f $(TEMP_FILE_PREFIX)*

result_split_20:
	@echo "Starting result_split_20"
	@shuf ../../network.txt | split -d -n r/20 - $(TEMP_FILE_PREFIX);
	@echo "Shuffle and split done";
	@/usr/bin/time -f "%e seconds" sh -c '\
		for file in $(TEMP_FILE_PREFIX)*; do \
			cat $$file | python3 mapper.py | sort | python3 combiner.py; \
		done | sort | python3 reducer.py > result_q2_t1_k20.txt; \
		echo "result_q2_t1_k20.txt is generated"; \
	'
	@echo "Ending result_split_20"
	rm -f $(TEMP_FILE_PREFIX)*

result_all:
	@echo "Starting result_all"
	@/usr/bin/time -f "%e seconds" sh -c '\
		cat ../../network.txt | python3 mapper.py | sort | python3 combiner.py | sort | python3 reducer.py > result_q2_t1_all.txt; \
		echo "result_q2_t1_all.txt is generated"; \
	'