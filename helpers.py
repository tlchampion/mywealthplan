def get_values():
    return q1.value, q2.value, q3.value, q4.value, q5.value, q6.value

def get_stocks():
    return pd.read_csv(Path("./stocks.csv"), index_col='Date', parse_dates=True, infer_datetime_format=True)
def get_weights():
    return [0.30,0.20,0.40,0.10]


if __name__ == "__main__":
    print ("This script is not meant to be accessed directly")