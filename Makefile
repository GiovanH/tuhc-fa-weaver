-include env_ruby

.SECONDEXPANSION:
.SUFFIXES:

PYTHON=py -3

.PHONY: default
default: ruby-online ruby-full nan-online nan-full

define postprocess
$(PYTHON) -c 'from rubyquest import *; fix_timestamps("./$(1)/")'
endef

.PHONY: ruby-full
ruby-full:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py $(STORY_ID)
	$(call postprocess,$(STORY_NAME))
	env MOD_TITLE="$(STORY_NAME)" \
	  j2 mod.js.j2 --print > "$(STORY_NAME)/mod.js"

.PHONY: ruby-online
ruby-online:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py $(STORY_ID) --online
	$(call postprocess,$(STORY_NAME)_online)
	env MOD_TITLE="$(STORY_NAME) (online)" \
	  j2 mod.js.j2 --print > "$(STORY_NAME)_online/mod.js"

# Extra adventure

.PHONY: nan-full
nan-full:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py 23588
	# $(call postprocess,$(STORY_NAME))
	echo -e "\n} // manual fix\n" >> "Nan Quest/adventure.css"
	echo -e "} // manual fix\n" >> "Nan Quest/adventure.scss"
	. ./env_nan && env MOD_TITLE="Nan Quest" \
	  j2 mod.js.j2 --print > "Nan Quest/mod.js"

.PHONY: nan-online
nan-online:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py 23588 --online
	# $(call postprocess,Nan Quest_online)
	echo -e "\n} // manual fix\n" >> "Nan Quest_online/adventure.css"
	echo -e "} // manual fix\n" >> "Nan Quest_online/adventure.scss"
	. ./env_nan && env MOD_TITLE="Nan Quest (online)" \
	  j2 mod.js.j2 --print > "Nan Quest_online/mod.js"