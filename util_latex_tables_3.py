import pandas as pd

def insert_multicol_at(df, row_content, row_index):
    """inserts a line into a dataframe at the row_index. row_content is a  string and gets wrapped into \multicol"""
    row_content = '\multicolumn{%d}{c}{%s}' % (df.shape[1], row_content)
    df.iloc[row_index, 0] = row_content + '\\\\ %'
    return df


def insert_rule_at(df, row_content, row_index):
    """inserts a line into a dataframe at the row_index. row_content is a  string"""
    df.iloc[row_index, 0] = row_content + ' %'
    return df

def insert_multirow_at(df, row_content, row_index, col_idx, num_rows):
    """inserts a line into a dataframe at the row_index. row_content is a  string and gets wrapped into \multicol"""
    row_content = '\\multirow{%d}{*}{%s}' % (num_rows, row_content)
    df.iloc[row_index, col_idx] = row_content
    return df

def insert_row_at(df, row_content, row_index):
    """replaces the row at row_index with row_content list"""
    # replace the row at row_index with row_content
    df.iloc[row_index] = row_content
    return df

def insert_list_at(df, row_content, row_index, col_idx):
    """replaces the row at row_index with row_content list"""
    # replace the row at row_index with row_content
    for j in range(0, len(row_content)):
        df.iloc[row_index, col_idx+j] = row_content[j]
    return df

def insert_at(df, content, row_index, col_idx):
    """replaces the row at row_index with row_content list"""
    # replace the row at row_index with row_content
    df.iloc[row_index, col_idx] = content
    return df




len_correlation_names = 1
len_mean_std_column = 1
len_reject_fail_column = 1
len_xy_yaw_rpe_ape_columns = 2
num_cols_temp = len_xy_yaw_rpe_ape_columns + len_reject_fail_column 

# make a dataframe with 3 columns and 4 rows with '' in each cell
len_rules = 5 - 1 # weil bottomrule schon da ist
len_header = 2
len_rows = 12 + len_header # #4 für rgbd stereo -1 für header
len_clines = 5

def df_latex_table_template_3(test_names, correlation_names=[]):
    num_rows = len_rows + len_rules + len_clines
    if len(correlation_names) == 0:
        num_cols = num_cols_temp + len(test_names)
    else:
        num_cols = num_cols_temp + len(test_names) + len(correlation_names) + len_mean_std_column
    # print('num_rows', num_rows)
    # print('num_cols', num_cols)
    df = pd.DataFrame([['' for i in range(0, num_cols)] for j in range(0, num_rows)])
    # df = pd.DataFrame() 
    #test_names = ["KS2", 'BF', "KW", 'BM', "MWU"]
    # correlation_names = ['f']
    line = ['', 'data type', ''] + test_names
    if len(correlation_names) != 0:
        line += [''] + correlation_names
    # insert a line at row 0
    df = insert_rule_at(df, '\midrule', len_header-1)
    df = insert_row_at(df, line, len_header) # line for the test names!?
    df = insert_rule_at(df, '\midrule', len_header+1)
    df = insert_rule_at(df, '\midrule', len_header+2)
    df = insert_multirow_at(df, 'RGBD and stereo ORB-SLAM', row_index=len_header+3, col_idx=0, num_rows=4)
    df = insert_multirow_at(df, '  translational  ', row_index=len_header+3, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, '  rotational  ', row_index=len_header+6, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, 'mono and stereo ORB-SLAM', row_index=len_header+9, col_idx=0, num_rows=4)
    df = insert_multirow_at(df, '  translational  ', row_index=len_header+9, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, '  rotational  ', row_index=len_header+12, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, 'mono and RGBD ORB-SLAM', row_index=len_header+15, col_idx=0, num_rows=4)
    df = insert_multirow_at(df, '  translational  ', row_index=len_header+15, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, '  rotational  ', row_index=len_header+18, col_idx=1, num_rows=2)
    # line = [1,2,3,4,5]
    # df = insert_list_at(df, line, row_index=6, col_idx=3)
    # line_f = 0.421
    # df = insert_at(df, line_f, row_index=6, col_idx=9)

    for i in range(0, 6):
        df = insert_at(df, 'reject', row_index=len_header+3+i*3, 
                       col_idx=len_xy_yaw_rpe_ape_columns)
        df = insert_at(df, 'fail', row_index=len_header+4+i*3, 
                       col_idx=len_xy_yaw_rpe_ape_columns)
        if len(correlation_names) != 0:
            df = insert_at(df, 'mean', row_index=len_header+3+i*3, 
                        col_idx=num_cols - len(correlation_names)-1)
            df = insert_at(df, 'std', row_index=len_header+4+i*3, 
                        col_idx=num_cols - len(correlation_names)-1)

    df = insert_rule_at(df, '\cline{2-%d}'%(num_cols), len_header+5)
    df = insert_rule_at(df, '\cline{1-%d}'%(num_cols), len_header+8)
    df = insert_rule_at(df, '\cline{2-%d}'%(num_cols), len_header+11)
    df = insert_rule_at(df, '\cline{1-%d}'%(num_cols), len_header+14)
    df = insert_rule_at(df, '\cline{2-%d}'%(num_cols), len_header+17)
    df = insert_rule_at(df, '\\bottomrule', len_header+20) # +2 hinter letzter rotational zeile

    return df

def latex_table_from_df_template_3(df, precision, test_names, correlation_names=[]):
    if len(correlation_names) == 0:
        col_format = 'll|l' + 'r' * len(test_names)
    else:
        col_format = 'll|l' + 'r' * len(test_names)+ '|l' + 'r' * len(correlation_names)
    df_latex = df.to_latex(index=False,header=False,index_names=False, column_format=col_format, float_format=f"%.{precision}f")
    #remove the \toprule and \midrule with replace ''
    df_latex = df_latex.replace('\\toprule\n\midrule\n', '')
    # get the number of cols of the df
    num_cols = df.shape[1]
    # create string of form "% &  &  &  &  &  &  &  &  &  \\" with width number of &"
    string_to_replace = ' %' + ' & ' * (num_cols-1) + ' \\\\'
    # replace '' with string_to_replace
    df_latex = df_latex.replace(string_to_replace, '')
    # # add caption add the end of the string
    # df_latex += "\caption{%s}\n" % caption
    # # add label add the end of the string
    # df_latex += "\label{%s}" % label
    return df_latex
