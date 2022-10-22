# mccabe-complexity-checker
A CLI tool that makes it easier to use mccabe complexity checker (for Python) available at https://github.com/PyCQA/mccabe

```
Usage: complexity_checker.py [options]

Options:
  -h, --help            show this help message and exit
  -d INPUT_DIRECTORY, --dir=INPUT_DIRECTORY
                        Directory to be checked
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        Output file
  -m MIN_THRESHOLD, --min=MIN_THRESHOLD
                        Minimum Threshold for Ciclomatic Complexity
  -f FORMAT, --format=FORMAT
                        table/csv
```

Examples:

```
me@host:/$ python3 complexity_checker.py --min=5  --dir=./mccabe-master/
```

| file                             | method                                 |   complexity | score   |
|----------------------------------|----------------------------------------|--------------|---------|
| ./mccabe-master/mccabe.py | PathGraphingAstVisitor._subgraph_parse |            5 | LOW     |
| ./mccabe-master/mccabe.py | get_code_complexity                    |            5 | LOW     |
| ./mccabe-master/mccabe.py | _read                                  |            5 | LOW     |
| ./mccabe-master/mccabe.py | main                                   |            7 | MEDIUM  |
