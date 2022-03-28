from asyncore import read
import pandas as pd

def readExcel():
    """
    readExcel():
    #TODO Upper, lower dictionary keys.
    #TODO State registers.
    """
    df = pd.read_excel('data.xlsx', index_col = None)            
    dictionary = df.to_dict();                       
    print(dictionary['FECHA'][1])

def main():    
    readExcel()

if __name__ == '__main__':
    main()