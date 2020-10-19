import pandas
import datetime


class Transform:
    @classmethod
    def to_alphavantage(cls, data: pandas.DataFrame)\
        -> pandas.DataFrame:
        data = data.iloc[:, [0,1,2,3,4]]
        data.iloc[:, 4] = data.iloc[:, 4] * 1000
        return data
