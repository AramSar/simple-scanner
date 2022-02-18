PYTHON = "python3"
COMPILER = "compiler0.py"
INP0 = "input0.txt"
OUT0 = "./output0.txt"
TMP0 = "/tmp/output0.txt"
DIFF = "/usr/bin/diff"
test:
			$(shell $(PYTHON) $(COMPILER) $(INP0) > $(TMP0))
		
ifeq ("$(shell $(DIFF) $(TMP0) $(OUT0); echo $$?)", "0")
			@echo "(:"
else
			@echo ":/"
endif
