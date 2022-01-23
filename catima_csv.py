class CatimaCSVSyntaxError(BaseException):
    pass


def parse_csv_line(line):
    output = [""]
    last = ""
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

        if character == "," and not in_quotes:
            output.append("")
        elif character == '"':
            if not in_quotes:
                in_quotes = True
            else:
                previous_quote = True
        else:
            output[-1] += character

    return output


def get_dicts(lines):
    title = parse_csv_line(lines[0])
    data = [parse_csv_line(line) for line in lines[1:]]

    line_dicts = []
    for line in data:
        if len(line) != len(title):
            raise CatimaCSVSyntaxError(
                "table entries must be the same length as header"
            )

        line_dict = {}
        for field_id, field_value in enumerate(line):
            line_dict[title[field_id]] = field_value
        line_dicts.append(line_dict)

    return line_dicts


def split_at_blank_lines(lines):
    line_groups = [[]]

    for line in lines:
        line = line.strip()
        if not line:
            line_groups.append([])
        else:
            line_groups[-1].append(line)

    if len(line_groups) != 4:
        raise CatimaCSVSyntaxError("file must have 4 line groups")

    if len(line_groups[0]) != 1 or line_groups[0][0] != "2":
        raise CatimaCSVSyntaxError(
            "file must start with `2` followed by a blank line (`2\\n\\n`)"
        )

    if line_groups[1][0] != "_id":
        raise CatimaCSVSyntaxError("invalid table header for groups database")

    if (
        line_groups[2][0]
        != '_id,store,note,expiry,balance,balancetype,cardid,barcodeid,barcodetype,headercolor,starstatus,lastused'
    ):
        raise CatimaCSVSyntaxError("invalid table header for cards database")

    if line_groups[3][0] != "cardId,groupId":
        raise CatimaCSVSyntaxError("invalid table header for card-to-group database")

    return line_groups[1:]


def parse_csv(lines):
    line_groups = split_at_blank_lines(lines)
    tables = []
    for line_group in line_groups:
        tables.append(get_dicts(line_group))

    return tables

def quote(item):
    if ',' in item or '"' in item:
        item = item.replace('"', '""')
        return f'"{item}"'
    else:
        return item

def quote_row(row):
    return ','.join([quote(item) for item in row])

def generate_card_row(card, card_id=1):
    return quote_row(card.csv_row(card_id))
