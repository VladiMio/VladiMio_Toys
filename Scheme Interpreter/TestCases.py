import Scheme

cases = {
    "(+ 1 2 3 4 5)": 1 + 2 + 3 + 4 + 5,
    "(- 1 2 3 4 5)": 1 - 2 - 3 - 4 - 5,
    "(* 1 2 3 4 5)": 1 * 2 * 3 * 4 * 5,
    "(/ 1 2 3 4 5)": 1 / 2 / 3 / 4 / 5,
}

casesList = list(cases.items())

isPass = True
for case in casesList:
    res = Scheme.scheme_eval(Scheme.parse(case[0]))
    if res != case[-1]:
        print("case %s failed, output %s" % (case[0], res))
        isPass &= False
    else:
        isPass &= True

if isPass:
    print("Congratulations! All Test Cases Passed! ")
