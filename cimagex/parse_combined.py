import re


class ParseCombined():
    def parse_file(self, filename, type='protein'):

        self.type = type

        with open(filename) as combined_dta:
            # ditch headings
            headings = combined_dta.readline()
            data = combined_dta.readlines()

            return self.parse_data(data)

    def parse_data(self, data):
        groups = []
        header_pattern = re.compile('^\d.+')

        for line in data:
            line_info = [ x.strip() for x in re.split('\t+', line.strip()) if len(x.strip()) ]

            # if we've reached a group header
            if header_pattern.match(line):
                groups.append(self._extract_header(line_info))
            # if we've reached a subgroup
            else:
                # append peptide to last group
                groups[-1]['peptides'].append(self._extract_line_data(line_info))

        return groups

    def _extract_header(self, line):
        if self.type == 'protein':
            return {
                'uniprot_id': line[1],
                'description': line[2],
                'symbol': line[3],
                'mean_ratio': float(line[4]),
                'peptides': []
            }
        elif self.type == 'peptide':
            return {
                'sequence': line[1],
                'mean_ratio': line[2],
                'peptides': []
            }

    def _extract_line_data(self, line):
        if self.type == 'protein':
            peptide_keys = [
                'sequence', 'mass', 'mr', 'sd', 'mean', 'noqp', 'run',
                'charge', 'segment', 'link'
            ]
        elif self.type == 'peptide':
            peptide_keys = [
                'uniprot_id', 'description', 'symbol', 'sequence',
                'mass', 'mr', 'sd', 'run', 'charge', 'segment', 'link'
            ]

        return dict(zip(peptide_keys, line))
