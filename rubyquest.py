#!/bin/python3

import json
import os
import bs4
import shutil
import traceback
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
    def tqdm(iterator, *args, **kwargs):  # type: ignore[no-redef]  # noqa: ARG001
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


map_page_to_image: typing.Dict[str, str] = {}
for line in all_lines:
    if '<span class="commentpostername">Weaver</span>' in line:
        soup = bs4.BeautifulSoup(line)
        name: bs4.Tag = soup.find(class_='commentpostername')  # type: ignore[assignment]
        if name:
            name.decompose()
        trip: bs4.Tag = soup.find(class_='postertrip')  # type: ignore[assignment]
        if trip:
            trip.decompose()

        image_links = soup.select('span.filesize a')
        if image_links:
            filename: str = os.path.split(image_links[0]['href'])[1]
            assert isinstance(filename, str)
            # print(filename)
            for dupeset in ruby_dupes['matchSets']:
                if any(
                    file['filePath'].endswith(filename)
                    for file in dupeset['fileList']
                ):
                    # print(dupeset['fileList'])
                    assets = [
                        os.path.split(file['filePath'])[1]
                        for file in dupeset['fileList']
                        if file['filePath'].startswith('TUHC')
                    ]
                    if assets:
                        if len(assets) > 1:
                            print("Identical:", assets)
                        else:
                            page_num: str = assets[0].split('_')[0].split('.')[0]
                            map_page_to_image[page_num] = filename
                        # print(assets[0])
        else:
            continue
            # raise NotImplementedError(soup)

# print(map_page_to_image)

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
            # print(textstrs, query)
            raise
    soup = bs4.BeautifulSoup(line)
    return soup


def fix_timestamps(mod_dir) -> None:
    story_yaml_path = os.path.join(mod_dir, "story.yaml")
    story_yaml_bakpath = story_yaml_path + ".orig"
    if not os.path.isfile(story_yaml_bakpath):
        shutil.copy2(story_yaml_path, story_yaml_bakpath)

    with open(story_yaml_bakpath, 'r', encoding="utf-8") as fp:
        story_data = yaml.load(fp)

    prev_doc_time: typing.Optional[int] = None
    for page in story_data['p'][1:]:
        doc_time_match: typing.Optional[str] = map_page_to_image.get(str(page['i']))

        if isinstance(doc_time_match, str):
            doc_time: int = int(doc_time_match.split('.')[0])
            if prev_doc_time:
                if doc_time < prev_doc_time:
                    # raise ValueError(f"{page}: Last doc_time {doc_time} < prev {prev_doc_time}")
                    print("[Matched] Shifting page time", doc_time, prev_doc_time, (prev_doc_time - doc_time), page)
                    # doc_time = prev_doc_time
            # assert (not prev_doc_time) or doc_time >= prev_doc_time
            page['d'] = doc_time
            prev_doc_time = doc_time

        else:
            page['d'] = prev_doc_time or page['d']
            # print("no known", page['i'], match, prev_doc_time)
            try:
                soup = docFor(page)
                image_links = soup.select('span.filesize a')
                if image_links:
                    filename: str = os.path.split(image_links[0]['href'])[1]
                    doc_time: int = int(filename.split('.')[0])
                if prev_doc_time:
                    if doc_time < prev_doc_time:
                        # raise ValueError(f"{page}: Last doc_time {doc_time} < prev {prev_doc_time}")
                        print("[Unmatched] Shifting page time", doc_time, prev_doc_time, (prev_doc_time - doc_time), page)
                        # doc_time = prev_doc_time
                # assert (not prev_doc_time) or doc_time >= prev_doc_time
                page['d'] = doc_time
                prev_doc_time = doc_time
            except Exception:
                # print(page)
                # raise
                # traceback.print_exc()
                continue
        # try:
            # print(docFor(page))
        # except:
        #     continue

    print("Saving...")
    with open(story_yaml_path, 'w', encoding="utf-8") as fp:
        yaml.dump(story_data, fp)


if __name__ == "__main__":
    try:
        fix_timestamps("./Ruby Quest/")
    except KeyboardInterrupt:
        os.abort()
