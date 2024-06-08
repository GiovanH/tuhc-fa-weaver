-include env

.SECONDEXPANSION:
.SUFFIXES:

PYTHON=py -3

.PHONY: default
default: mspfa-online mspfa-full

define postprocess
sed -i $(1)/story.yaml -e \
  's|https://pipe.miroware.io/60e5694ca5f8ec784408eb80|https://file.garden/YOVpTKX47HhECOuA|g'
endef

.PHONY: mspfa-full
mspfa-full:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py $(STORY_ID)
	$(call postprocess,"$(STORY_NAME)")
	env MOD_TITLE="$(STORY_NAME)" \
	  j2 mod.js.j2 --print > "$(STORY_NAME)/mod.js"

.PHONY: mspfa-online
mspfa-online:
	$(PYTHON) $(TUHC_DIR)/tools/mspfa/mspfa.py $(STORY_ID) --online
	$(call postprocess,"$(STORY_NAME)_online")
	env MOD_TITLE="$(STORY_NAME) (online)" \
	  j2 mod.js.j2 --print > "$(STORY_NAME)_online/mod.js"