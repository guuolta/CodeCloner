''' クローン率を計算
'''
def calculate_clone_rate(count, clone_count):
    return clone_count / (1 if count == 0 else count)