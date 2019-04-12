# coding: utf8
from bs4 import BeautifulSoup
from requests import get
from tag_mapper import TagMapper
import os

class MediumToMarkdown:
    def __init__(self, post_url):
        self.post_url = post_url

    def transform(self, fpath='./'):
        responses, url = self.medium_post()
        fname = '-'.join(url.split('/?')[0].split('/')[-1].split('-')[:-1])
        fname = os.path.join(fpath, fname)
        markdown_file = open(f"{fname}.md", "w+", encoding="utf8")
        for section in responses:
            for tag in section:
                # skip author infomation
                if tag.name == 'div' and 'uiScale-caption--regular' in tag["class"]:
                    continue
                markdown_tag = TagMapper(tag).to_markdown()
                if markdown_tag:
                    markdown_file.write(markdown_tag)
                markdown_file.write("\n\n")

        markdown_file.close()

    def medium_post(self):
        responses = self.medium_post_response()
        url = responses.url
        # if 'medium.com' in url:
        self.tag, self.class_ = 'div', 'sectionLayout--insetColumn'
        if 'linkedin.com' in url:
            self.tag, self.class_ = 'section', 'article-body'
        post_content = responses.content
        soup = BeautifulSoup(post_content, 'lxml')
        return soup.find_all(self.tag, {"class": self.class_}), url

    def medium_post_response(self):
        return get(self.post_url, stream=True)
