import pandas as pd
import os

#path ヘッダ、データタイプを指定
path_default = '/Users/yoshizawatatsuya/jupyter_workspace'
HEADER_STOCK = ['test1', 'test2', 'yyyymmdd', 'onhand', 'alocated', 'last_out_moving', 'last_in_moving']
DTYPE_STOCK = {'test1': str, 'test2': int, 'yyyymmdd': str, 'onhand': int, 'alocated': int, 'last_out_moving': str, 'last_in_moving': str}

class StockPreProcessing:
    def __init__(self, filename='test.csv', path= path_default, dataframefilename='df'):
        self.filename = filename
        self.path = path
        self.dataframefilename = dataframefilename

    def read_stock(self):
        filepath = os.path.join(self.path, self.filename)
        self.dataframefilename = pd.read_csv(filepath,
                                             encoding='utf-8', 
                                             sep=',',
                                             names=HEADER_STOCK,
                                             skiprows=1,
                                             header=None,
                                             index_col=None,
                                             low_memory=False,
                                             dtype=DTYPE_STOCK)

    def add_column_yyyymm_end(self):
        self.dataframefilename['yyyymm'] = self.dataframefilename['yyyymmdd'].str[:6] + 'E'
    
    def caliculate_free_onhand(self):
        self.dataframefilename['free_onhand'] = self.dataframefilename['onhand'] - self.dataframefilename['alocated']
        
    def fillna_last_moving(self):
        '''nonmovingを計算するために欠損値を穴埋め
        '''
        # 計算のためlast_in, last_out空欄を1900/1/1で穴埋め
        self.dataframefilename['last_out_moving'] = self.dataframefilename['last_out_moving'].fillna('19000101')
        self.dataframefilename['last_in_moving'] = self.dataframefilename['last_in_moving'].fillna('19000101')

        # datetetime計算に不都合な値を置換
        self.dataframefilename['last_out_moving'] = self.dataframefilename['last_out_moving'].replace('99991231', '19000101')
        self.dataframefilename['last_in_moving'] = self.dataframefilename['last_in_moving'].replace('19000101', '19000101')

    def to_datetime_last_moving(self):
        # last_in, last_out, yyyymmddをdatetime型に変換
        self.dataframefilename['last_out_moving'] = pd.to_datetime(self.dataframefilename['last_out_moving'], format='%Y%m%d')
        self.dataframefilename['last_in_moving'] = pd.to_datetime(self.dataframefilename['last_in_moving'], format='%Y%m%d')
        self.dataframefilename['yyyymmdd'] = pd.to_datetime(self.dataframefilename['yyyymmdd'], format='%Y%m%d')

    def caliculate_non_moving(self):
        '''non-mivingの計算
        '''
        pass

def main():
    print('test_module_import.pyがimportされました')

if __name__ == "__main__":
    main()