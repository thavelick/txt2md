#!/bin/python3
'convert arbitrarily formatted text files to markdown.'

import fileinput
import re

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class BlockCategory(Enum):
    'track the type of a block of text.'

    UNKNOWN = 0
    NORMAL_TEXT = 1
    PAGE_HEADING = 2

@dataclass
class Block:
    'a block of text that will be converted to markdown as a unit.'

    category: BlockCategory = BlockCategory.UNKNOWN
    content: str = ''

def main(lines: Iterable[str]) -> None:
    'convert `lines` to markdown'

    blocks = tokenize_blocks(lines)
    blocks = identify_normal_text(blocks)
    blocks = identify_page_headings(blocks)
    blocks = remove_by_category(blocks, BlockCategory.PAGE_HEADING)
    text = join_blocks(blocks)
    # text = unwrap(text)
    print(text.strip())

NEWLINES_RE = re.compile(r"\n{2,}")  # two or more "\n" characters
def split_sections(input_text=""):
    'split the given input into sections specified by double newlines.'

    # From: https://stackoverflow.com/a/64863601
    no_newlines = input_text.strip("\n")  # remove leading and trailing "\n"
    split_text = NEWLINES_RE.split(no_newlines)  # regex splitting

    sections = [p + "\n" for p in split_text if p.strip()]
    # p + "\n" ensures that all lines in the section end with a newline
    # p.strip() == True if section has other characters than whitespace

    return sections

def tokenize_blocks(lines: Iterable[str]) -> Iterable[Block]:
    'break down `lines` into blocks to be later parsed.'

    blocks: Iterable[Block] = []
    sections = split_sections(''.join(lines))
    for section in sections:
        block = Block(content=section)
        blocks.append(block)

    return blocks

def join_blocks(blocks: Iterable[Block]) -> str:
    'join blocks back together into one chunck of text.'

    return "\n".join([
        block.content for block in blocks
    ])

def remove_by_category(
            blocks: Iterable[Block],
            remove: BlockCategory
        ) -> Iterable[Block]:
    'remove blocks of a given category from a list'

    return [ b for b in blocks if not b.category == remove ]

def identify_page_headings(blocks: Iterable[Block]) -> Iterable[Block]:
    'mark blocks that are frequently repeated as page headings.'

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
    'returns True if `text` is alphanumeric over a given threshold.'

    clean_text = text.strip()
    total_count = len(clean_text)
    alpha_count = 0
    for char in clean_text:
        if ALPHA_RE.match(char):
            alpha_count += 1
    return alpha_count / total_count > threshold

def identify_normal_text(blocks: Iterable[Block]) -> Iterable[Block]:
    'mark unknown blocks that look like prose as normal text.'

    for block in blocks:
        if block.category != BlockCategory.UNKNOWN:
            continue
        is_normal_text = is_mostly_letters(block.content)
        if is_normal_text:
            block.category = BlockCategory.NORMAL_TEXT
    return blocks

if __name__ == '__main__':
    main(fileinput.input())
