import copy

sg1prefers = {
    't1':  ['s1', 's5', 's3', 's4', 's6', 's2', 's8', 's7'],
    't2':  ['s3', 's8', 's1', 's4', 's5', 's6', 's2', 's7'],
    't3':  ['s8', 's5', 's1', 's4', 's2', 's6',  's7', 's3'],
    't4':  ['s6', 's4', 's7', 's8', 's5', 's2', 's3', 's1'],
    't5':   ['s4', 's2', 's3', 's6', 's5', 's1', 's8', 's7'],
    't6': ['s2', 's1', 's4', 's7', 's5',  's3', 's8', 's6'],
    't7':  ['s7', 's5', 's2', 's3', 's1', 's4', 's8', 's6'],
    't8':  ['s1', 's5', 's8', 's6', 's3', 's2', 's7', 's4']
    }

sg2prefers = {
        's1':  ['t2', 't6', 't7', 't1', 't4', 't5', 't3', 't8'],
        's2':  ['t2', 't1', 't3', 't6', 't7', 't4', 't5', 't8'],
        's3': ['t6', 'bt2', 't5', 't7', 't8', 't3', 't1', 't4'],
        's4':  ['t6', 't3', 't1', 't8', 't7', 't4', 't2', 't5'],
        's5':  ['t8', 't6', 't4', 't1', 't7', 't3', 't5', 't2'],
        's6':  ['t2', 't1', 't5', 't4', 't6', 't7', 't3', 't8'],
        's7':  ['t7', 't8', 't6', 't2', 't1', 't3', 't5', 't4'],
        's8': ['t7', 't2', 't1', 't4', 't8', 't5', 't3', 't6'],
    }
sg1 = sorted(sg1prefers.keys())
sg2 = sorted(sg2prefers.keys())


def check(matched):
    inversematched = dict((v, k) for k, v in matched.items())
    for groupabc, groupdef in matched.items():
        groupdeflikes = sg2prefers[groupdef]
        groupdefikesbetter = groupdeflikes[:groupdeflikes.index(groupabc)]
        groupabclikes = sg1prefers[groupabc]
        groupabclikesbetter = groupabclikes[:groupabclikes.index(groupdef)]
        for x in groupdefikesbetter:
            xsrival = inversematched[x]
            xlikes = sg1prefers[x]
            if xlikes.index(xsrival) > xlikes.index(groupdef):
                print("%s and %s prefer each other better than "
                      "their present rivals: %s and %s, respectively"
                      % (groupdef, x, groupabc, xsrival))
                return False
        for y in groupabclikesbetter:
            ysrival = matched[y]
            ylikes = sg2prefers[y]
            if ylikes.index(ysrival) > ylikes.index(groupabc):
                print("%s and %s prefer each other better than "
                      "their present rivals: %s and %s, respectively"
                      % (groupabc, y, groupdef, ysrival))
                return False
    return True


def matchmaker():
    xsfree = sg1[:]
    matched = {}
    sg1prefers2 = copy.deepcopy(sg1prefers)
    sg2prefers2 = copy.deepcopy(sg2prefers)
    while xsfree:
        x = xsfree.pop(0)
        xslist = sg1prefers2[x]
        y = xslist.pop(0)
        therival = matched.get(y)
        if not therival:
            # She's free
            matched[y] = x
            print("  %s and %s" % (x, y))
        else:
            # The bounder proposes to an engaged lass!
            yslist = sg2prefers2[y]
            if yslist.index(therival) > yslist.index(x):
                # She prefers new guy
                matched[y] = x
                print("  %s dumped %s for %s" % (y, therival, x))
                if sg1prefers2[therival]:
                    # Ex has more girls to try
                    xsfree.append(therival)
            else:
                # She is faithful to old fiance
                if xslist:
                    # Look again
                    xsfree.append(x)
    return matched

print('\nMatches:')


matched = matchmaker()

print('\nCompetitions:')
print('  ' + ',\n  '.join('%s is competed to %s' % match
                          for match in sorted(matched.items())))
print()
print('Competition stability check PASSED'
      if check(matched) else 'Engagement stability check FAILED')

print('\n\nSwapping two fiances to introduce an error')
matched[sg2[0]], matched[sg2[1]] = matched[sg2[1]], matched[sg2[0]]
for y in sg2[:2]:
    print('  %s is now competed to %s' % (y, matched[y]))
print()
print('Competition stability check PASSED'
      if check(matched) else 'Competition stability check FAILED')
