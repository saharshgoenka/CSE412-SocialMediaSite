OUTPUTS = $(sort $(wildcard outputs/*.txt))
QUESTIONS = $(patsubst outputs/%.txt,%,$(OUTPUTS))
SRC_DIRECTORY = PASTE THE FILE PATH TO THE init_db FOLDER HERE
MAKEFILE_PATH = $(SRC_DIRECTORY)/makefile
ROOT = $(MAKEFILE_PATH)

all: path $(QUESTIONS)
	rm -rf tmp

%: queries/%.sql
	@echo "checking $@; correct if nothing below ----"
	@psql -A -t -d $(USER) -q -f $< 1> tmp/$@.txt
	@diff outputs/$@.txt tmp/$@.txt || echo "$@ is wrong"; exit 0
	@echo ""

path:
	@mkdir -p tmp

setup_postgres:
	@echo "creating tables"
	psql -d $(USER) -q -f $(SRC_DIRECTORY)/setup.sql

clean_postgres:
	@echo "dropping tables"
	psql -d $(USER) -q -f $(SRC_DIRECTORY)/clean.sql


.PHONY: setup_postgres