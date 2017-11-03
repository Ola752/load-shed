import pandas as pd
import os



def csv2hdf(df, fn):
    df.to_hdf(fn, 'data', mode='w', format='table')
    del df
    print('done')


def csv2hdf_(df, fn):
    store = pd.HDFStore(fn)
    store.append('data', df)
    store.close()
    print('done')


# def list2hdf(df, fn):
#     save = pd.HDFStore(fn)
#     save.append('data', df)
#     save.close()
#     print('done')


if __name__ == '__main__':
    filename = 'ls_comp'
    # filename = 'ls_debug'
    csv_file = f'{filename}.csv'
    hdf_file = f'{filename}.h5'
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, csv_file)
    uses = pd.read_csv(csv_file, names=['date', 'hour', 'house_id', 'value'])  # dataframe (in pandas)
    pd.to_datetime(uses['date'])
    uses.value = uses.value.astype(float)
    csv2hdf(uses, hdf_file)
    # list2hdf(hour_uses, hdf_file)

