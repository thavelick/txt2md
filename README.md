# txt2md

(enventually) convert arbitrarily formatted text files to markdown. They can 
then be converted using standarded utilities to other formats like html, pdf
or epub for easy reading on phones, ereaders or comforatably in a web browser
in any size of window.

## Motivation
I often stumble across text files that are designed to be viewed through a 
terminal with a fixed-size font. Here are some examples:
- https://github.com/kisslinux/website/blob/master/site/wiki/package-manager.txt
- https://www.rfc-editor.org/rfc/rfc2616.txt and other rfcs
- https://gamefaqs.gamespot.com/snes/563538-chrono-trigger/faqs/25492

These files look great in a terminal but look awful on a phone or e-reader. 
The idea here is to create a program that an take a semi-arbitrary text file and
convert it to markdown for easy convesion to other format.

## Attribution
* unwrap algorithm from Gregory C Benison,  
    https://github.com/gbenison/Line-unwrap/

## Resources
* To identify nearly duplicate lines:
  * https://python-ssdeep.readthedocs.io/
  * could be useful for removing page header and footers on documents like rfcs

## Tasks
- [x] "unwrap" text that has been wrapped at a fixed width
  - [x] Figure out how to do it when we know the width up front
  - [x] Make sure divisions between paragraphs are retained 
  - [x] Ensure intentionally short lines are not unwrapped
- [x] unwrap text wrapped to an arbitrary width
- [ ] Identify and convret headlines to Markdown
  - [ ] Don't destroy existing markdown style headlines
  - [ ] Convert under-line style headlines
  - [ ] Convert over-and-under-line style headlines
  - [ ] Convert block sytle headlines
- [ ] Identify and put ascii art in "code" blocks
- [ ] Remove repetitive page headers 
- [ ] Try to determine emphasis of headlines and convert to corresponding markdo
wn subheadlines  
- [ ] Make it possible to add new tests just by adding example test files and 
      expected output files
