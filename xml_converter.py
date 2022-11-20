import sys


def get_val(lst, index):
    try:
        val = lst[index]
        return val.rstrip()  # Strip trailing
    except IndexError:
        return ''


def serialize(k, v, indent=0):
    return ' ' * 2 * indent + f'<{k}>{v}</{k}>\n'


def sort_family_keys(family_lst):
    """ Sorts the keys of each family dict. """
    family_sorted = []
    for dct in family_lst:
        new_dict = {}
        for k in ['name', 'born', 'address', 'phone']:
            if k in dct:
                new_dict[k] = dct[k]
        family_sorted.append(new_dict)
    return family_sorted


def sort_person_keys(person_dct):
    """ Sorts the keys of person_dct. """
    person_dct_sorted = {}
    for key in ['firstname', 'lastname', 'address', 'phone', 'family']:
        if key in person_dct:
            person_dct_sorted[key] = person_dct[key]
    return person_dct_sorted


def dct_2_xml(dct, indent=0):
    """ Iterates over dxt to create and return a list with xml formatted text. """
    lines = []
    for k, v in dct.items():
        if isinstance(v, str):
            lines.append(serialize(k, v, indent))
        elif isinstance(v, list):
            for i in v:
                lines.append(' ' * 2 * indent + f'<{k}>\n')
                lines.extend(dct_2_xml(i, indent + 1))
                lines.append(' ' * 2 * indent + f'</{k}>\n')
        elif isinstance(v, dict):
            lines.append(' ' * 2 * indent + f'<{k}>\n')
            lines.extend(dct_2_xml(v, indent + 1))
            lines.append(' ' * 2 * indent + f'</{k}>\n')
    return lines


def main(fpath):

    # Read input file
    with open(fpath, 'r') as fp:
        lines = fp.readlines()

    person_lst = []  # List to hold person_dct's
    person_dct = {}  # Dict to hold person info
    for ln in lines:
        ln_split = ln.split('|')
        key = ln_split[0]
        vals = ln_split[1:]

        if key == 'P':
            if person_dct:
                # Add person dict to person_lst
                family_sorted = sort_family_keys(family_lst)
                person_dct['family'] = family_sorted
                person_sorted = sort_person_keys(person_dct)
                person_lst.append(person_sorted)

            # Create a new person_dct and reset family_lst and family_dct
            person_dct = {'firstname': get_val(vals, 0), 'lastname': get_val(vals, 1)}
            family_lst = []
            family_dct = {}

        elif key == 'F':
            # Append existing family_dct to family_lst and create a new family_dct
            if family_dct:
                family_lst.append(family_dct)
            family_dct = {'name': get_val(vals, 0), 'born': get_val(vals, 1)}

        elif key == 'T':
            phone_dct = {'mobile': get_val(vals, 0), 'landline': get_val(vals, 1)}
            # Set phone_dct in family_dct if possible, otherwise set in person_dct
            if family_dct:
                family_dct['phone'] = phone_dct
            else:
                person_dct['phone'] = phone_dct

        elif key == 'A':
            address_dct = {'street': get_val(vals, 0), 'city': get_val(vals, 1), 'zip': get_val(vals, 2)}
            # Set address_dct in family_dct if possible, otherwise set in person_dct
            if family_dct:
                family_dct['address'] = address_dct
            else:
                person_dct['address'] = address_dct

    # Add last person dict to person_lst
    family_sorted = sort_family_keys(family_lst)
    person_dct['family'] = family_sorted
    person_sorted = sort_person_keys(person_dct)
    person_lst.append(person_sorted)

    # Create dict to convert to xml
    dict_2_convert = {'people': {'person': person_lst}}

    # Convert dict to xml lines
    lines = dct_2_xml(dict_2_convert)

    # Write lines
    with open('out.xml', 'w') as fp:
        fp.writelines(lines)


if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) > 1:
        print(f'ERROR: The program takes only one positional argument ({len(argv)} was given)')
        sys.exit(1)
    main(argv[0])
