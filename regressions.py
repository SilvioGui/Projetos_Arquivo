import numpy as np
import scipy
from scipy import stats

def get_x_axis(vecty):
    x = np.arange(len(vecty))
    return x

def lin_regress(vectx, vecty):
    slope, intercept, r_value, p_value, std_err = stats.linregress(vectx,vecty)
    rquad = r_value**2
    vectreg = [slope*i + intercept for i in vectx]
    return vectreg, rquad, slope, p_value

def exp_regress(vectx, vecty):
    ln = [np.log(i) for i in vecty]
    slope, intercept, r_value, p_value, std_err = stats.linregress(vectx,ln)
    rquad = r_value**2
    vectreg = [np.exp(slope*i + intercept) for i in vectx]
    return vectreg, rquad, slope, p_value

def log_regress(vectx, vecty):
    yexp = [np.exp(i) for i in vecty]
    slope, intercept, r_value, p_value, std_err = stats.linregress(vectx, yexp)
    rquad = r_value**2
    vectreg = [np.log(slope*i + intercept) for i in vectx]
    return vectreg, rquad, slope, p_value

def best_curve_fit(vecty, tests):
    vectx = get_x_axis(vecty)
    first_value = vecty[0]
    last_value = vecty[len(vecty)-1]
    if first_value != 0 and last_value != 0:
        perc_dif = abs(first_value/last_value-1)
    else:    
        perc_dif = 1
    if perc_dif < 0.03:
        return vectx, vectx, 0, 0, 0, "Irrelevant trend", 'irrelevant'
    else:
        rquad_lin, rquad_exp, rquad_log = 0, 0, 0
        vectreg_lin, rquad_lin, slope_lin, p_value_lin = lin_regress(vectx, vecty)
        vectreg_exp, rquad_exp, slope_exp, p_value_exp = exp_regress(vectx, vecty)
        vectreg_log, rquad_log, slope_log, p_value_log = log_regress(vectx, vecty)
        trend_result = "R.lin² = %s, R.exp² = %s, R.log² = %s\n" %(rquad_lin, rquad_exp, rquad_log)
        if tests == 'all':
            best_fit = max(rquad_lin, rquad_exp, rquad_log)
        elif tests == 'not linear':
            best_fit = max(rquad_exp, rquad_log)
        elif tests == 'not exp':
            best_fit = max(rquad_lin, rquad_log)
        elif tests == 'not log':
            best_fit = max(rquad_lin, rquad_exp)
        
        if best_fit == rquad_lin:        
            trend_result += "The best curve fit is linear"
            trend_type = 'linear'
            return vectx, vectreg_lin, rquad_lin, slope_lin, p_value_lin, trend_result, trend_type
        elif best_fit == rquad_exp:        
            trend_result += "The best curve fit is exponencial"
            trend_type = 'exponencial'
            return vectx, vectreg_exp, rquad_exp, slope_exp, p_value_exp, trend_result, trend_type
        elif best_fit == rquad_log:
            trend_result += "The best curve fit is logarithmic"
            trend_type = 'logarithmic'
            return vectx, vectreg_log, rquad_log, slope_log, p_value_log, trend_result, trend_type
    
