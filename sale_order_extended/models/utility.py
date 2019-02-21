# -*- coding: utf-8 -*-
# © 2019 Didotech srl (www.didotech.com)


def set_sequence(lines):
    sequence = 10
    previous_sequence = 0
    update = False

    for line in lines:
        if line[0] in (1, 4, 6):
            update = True
            break

    for line in lines:
        if line[0] == 0:
            if line[2]['sequence'] == sequence:
                sequence += 10
            elif line[2]['sequence'] > sequence:
                next_sequence = line[2]['sequence'] / 10 * 10 + 10
                if line[2]['sequence'] / 10 * 10 == line[2]['sequence']:
                    line[2]['sequence'] = sequence
                sequence = next_sequence
            else:
                if update:
                    if line[2]['sequence'] <= previous_sequence:
                        line[2]['sequence'] = previous_sequence + 2
                        if line[2]['sequence'] > sequence:
                            sequence = line[2]['sequence'] + 10

                    previous_sequence = line[2]['sequence']
                else:
                    line[2]['sequence'] = sequence
                    previous_sequence = sequence
                    sequence += 10
        elif line[0] == 4:
            sequence += 10

    return lines
