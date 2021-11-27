#!/bin/python3
import fileinput
import re

from dataclasses import dataclass
from enum import Enum
from pprint import pprint
from typing import Iterable


class BlockCategory(Enum):
    UNKNOWN = 0
    NORMAL_TEXT = 1
    PAGE_HEADING = 2


@dataclass
class Block:
    category: BlockCategory = BlockCategory.UNKNOWN
    content: str = ''

def main(lines: Iterable[str]) -> None:
    blocks = tokenize_blocks(lines)
    blocks = identify_normal_text(blocks)
    blocks = identify_page_headings(blocks)
    blocks = remove_by_category(blocks, BlockCategory.PAGE_HEADING)
    text = join_blocks(blocks)
    # text = unwrap(text)
    print(text.strip())


NEWLINES_RE = re.compile(r"\n{2,}")  # two or more "\n" characters
def split_sections(input_text=""):
    # From: https://stackoverflow.com/a/64863601
    no_newlines = input_text.strip("\n")  # remove leading and trailing "\n"
    split_text = NEWLINES_RE.split(no_newlines)  # regex splitting

    sections = [p + "\n" for p in split_text if p.strip()]
    # p + "\n" ensures that all lines in the section end with a newline
    # p.strip() == True if section has other characters than whitespace

    return sections

def tokenize_blocks(lines: Iterable[str]) -> Iterable[Block]:
    blocks: Iterable[Block] = []

    sections = split_sections(''.join(lines))
    for section in sections:
        block = Block(content=section)
        blocks.append(block)

    return blocks

def join_blocks(blocks: Iterable[Block]) -> str:
    return "\n".join([
        block.content for block in blocks
    ])

def remove_by_category(
            blocks: Iterable[Block], 
            remove: BlockCategory
        ) -> Iterable[Block]:
    return [ b for b in blocks if not b.category == remove ]

def identify_page_headings(blocks: Iterable[Block]) -> Iterable[Block]:
    counts = {}
    # Figure out how many of each block there are
    for block in blocks:
        counts[block.content] = counts.get(block.content, 0) + 1

    # Now flag the blocks with the heading category
    for block in blocks:
        if block.category != BlockCategory.UNKNOWN:
            continue
        if counts.get(block.content, 0) > 2:
            block.category = BlockCategory.PAGE_HEADING
    
    return blocks

ALPHA_RE = re.compile(r'[A-Za-z]')
def is_mostly_letters(text, threshold=0.75):
    clean_text = text.strip()
    total_count = len(clean_text)
    alpha_count = 0
    for char in clean_text:
        if ALPHA_RE.match(char):
            alpha_count += 1
    return alpha_count / total_count > threshold

def identify_normal_text(blocks: Iterable[Block]) -> Iterable[Block]:
    for block in blocks:
        if block.category != BlockCategory.UNKNOWN:
            return
        is_normal_text = is_mostly_letters(block.content)
        if is_normal_text: 
            block.category = BlockCategory.NORMAL_TEXT
    return blocks

if __name__ == '__main__':
    main(fileinput.input())
