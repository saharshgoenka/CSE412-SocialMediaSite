OUTPUTS = $(sort $(wildcard outputs/*.txt))
QUESTIONS = $(patsubst outputs/%.txt,%,$(OUTPUTS))
SRC_DIRECTORY = /Users/mitsuakifukuzaki/Desktop/Hub/Programming/School/412/CSE412-SocialMediaSite/init_db
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


clean_postgres:
	@echo "emptying database"
	psql -d $(USER) -q -f $(SRC_DIRECTORY)/clean.sql



.PHONY: setup_postgres