# US Appendix

### Report Selection
A set of 4616 reports with study `US APPENDIX` were obtained from an old Oracle database called Clarity. The unique identifiers were a de-identified patient id and study id. There were some errors with the dump, including a file that ended suddenly, and duplicated study ids. To be completely safe, all duplicated records were removed. The entire process is detailed in [prep/prepare_minimal.py](prep/prepare_minimal.py).

### WordFish Upload
[Wordfish](http://www.github.com/radinformatics/whatisit) is an annotation tool, intended for purposes like these. The script [prep/upload_appendix.py](prep/upload_appendix.py) was used to upload the reports to a new collection in WordFish, without any Annotations or labels. A view will be developed to define these in the web interface.


