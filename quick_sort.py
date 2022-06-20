def quick_sort(array_list):
    length = len(array_list)
    if length <= 1:
        return array_list
    else:
        pivot = array_list.pop()
        
    items_greater = []
    items_lower = []
    
    for item in array_list:
        if item > pivot:
            items_greater.append(item)
        else:
            items_lower.append(item)
    
    return quick_sort(items_lower) + [pivot] + quick_sort(items_greater)



    