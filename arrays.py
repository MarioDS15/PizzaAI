def compareArrays(verified, new):
    difference = False
    if len(new) < len(verified):
        return False
    for i in range(len(verified)):
        if verified[i] != new[i]:
            return False
    if len(verified) == len(new):
        return False
    return True

def organize(lst):
    if not lst:
        return []
    print("Before Organize: ", lst)
    result = [lst[0]]
    count = 1

    for i in range(1, len(lst)):
        if lst[i] == lst[i-1]:
            count += 1
        else:
            count = 1

        if count % 2 != 0:
            result.append(lst[i])
    cordArray = [cord for cord in lst if cord]
    print("After Organize: ", cordArray)
    return cordArray