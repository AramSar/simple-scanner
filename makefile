$(eval TMP := $(shell mktemp))
C = "cc"
COMPILER = "compiler0"
INP0 = "input0.txt"
OUT0 = "./output0.txt"
TMP0 = "/tmp/output0.txt"
DIFF = "/usr/bin/diff"
CMD = "/usr/bin/diff /tmp/output0.txt ./output0.txt"
all:
			$(CC) -o $(COMPILER) $(COMPILER).c

test:
			./$(COMPILER) $(INP0) > $(TMP)
ifeq ("$(shell $(DIFF) $(TMP0) $(OUT0) ; echo $$?)", "0")
			@echo "(:"
else
			@echo ":/"
endif
