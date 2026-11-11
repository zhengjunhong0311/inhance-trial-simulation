import pandas as pd
from src.dose_selection import select_doses
from src import config

def create_mock_res(trough_vals, auc_vals):
    df_t = pd.DataFrame({'LS_Mean_Diff': trough_vals}, index=config.DOSE_ORDER)
    df_a = pd.DataFrame({'LS_Mean_Diff': auc_vals}, index=config.DOSE_ORDER)
    return df_t, df_a

def test_rule_1_multiple_meet_both():
    # 规则 1：都达标
    t, a = create_mock_res([0.2, 0.2, 0.2, 0.2], [0.3, 0.3, 0.3, 0.3])
    low, high, rule, _ = select_doses(t, a, X=0.1, Y=0.2)
    assert rule == '1'
    assert low == 'Indacaterol75'
    assert high == 'Indacaterol150'

def test_rule_8_none_meet():
    # 规则 8：都不达标
    t, a = create_mock_res([0.05, 0.04, 0.03, 0.02], [0.1, 0.1, 0.1, 0.1])
    low, high, rule, _ = select_doses(t, a, X=0.1, Y=0.2)
    assert rule == '8'