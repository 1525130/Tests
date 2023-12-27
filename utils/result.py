import os
import html
import string
import datetime
import platform
import unittest


class BaseTestResult(unittest.TextTestResult):
    def startTestRun(self):
        self.successes = []
        self.start_time = datetime.datetime.now()

    def addSuccess(self, test):
        self.successes.append(test)
        super().addSuccess(test)

    def stopTestRun(self):
        self.end_time = datetime.datetime.now()
        self.file_name = self.end_time.isoformat(sep='_', timespec='seconds').replace(':', '-')

        # statistic
        if self.testsRun:
            self.execute_rate = 1 - len(self.skipped) / self.testsRun
            self.pass_rate = (len(self.successes) + len(self.expectedFailures)) / (self.testsRun - len(self.skipped))
        else:
            self.execute_rate = 0
            self.pass_rate = 0

        if not os.path.exists('reports'):
            os.mkdir('reports')

    def printErrorList(self, flavour, errors):
        pass


class HTMLTestResult(BaseTestResult):
    def stopTestRun(self):
        super().stopTestRun()

        # test report
        report = '\n'
        report += '<h1>Test Report</h1>\n'

        # information
        report += '<h2>Information</h2>\n'
        report += f'<p>Start Time: {self.start_time.isoformat(sep=" ", timespec="seconds")}</p>\n'
        report += f'<p>End Time: {self.end_time.isoformat(sep=" ", timespec="seconds")}</p>\n'
        report += f'<p>Elapsed Time: {(self.end_time - self.start_time).total_seconds():.3f}s</p>\n'

        # environment
        report += '<h2>Environment</h2>\n'
        report += f'<p>Platform: {platform.platform()}</p>\n'
        report += f'<p>Python: {platform.python_version()}</p>\n'

        # statistic
        report += '<h2>Statistic</h2>\n'
        report += f'<p>Total Count: {self.testsRun}</p>\n'
        report += f'<p>Execute Rate: {self.execute_rate:.2%}</p>\n'
        report += f'<p>Pass Rate: {self.pass_rate:.2%}</p>\n'
        # statistic table
        report += '<table>\n'
        report += '<tr>\n' + \
                  '<th style="color: green">Success</th>\n' + \
                  '<th style="color: green">ExpectedFailure</th>\n' + \
                  '<th style="color: blue">Skip</th>\n' + \
                  '<th style="color: red">Error</th>\n' + \
                  '<th style="color: red">Failure</th>\n' + \
                  '<th style="color: red">UnexpectedSuccess</th>\n' + \
                  '</tr>\n'
        report += '<tr>\n' + \
                  f'<td>{len(self.successes)}</td>\n' + \
                  f'<td>{len(self.expectedFailures)}</td>\n' + \
                  f'<td>{len(self.skipped)}</td>\n' + \
                  f'<td>{len(self.errors)}</td>\n' + \
                  f'<td>{len(self.failures)}</td>\n' + \
                  f'<td>{len(self.unexpectedSuccesses)}</td>\n' + \
                  '</tr>\n'
        report += '</table>\n'

        # summary
        if self.testsRun:
            report += '<h2 id="Summary">Summary</h2>\n'
            report += '<table>\n'
            report += '<tr>\n' + \
                      '<th>Status</th>\n' + \
                      '<th>ID(file.class.method)</th>\n' + \
                      '<th>Short Description</th>\n' + \
                      '</tr>\n'
        for test, temp in self.errors:
            report += self.pretty_summary(status='red">Error', test=test)
        for test, temp in self.failures:
            report += self.pretty_summary(status='red">Failure', test=test)
        for test in self.unexpectedSuccesses:
            report += self.pretty_summary(status='red">UnexpectedSuccess', test=test)
        for test, temp in self.skipped:
            report += self.pretty_summary(status='blue">Skip', test=test)
        for test in self.successes:
            report += self.pretty_summary(status='green">Success', test=test)
        for test, temp in self.expectedFailures:
            report += self.pretty_summary(status='green">ExpectedFailure', test=test)
        if self.testsRun:
            report += '</table>\n'

        # detail
        if any([self.errors, self.failures, self.skipped, self.expectedFailures]):
            report += '<h2>Detail</h2>\n'
        if self.errors:
            report += '<h3>Error</h3>\n'
            for test, err in self.errors:
                report += f'<h4 id="{test.id()}">{test.id()}</h4>\n'
                report += f'<pre>\n{html.escape(err)}\n</pre>\n'
                report += '<p><a href="#Summary">Back to Summary</a></p>\n'
        if self.failures:
            report += '<h3>Failure</h3>\n'
            for test, err in self.failures:
                report += f'<h4 id="{test.id()}">{test.id()}</h4>\n'
                report += f'<pre>\n{html.escape(err)}\n</pre>\n'
                report += '<p><a href="#Summary">Back to Summary</a></p>\n'
        if self.skipped:
            report += '<h3>Skip</h3>\n'
            for test, reason in self.skipped:
                report += f'<h4 id="{test.id()}">{test.id()}</h4>\n'
                report += f'<p>Reason: {html.escape(reason)}</p>\n'
                report += '<p><a href="#Summary">Back to Summary</a></p>\n'
        if self.expectedFailures:
            report += '<h3>ExpectedFailure</h3>\n'
            for test, err in self.expectedFailures:
                report += f'<h4 id="{test.id()}">{test.id()}</h4>\n'
                report += f'<pre>\n{html.escape(err)}\n</pre>\n'
                report += '<p><a href="#Summary">Back to Summary</a></p>\n'

        with open('utils/template.html', 'r', encoding='utf-8') as f1, \
                open(f'reports/{self.file_name}.html', 'w', encoding='utf-8') as f2:
            f2.write(string.Template(f1.read()).substitute(title=self.file_name, report=report))

    def pretty_summary(self, status: str, test: unittest.TestCase):
        return '<tr>\n<td style="color: ' + '</td>\n<td>'.join([
            status,
            test.id() if 'Success' in status or 'UnexpectedSuccess' in status else f'<a href="#{test.id()}">{test.id()}</a>',
            html.escape(sd) if (sd := test.shortDescription()) else '',
        ]) + '</td>\n</tr>\n'


