import numpy as np
import pandas as pd

a = pd.DataFrame(
    np.array([[0, 0, 7, 4, 0, 9, 0, 3, 1],
              [0, 1, 0, 0, 3, 7, 0, 8, 0],
              [0, 0, 0, 6, 0, 0, 4, 0, 2],

              [4, 2, 0, 0, 0, 5, 0, 0, 9],
              [0, 7, 0, 0, 0, 0, 0, 0, 0],
              [3, 0, 0, 0, 0, 4, 0, 1, 0],

              [0, 0, 3, 5, 9, 8, 0, 0, 0],
              [0, 0, 6, 0, 0, 0, 0, 4, 8],
              [8, 0, 0, 0, 0, 0, 7, 0, 0]]
             )
)


class Sudu:
    def __init__(self, x):
        self.df = x
        self.new_df = self.df.copy()
        self.index = [(i, j) for i in range(9) for j in range(9)]
        self.index_list = []

    # 返回0数值的位置
    def return_zero(self):
        for k in self.index:
            if self.df.iloc[k] == 0:
                self.index_list.append(k)
        return self.index_list

    # 返回行列区域可取值，并进行更新
    def insert(self):
        for zero in self.index_list:
            # 如果要具体分析某个点信息，这里改pass为continue
            if not (zero == (6, 5)):
                pass
            # 横轴可取的数据范围
            a = [k for k in range(1, 10) if not (k in self.df.iloc[zero[0], :].values)]
            # 列轴可取的数据范围
            b = [k for k in range(1, 10) if not (k in self.df.iloc[:, zero[1]].values)]
            # 区域内可取的数据范围
            x, y = int(zero[0] / 3), int(zero[1] / 3)
            x_start, x_end = x * 3, x * 3 + 2
            y_start, y_end = y * 3, y * 3 + 2
            tt = [(i, j) for i in range(x_start, x_end + 1) for j in range(y_start, y_end + 1)]
            local_values = [self.df.iloc[v] for v in tt]
            c = [k for k in range(1, 10) if not (k in local_values)]
            # 取三种组合交集
            res = [v for v in a if v in b if v in c]
            # 如果只能取唯一值就进行更新
            if len(res) == 1:
                self.df.iloc[zero] = res[0]


su = Sudu(a)
su.return_zero()
su.insert()
if len(su.index_list) == 0:
    print(su.df)
else:
    for i in range(10):
        su = Sudu(su.df)
        su.return_zero()
        su.insert()
        if len(su.index_list) == 0:
            print(su.df)
            break
