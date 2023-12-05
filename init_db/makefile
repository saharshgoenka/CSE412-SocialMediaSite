OUTPUTS = $(sort $(wildcard outputs/*.txt))
QUESTIONS = $(patsubst outputs/%.txt,%,$(OUTPUTS))
SRC_DIRECTORY = PASTE THE PATH TO init_db FOLDER
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
	@echo "Creating tables"
	psql -d $(USER) -q -f $(SRC_DIRECTORY)/setup.sql
	@echo "Successfully created tables"


clean_postgres:
	@echo "emptying database"
	psql -d $(USER) -q -f $(SRC_DIRECTORY)/clean.sql
	@echo "Successfully deleted data"



.PHONY: setup_postgres