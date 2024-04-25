from .process_birthday_df import append_yearday

def get_updated_df():

    # update yday
    df = append_yearday()

    # 後面可能還會有別的需要update的東西

    return df