class MarkdownTestResult(BaseTestResult):
    def stopTestRun(self):
        super().stopTestRun()

        # test report
        report = ''
        report += '# Test Report\n\n'

        # information
        report += '## Information\n\n'
        report += f'Start Time: {self.start_time.isoformat(sep=" ", timespec="seconds")}\n\n'
        report += f'End Time: {self.end_time.isoformat(sep=" ", timespec="seconds")}\n\n'
        report += f'Elapsed Time: {(self.end_time - self.start_time).total_seconds():.3f}s\n\n'

        # environment
        report += '## Environment\n\n'
        report += f'Platform: {platform.platform()}\n\n'
        report += f'Python: {platform.python_version()}\n\n'

        # statistic
        report += '## Statistic\n\n'
        report += f'Total Count: {self.testsRun}\n\n'
        report += f'Execute Rate: {self.execute_rate:.2%}\n\n'
        report += f'Pass Rate: {self.pass_rate:.2%}\n\n'
        # statistic table
        report += '| <font color="green">Success</font> | <font color="green">ExpectedFailure</font> ' + \
                  '| <font color="blue">Skip</font> | <font color="red">Error</font> ' + \
                  '| <font color="red">Failure</font> | <font color="red">UnexpectedSuccess</font> |\n'
        report += '| ---- | ---- | ---- | ---- | ---- | ---- |\n'
        report += f'| {len(self.successes)} | {len(self.expectedFailures)} ' + \
                  f'| {len(self.skipped)} | {len(self.errors)} ' + \
                  f'| {len(self.failures)} | {len(self.unexpectedSuccesses)} |\n'
        report += '\n'

        # summary
        if self.testsRun:
            report += '## Summary\n\n'
            report += '| Status | ID(file.class.method) | Short Description |\n'
            report += '| ---- | ---- | ---- |\n'
        for test, temp in self.errors:
            report += self.pretty_summary(status='<font color="red">Error</font>', test=test)
        for test, temp in self.failures:
            report += self.pretty_summary(status='<font color="red">Failure</font>', test=test)
        for test in self.unexpectedSuccesses:
            report += self.pretty_summary(status='<font color="red">UnexpectedSuccess</font>', test=test)
        for test, temp in self.skipped:
            report += self.pretty_summary(status='<font color="blue">Skip</font>', test=test)
        for test in self.successes:
            report += self.pretty_summary(status='<font color="green">Success</font>', test=test)
        for test, temp in self.expectedFailures:
            report += self.pretty_summary(status='<font color="green">ExpectedFailure</font>', test=test)
        if self.testsRun:
            report += '\n'

        # detail
        if any([self.errors, self.failures, self.skipped, self.expectedFailures]):
            report += '## Detail\n\n'
        if self.errors:
            report += '### Error\n\n'
            for test, err in self.errors:
                report += f'#### {test.id()}\n\n'
                report += f'```python\n{err}\n```\n\n'
                report += '[Back to Summary](#Summary)\n\n'
        if self.failures:
            report += '### Failure\n\n'
            for test, err in self.failures:
                report += f'#### {test.id()}\n\n'
                report += f'```python\n{err}\n```\n\n'
                report += '[Back to Summary](#Summary)\n\n'
        if self.skipped:
            report += '### Skip\n\n'
            for test, reason in self.skipped:
                report += f'#### {test.id()}\n\n'
                report += f'Reason: {reason}\n\n'
                report += '[Back to Summary](#Summary)\n\n'
        if self.expectedFailures:
            report += '### ExpectedFailure\n\n'
            for test, err in self.expectedFailures:
                report += f'#### {test.id()}\n\n'
                report += f'```python\n{err}\n```\n\n'
                report += '[Back to Summary](#Summary)\n\n'

        with open(f'reports/{self.file_name}.md', 'w', encoding='utf-8') as f:
            f.write(report)

    def pretty_summary(self, status: str, test: unittest.TestCase):
        return '| ' + ' | '.join([
            status,
            test.id() if 'Success' in status or 'UnexpectedSuccess' in status else f'[{test.id()}](#{test.id()})',
            sd.replace('|', '') if (sd := test.shortDescription()) else '',
        ]) + ' |\n'
