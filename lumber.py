#! /bin/python

class TooBig(Exception):
    pass

msg = \
    """
        ###########################################################################

        Lumber Calculator:
            Enter the MAX length per BOARD (in feet)
            Then enter the cut lengths (in inches)
            I'll spit out how many boards you need

        ###########################################################################
    """

def remove_and_add(remove_from, add_to, *args):
    for arg in args:
        remove_from.remove(arg)
        add_to.append(arg)


def in_order(arr):
    lengths = [ ]
    current_lengths = [ arr.pop(0) ]
    remaining = 0
    while len(arr) > 0:
        remaining = board_inches - sum(current_lengths)
        possibles = [x for x in arr if x < remaining]

        # if we have no possible fits for the remaining area start the next board
        if len(possibles) == 0:
            current_lengths.append(remaining)
            lengths.append(current_lengths[:])
            current_lengths = [ arr.pop(0) ]
            continue

        # get a count of cuts that are greater than half of the remaining length
        greater_than_half = sorted(
            [x for x in possibles if (x > remaining / 2) and ((sum(current_lengths) + x) <= board_inches)],
            reverse=True)
        gth_remaining = remaining
        if len(greater_than_half) > 0:
            gth1 = greater_than_half.pop(0)
            gth_remaining -= gth1
            # if we find that other lengths can definitely be cut from this board, accept it and move on
            more_will_fit = [x for x in possibles if x <= gth_remaining]
            if len(more_will_fit) > 0:
                remove_and_add(arr, current_lengths, gth1)
                continue

        # get a list of cuts that less than half of the remaining length
        less_by_half = sorted([x for x in possibles if x <= (remaining/2)], reverse=True)
        lbh_remaining = remaining
        if len(less_by_half) > 1:
            lbh1 = less_by_half.pop(0)
            lbh2 = less_by_half.pop(0)
            lbh_remaining -= lbh1 + lbh2
            # if we find that other lengths can definitely be cut from this board, accept it and move on
            more_will_fit = [x for x in possibles if x <= lbh_remaining]
            if len(more_will_fit) > 0:
                remove_and_add(arr, current_lengths, lbh1, lbh2)
                continue

        # if they are competing, compare the remainders and append cut lengths
        if gth_remaining == remaining and lbh_remaining == remaining:
            current_lengths.append(remaining)
            lengths.append(current_lengths[:])
            current_lengths = [ arr.pop(0) ]
        elif gth_remaining < lbh_remaining:
            remove_and_add(arr, current_lengths, gth1)
        elif lbh_remaining < gth_remaining:
            remove_and_add(arr, current_lengths, lbh1, lbh2)

    if len(current_lengths) > 0:
        current_lengths.append(board_inches - sum(current_lengths))
        lengths.append(current_lengths)
    return lengths

def biggest_first(arr):
    return in_order(sorted(arr, reverse=True))

def smallest_first(arr):
    return in_order(sorted(arr))


print (msg)

board_length = input('\nenter the max board length (ft): ')
board_inches = int(board_length) * 12
total_cuts = [ ]
in_length = raw_input('enter the first cut length: ')
while in_length:
    if in_length == "" or in_length == "q": break
    try:
        value = float(in_length)
        if value > board_inches:
            raise TooBig('That one (%d) won\'t fit on a %s foot board' % value)
        total_cuts.append(value)
        in_length = raw_input('next: ')
    except TooBig, e:
        print e.message
    except:
        break


if len(total_cuts) > 0:
    in_order_boards = in_order(total_cuts[:])
    biggest_first_boards = biggest_first(total_cuts[:])
    smallest_first_boards = smallest_first(total_cuts[:])

cuts = [in_order_boards, biggest_first_boards, smallest_first_boards]

cuts = sorted(cuts, lambda x, y: cmp(len(x), len(y)))
least_boards = cuts[0]
for i in range(len(least_boards)):
    least_boards[i] = sorted(least_boards[i], reverse=True)

print "you can do that in %d boards like this: %s" % (len(least_boards), least_boards)


if __name__ == 'main':
    main()

