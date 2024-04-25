import datetime
import msg_wrapper
import pandas

def today(cache_bd):
    # 得到當前時間的datetime
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

    # 月、日
    month = t.month
    day = t.day

    today_date = str(month) + '/' + str(day)

    # 直接用日期下去搜比較快
    columns = ['ID', 'name']
    result = cache_bd[cache_bd['birthday'] == today_date][columns]
    
    return msg_wrapper.today(result, today_date) 

def sort_ng_rank(cache_ng):

    # sort 
    sorted_cache_ng = cache_ng.sort_values('Points', ascending=False, ignore_index=True)

    return sorted_cache_ng