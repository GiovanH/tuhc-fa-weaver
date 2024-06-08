#!/bin/python3
# Run mspfa.py <story_slug> <mspfa_id>
# e.g. python3 mspfa.py "Felt" 21

# import re
import json
import os
# import requests
import bs4
# import urllib.parse
# import logging
# import difflib
# import itertools
# from urllib.parse import urlparse
# from lib import TriadLogger
import shutil
import traceback
# import cgi
import glob
import typing

import ruamel.yaml

yaml = ruamel.yaml.YAML()

# Sensible multiline representer
def _str_presenter(dumper, data):
    TAG_STR = 'tag:yaml.org,2002:str'
    if '\n' in data:
        return dumper.represent_scalar(TAG_STR, data, style='|')
    return dumper.represent_scalar(TAG_STR, data, style='"')


yaml.representer.add_representer(str, _str_presenter)


try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterator, *args, **kwargs):
        yield from iterator

wgetroot = 'L:/Archive/Homestuck/suptg.thisisnotatrueending.com/archive/'
all_lines = []
for html in tqdm(glob.glob(os.path.join(wgetroot, '*', '**.html'), recursive=True)):
    with open(html, 'r', encoding="utf-8") as fp:
        all_lines += fp.readlines()

with open('./alllines.txt', 'w', encoding="utf-8") as fp:
    for line in all_lines:
        fp.write(line + '\n')

with open('./ruby.json', 'r') as fp:
    ruby_dupes = json.load(fp)

known_pairs: typing.Mapping[str, str] = {}
for line in all_lines:
    if '<span class="commentpostername">Weaver</span>' in line:
        soup = bs4.BeautifulSoup(line)
        name = soup.find(class_='commentpostername')
        if name:
            name.decompose()
        trip = soup.find(class_='postertrip')
        if trip:
            trip.decompose()

        image_links = soup.select('span.filesize a')
        if image_links:
            filename: str = os.path.split(image_links[0]['href'])[1]
            # print(filename)
            for set in ruby_dupes['matchSets']:
                if any([
                    file['filePath'].endswith(filename)
                    for file in set['fileList']
                ]):
                    # print(set['fileList'])
                    assets = [
                        os.path.split(file['filePath'])[1]
                        for file in set['fileList']
                        if file['filePath'].startswith('TUHC')
                    ]
                    if assets:
                        if len(assets) > 1:
                            print("Identical:", assets)
                        else:
                            page_num = assets[0].split('_')[0].split('.')[0]
                            known_pairs[page_num] = filename
                        # print(assets[0])
        else:
            continue
            # raise NotImplementedError(soup)

# print(known_pairs)

all_docs: dict = {}
def docFor(page) -> bs4.BeautifulSoup:
    # print(page)

    textstrs = [s for s in page['b'].split('\n') if s and '[img]' not in s]
    query = textstrs[-1]
    try:
        line = [s for s in all_lines if query.replace(',', '&#44;') in s][0]
    except IndexError:
        try:
            query = textstrs[-2]
            line = [s for s in all_lines if query.replace(',', '&#44;') in s][0]
        except IndexError:
            print(query)
            raise
    soup = bs4.BeautifulSoup(line)
    return soup


def encoolen(mod_dir) -> None:
    story_yaml_path = os.path.join(mod_dir, "story.yaml")
    story_yaml_bakpath = story_yaml_path + ".orig"
    if not os.path.isfile(story_yaml_bakpath):
        shutil.copy2(story_yaml_path, story_yaml_bakpath)

    with open(story_yaml_bakpath, 'r', encoding="utf-8") as fp:
        story_data = yaml.load(fp)

    prev_match: typing.Optional[int] = None
    for page in story_data['p']:
        doc_time_match: typing.Optional[str] = known_pairs.get(str(page['i']))
        if isinstance(doc_time_match, str):
            doc_time: int = int(doc_time_match.split('.')[0])
            if prev_match:
                if doc_time < prev_match:
                    raise ValueError(f"{page}: Last doc_time {doc_time} < prev {prev_match}")
            assert (not prev_match) or doc_time >= prev_match
            page['d'] = doc_time
            prev_match = doc_time
        else:
            page['d'] = prev_match or page['d']
            # print("no known", page['i'], match, prev_match)
            try:
                soup = docFor(page)
                image_links = soup.select('span.filesize a')
                if image_links:
                    filename: typing.Optional[str] = os.path.split(image_links[0]['href'])[1]
                doc_time: int = int(filename.split('.')[0])
                if prev_match:
                    if doc_time < prev_match:
                        raise ValueError(f"{page}: Last doc_time {doc_time} < prev {prev_match}")
                assert (not prev_match) or doc_time >= prev_match
                page['d'] = doc_time
                prev_match = doc_time
            except Exception:
                traceback.print_exc()
                continue
        # try:
            # print(docFor(page))
        # except:
        #     continue

    with open(story_yaml_path, 'w', encoding="utf-8") as fp:
        yaml.dump(story_data, fp)


if __name__ == "__main__":
    try:
        encoolen("./Ruby Quest/")
    except KeyboardInterrupt:
        os.abort()
