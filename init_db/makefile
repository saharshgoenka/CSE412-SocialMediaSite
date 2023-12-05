OUTPUTS = $(sort $(wildcard outputs/*.txt))
QUESTIONS = $(patsubst outputs/%.txt,%,$(OUTPUTS))
MAKEFILE_PATH = /Users/mitsuakifukuzaki/Desktop/Hub/Programming/School/412/CSE412-SocialMediaSite/init_db/makefile
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
	psql -d $(USER) -q -f /Users/mitsuakifukuzaki/Desktop/Hub/Programming/School/412/CSE412-SocialMediaSite/init_db/setup.sql

clean_postgres:
	@echo "dropping tables"
	psql -d $(USER) -q -f /Users/mitsuakifukuzaki/Desktop/Hub/Programming/School/412/CSE412-SocialMediaSite/init_db/clean.sql


.PHONY: setup_postgres