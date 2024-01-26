# @Version: python3.10
# @Time: 2024/1/24 22:43
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: pulp_configure.py
# @Software: PyCharm
# @User: chent


# from pulp import *
import PuLP

# 定义问题
prob = LpProblem("Maximize the sum of list2", LpMaximize)

# 定义变量
vars = LpVariable.dicts("Var", range(1, len(list1) + 1), 0, None, LpInteger)

# 建立目标函数
prob += lpSum(vars)

# 建立约束条件
for i in range(len(list1)):
    if list3[i] == 1:
        prob += vars[i] <= max_increase1 * list2[i] / list1[i]
    elif list3[i] == 0:
        prob += vars[i] <= list2[i] / list1[i]
    else:  # list3[i] == -1
        prob += vars[i] >= list2[i] / list1[i] * (1 - max_decrease)

    # 添加目标函数的约束条件
prob += lpSum([vars[i] * list1[i] for i in range(len(list1))]) <= x

# 求解问题
prob.solve()

# 输出结果
print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Objective=", value(prob.objective))

