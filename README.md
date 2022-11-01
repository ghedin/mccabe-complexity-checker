# mccabe-complexity-checker
A CLI tool that makes it easier to use mccabe complexity checker (for Python) available at https://github.com/PyCQA/mccabe in larger code-bases.

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
me@host:/$ python3 complexity_checker.py --min=1  --dir=./sample/
```

| file                           | method                                |   complexity | score   |
|--------------------------------|---------------------------------------|--------------|---------|
| ./sample/complexity_checker.py | CaptureStdout.__enter__               |            1 | LOW     |
| ./sample/complexity_checker.py | CaptureStdout.__exit__                |            1 | LOW     |
| ./sample/complexity_checker.py | FileSeeker.__init__                   |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityChecker.__init__            |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityChecker._check_file         |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityChecker.run                 |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport.__init__             |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport._sort_by_complexity  |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport._output_as_table     |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport._write_to_file       |            1 | LOW     |
| ./sample/complexity_checker.py | ComplexityChecker._check_target_files |            2 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport._output_as_csv       |            2 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport.asTable              |            2 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport.asCSV                |            2 | LOW     |
| ./sample/complexity_checker.py | 143                                   |            2 | LOW     |
| ./sample/complexity_checker.py | FileSeeker.is_black_listed            |            3 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport._parse_mccabe_output |            3 | LOW     |
| ./sample/complexity_checker.py | FileSeeker.run                        |            4 | LOW     |
| ./sample/complexity_checker.py | ComplexityReport._get_complexity_rate |            5 | LOW     |
