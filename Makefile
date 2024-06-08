-include env

.SECONDEXPANSION:
.SUFFIXES:

PYTHON=py -3

.PHONY: default
default: ruby-online ruby-full

define postprocess
$(PYTHON) -c 'from rubyquest import *; encoolen("./$(1)/")'
endef

.PHONY: ruby-full
ruby-full:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py $(STORY_ID)
	# $(call postprocess,$(STORY_NAME))
	env MOD_TITLE="$(STORY_NAME)" \
	  j2 mod.js.j2 --print > "$(STORY_NAME)/mod.js"

.PHONY: ruby-online
ruby-online:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py $(STORY_ID) --online
	# $(call postprocess,$(STORY_NAME)_online)
	env MOD_TITLE="$(STORY_NAME) (online)" \
	  j2 mod.js.j2 --print > "$(STORY_NAME)_online/mod.js"