from unicodedata import name
import pandas

def read_data_from_csv():
    # read
    data = pandas.read_csv('C:/Users/Flask/OneDrive/Desktop/test/birthday_Data.csv')

    column = ['User_Id', 'Name', 'Birthday']

    # data pre-processing (fill N/A value with -1, using type)
    data = data[column]

    data = data.dropna()
    data['User_Id'] = data['User_Id'].astype(int)

    
    # print(data[column])

    return data[column]

if __name__ == '__main__':
    read_data_from_csv()