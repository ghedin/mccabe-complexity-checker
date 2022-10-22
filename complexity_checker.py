import os
from glob import glob
from io import StringIO
import sys
from tabulate import tabulate
from mccabe import main as mccabe_checker
from alive_progress import alive_bar as progress_bar
import optparse
from collections import namedtuple
from operator import attrgetter

Result = namedtuple('Result', ['file', 'method', 'complexity', 'rate'])


class CaptureStdout(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


class FileSeeker():
    def __init__(self, input_directory, pattern='*.py'):
        self.input_directory = input_directory
        self.pattern = pattern
        self.black_listed_dirs = ['v2/pytests', 'v2/migrations']

    def is_black_listed(self, path):
        for entry in self.black_listed_dirs:
            if entry in path:
                return True
        return False

    def run(self):
        with progress_bar() as update_progress_bar:
            results = []
            for entry in os.walk(self.input_directory):
                current_directory = entry[0]
                if self.is_black_listed(current_directory):
                    continue
                for file in glob(os.path.join(current_directory, self.pattern)):
                    results.append(file)
                    update_progress_bar()
            return results


class ComplexityChecker():
    def __init__(self, input_directory, min_threshold=5):
        self.input_directory = input_directory
        self.min_threshold = str(min_threshold)
        self.results = []

    def _check_target_files(self, target_files):
        with progress_bar() as update_progress_bar:
            for file in target_files:
                result = self._check_file(file)
                self.results.append([file, result])
                update_progress_bar()

    def _check_file(self, path):
        with CaptureStdout() as stdout:
            mccabe_checker([path, '-m', self.min_threshold])
        return stdout

    def run(self):
        files = FileSeeker(self.input_directory, '*.py').run()
        self._check_target_files(files)
        return self.results


class ComplexityReport():
    def __init__(self, complexityCheckerOutputArray, outputFile=None):
        self.input = complexityCheckerOutputArray
        self.outputFile = outputFile

    def _parse_mccabe_output(self):
        output = []
        for item in self.input:
            filename = item[0]
            functions = item[1]
            for function in functions:
                items = function.split(' ')
                functionName = items[1].replace("'", "").replace('"', '')
                functionComplexity = int(items[2].replace("'", ""))
                rate = self._get_complexity_rate(functionComplexity)
                entry = Result(file=filename,
                               method=functionName,
                               complexity=functionComplexity,
                               rate=rate)
                output.append(entry)
        return output

    def _get_complexity_rate(self, complexity):
        if complexity > 40:
            return "ULTRA HIGH"
        if complexity > 15:
            return "VERY HIGH"
        if complexity > 10:
            return "HIGH"
        if complexity > 6:
            return "MEDIUM"
        return "LOW"

    def _sort_by_complexity(self, result):
        return sorted(result, key=attrgetter('complexity'))

    def _output_as_csv(self):
        output = ''
        result = self._sort_by_complexity(self._parse_mccabe_output())
        for item in result:
            output += "{}, {}, {}, {}\n".format(item.file, item.method, item.complexity, item.rate)
        return output

    def _output_as_table(self):
        result = self._sort_by_complexity(self._parse_mccabe_output())
        headers = ['file', 'method', 'complexity', 'score']
        return tabulate(result, headers, tablefmt="github")

    def _write_to_file(self, contents):
        with open(self.outputFile, 'w') as f:
            f.write(contents)

    def asTable(self):
        output = self._output_as_table()
        if self.outputFile:
            self._write_to_file(output)
            return
        print(output)

    def asCSV(self):
        output = self._output_as_csv()
        if self.outputFile:
            self._write_to_file(output)
            return
        print(output)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', '--dir', action="store", dest="input_directory", help="Directory to be checked", default='./')
    parser.add_option('-o', '--output', action="store", dest="output_file", help="Output file", default=None)
    parser.add_option('-m', '--min', action="store", dest="min_threshold", help="Minimum Threshold for Ciclomatic Complexity", default=5)
    parser.add_option('-f', '--format', action="store", dest="format", help="table/csv", default='table')
    options, args = parser.parse_args()

    result = ComplexityChecker(options.input_directory, options.min_threshold).run()
    if options.format == 'table':
        ComplexityReport(result, options.output_file).asTable()
    else:
        ComplexityReport(result, options.output_file).asCSV()
