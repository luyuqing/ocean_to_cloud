def cal_reeling(steel_diameter,
                fabrication_method,
                vessel,
                any_inner_metal_layer,
                cladded_or_lined,
                clad_layer_thickness=3.0,
                resistance_strain_factor=2.0, #Low for installation, Table 7-5 of OS-F101
                material_factor=1.15,
                load_effect_factor=1.2, # Table 4-4 of OS-F101
                ext_coating_thickness=0):

    if fabrication_method == 'HFW':
        max_yt_ratio = 0.95
    elif fabrication_method == 'SMLS':
        max_yt_ratio = 0.89
    else:
        max_yt_ratio = 0.90


    if vessel == '7Oceans':
        reel_diameter = 18000 #Unit mm
    elif vessel == '7Navica':
        reel_diameter = 15000 #Unit mm
    else: 
        return('Erro, no installation vessel is found')

    #Calcuations for Min Required WT for Reeling

    if fabrication_method == 'SMLS':
        condition_effect_factor = 0.77
    elif fabrication_method == 'HFW':
        condition_effect_factor = (0.59+(max_yt_ratio-0.9)/0.3)
    else:
        condition_effect_factor = 0.82

    max_nominal_reeling_strain = (steel_diameter/2)/((reel_diameter+steel_diameter)/2 + ext_coating_thickness)

    design_comp_strain= max_nominal_reeling_strain*load_effect_factor*condition_effect_factor

    from scipy.optimize import fsolve

    x0 = steel_diameter/20

    def f_reeling(t): 
        if steel_diameter/t <= 20:
            girth_weld_factor = 1.0
        elif steel_diameter/t <= 45 and steel_diameter/t > 20:
            girth_weld_factor = 1 - (steel_diameter/t - 20)/100
        return(design_comp_strain- (0.78*(t/steel_diameter-0.01)*max_yt_ratio**(-1.5)*girth_weld_factor)/resistance_strain_factor)


    min_wt_reeling = round(float(fsolve(f_reeling,x0)),3)


    if min_wt_reeling < steel_diameter/45:
        return 'Girth Weld Factor is not defined due to the D/t is larger then 45'

    if any_inner_metal_layer == 'yes':
        if cladded_or_lined == 'Cladded':
            min_wt_reeling_no_clad  = min_wt_reeling - clad_layer_thickness
        else: 
            min_wt_reeling_no_clad = min_wt_reeling
    else:
        min_wt_reeling_no_clad = min_wt_reeling

    return(min_wt_reeling_no_clad)


print(cal_reeling(steel_diameter=273.1,
                  fabrication_method='HFW',
                  vessel='7Oceans',
                  any_inner_metal_layer='no',
                  cladded_or_lined='Cladded',
                  clad_layer_thickness=3.0,
                  resistance_strain_factor=2.0, #Low for installation, Table 7-5 of OS-F101
                  material_factor=1.15,
                  load_effect_factor=1.2, # Table 4-4 of OS-F101
                  ext_coating_thickness=0))
