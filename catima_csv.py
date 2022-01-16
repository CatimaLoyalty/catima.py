def parse_csv_line(line):
    output = ['']
    last = ''
    in_quotes = False
    previous_quote = False

    for character in line:
        if previous_quote:
            previous_quote = False
            if character == '"':
                output[-1] += '"'
                continue
            else:
                in_quotes = False
        
        if character == ',' and not in_quotes:
            output.append('')
        elif character == '"':
            if not in_quotes:
                in_quotes = True
            else:
                previous_quote = True
        else:
            output[-1] += character

    return output


