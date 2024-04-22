__all__ = ()


def merge_update_poll_results(new_results, old_results):
    """
    Merges poll results.
    
    Parameters
    ----------
    new_results : `None | list<PollResult>`
        New results.
    old_results : `None | list<PollResult>`
        Old results.
    
    Returns
    -------
    results : `None | list<PollResult>`
    """
    if new_results is None:
        return None
    
    if old_results is None:
        return new_results
    
    # Collect alive answer_id-s
    answer_ids = {result.answer_id for result in new_results}
    
    # Remove not alive answer_id-s
    for index in reversed(range(len(old_results))):
        old_result = old_results[index]
        if old_result.answer_id not in answer_ids:
            del old_results[index]
    
    # Merge old with new.
    for new_result in new_results:
        answer_id = new_result.answer_id
        for old_result in old_results:
            if answer_id == old_result.answer_id:
                old_result._merge_with(new_result)
                break
        else:
            old_results.append(new_result)

    return old_results


def poll_result_sort_key(result):
    """
    Sort key that can be used for poll results.
    
    Parameters
    ----------
    result : ``PollResult``
        Poll Result to get its sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return result.answer_id
