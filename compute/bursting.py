

def cal_pressure_containment(steel_diameter,
                             corrosion_allowance,
                             fabrication_method,
                             pipe_material,
                             max_design_temperature,
                             supplimentary_d_fulfilled,
                             supplimentary_u_fulfilled,
                             design_pressure,
                             level,
                             max_contents_density,
                             sea_water_density,
                             water_depth_for_bursting,
                             contents_type,
                             operation_zone,
                             gravity=9.807,
                             sys_test_content_density=1025,
                             incidental_design_factor_ope=1.1,
                             incidental_sys_test_factor_sys_test=1.0,
                             material_factor=1.15,
                             safety_class_system_test='Low'):
    # Calcuated the other parameters

    if supplimentary_d_fulfilled =='yes':
        if fabrication_method == "SMLS":
            tol = 0.1 # 10%
        elif fabrication_method == "HFW": # for 15mm < WT < 20mm
            tol = 0.8 # mm
        elif fabrication_method == "MWP": # for 15mm < WT < 20mm
            tol = 0.8 # mm
    else:
        if fabrication_method == "SMLS":
            tol = 0.125 # 12.5% for 10mm < WT < 25mm
        elif fabrication_method == "HFW": # for  WT > 15mm
            tol = 1.0 # mm
        elif fabrication_method == "MWP": # for  WT > 15mm
            tol = 1.0 # mm

    if pipe_material == 'DNV450': # Table 7-5
        smys = 450 #unit MPa
        smts = 535
    elif pipe_material == 'DNV415':
        smys = 415 #unit MPa
        smts = 520
    elif pipe_material == 'DNV390':
        smys = 390 #unit MPa
        smts = 490
    elif pipe_material == 'DNV360':
        smys = 360 #unit MPa
        smts = 460
    elif pipe_material == 'DNV22Cr':   # Table 7-11
        smys = 450 #unit MPa
        smts = 620
    elif pipe_material == 'DNV25Cr':
        smys = 550 #unit MPa
        smts = 750
    else:
        return('Error, Material must be defined')

    if pipe_material == 'DNV450' or 'DNV415' or 'DNV390' or 'DNV360':
        derate_ys = 0
        derate_ts = 0
        if max_design_temperature >= 0 and max_design_temperature < 50:
            derate_ys = 0
            derate_ts = 0
        elif max_design_temperature >= 50 and max_design_temperature < 100:
            derate_ys = 0.6 * max_design_temperature - 30
            derate_ts = 0.6 * max_design_temperature - 30
        elif max_design_temperature >= 100 and max_design_temperature < 200:
            derate_ys = 0.4 * max_design_temperature - 10
            derate_ts = 0.4 * max_design_temperature - 10
        else:
            return("No Material Derating is defined")
    elif pipe_material == 'DNV22Cr' or 'DNV25Cr':
        derate_ys = 0
        derate_ts = 0
        if max_design_temperature >= 0 and max_design_temperature < 20:
            derate_ys = 0
            derate_ts = 0
        elif max_design_temperature >= 20 and max_design_temperature < 50:
            derate_ys = 4/3 * max_design_temperature - 80/3
            derate_ts = 4/3 * max_design_temperature - 80/3
        elif max_design_temperature >= 50 and max_design_temperature < 100:
            derate_ys =  max_design_temperature - 10
            derate_ts =  max_design_temperature - 10
        elif max_design_temperature >= 100 and max_design_temperature < 150:
            derate_ys = 0.6 * max_design_temperature + 30
            derate_ys = 0.6 * max_design_temperature + 30
        elif max_design_temperature >= 150 and max_design_temperature < 200:
            derate_ys = 0.4 * max_design_temperature + 60
            derate_ys = 0.4 * max_design_temperature + 60
        else:
            return("No Material Derating is defined")
    else:
        return("No Material Derating is defined")


    if supplimentary_u_fulfilled == 'yes':
        material_strength_factor = 1.0
    else:
        material_strength_factor = 0.96

    char_yiled_stress = (smys - derate_ys)* material_strength_factor

    char_tensile_stress = (smts - derate_ts)* material_strength_factor


    # Define Safety Class

    if contents_type == 'Flammable': # Table 2-1 of OS-F101
        if operation_zone == 'Zone2':
            safety_class_ope = 'High'
        elif operation_zone == 'Zone1':
            safety_class_ope = 'Medium'
        else:
            return('No Safety Class is defined')


    if contents_type == 'Non-flammable':
        if operation_zone == 'Zone2':
            safety_class_ope = 'Medium'
        elif operation_zone == 'Zone1':
            safety_class_ope = 'Low'
        else:
            return('No Safety Class for Operation is defined')


    if safety_class_ope == 'High':  #Table 5-3 of OS-F101
        safety_class_resistance_ope = 1.308

    if safety_class_ope == 'Medium':
        safety_class_resistance_ope = 1.138

    if safety_class_ope == 'Low':
        safety_class_resistance_ope = 1.046

    if safety_class_system_test == 'Low':
        safety_class_resistance_sys_test = 1.046
    else:
        return('Safety Class Resistance of System Test is not Normal')

    # Bursting Check


    # for Operation Case
    local_incidental_pressure= design_pressure/10 * incidental_design_factor_ope + max_contents_density*gravity*(level+water_depth_for_bursting)*1e-6
    hydrostatic_pressure = sea_water_density * gravity * water_depth_for_bursting * 1e-6
    local_design_pressure = local_incidental_pressure- hydrostatic_pressure
    pressure_containment_resistance_factor = min(char_yiled_stress, char_tensile_stress/1.15)
    wt_pressure_containment_with_tol_ope = (steel_diameter*3**(0.5)*local_design_pressure*material_factor*safety_class_resistance_ope/4.0)/(pressure_containment_resistance_factor+3**(0.5)*local_design_pressure*material_factor*safety_class_resistance_ope/4.0)
    # for System Test Case
    local_incidetal_pressure_sys_test = design_pressure/10 * incidental_design_factor_ope * 1.05  + sys_test_content_density*gravity*(level+water_depth_for_bursting)*1e-6
    local_design_pressure_sys_test = local_incidetal_pressure_sys_test - hydrostatic_pressure
    pressure_containment_resistance_factor_sys_test = min(smys, smts/1.15)
    wt_pressure_containment_with_tol_sys_test = (steel_diameter*3**(0.5)*local_design_pressure_sys_test*material_factor*safety_class_resistance_sys_test/4.0)/(pressure_containment_resistance_factor_sys_test+3**(0.5)*local_design_pressure_sys_test*material_factor*safety_class_resistance_sys_test/4.0)

    if fabrication_method == 'SMLS':
        min_wt_pressure_containment_ope = (wt_pressure_containment_with_tol_ope + corrosion_allowance)/(1.0-tol)
        min_wt_pressure_containment_sys_test = wt_pressure_containment_with_tol_sys_test/(1.0-tol)

    if fabrication_method == 'HFW':
        min_wt_pressure_containment_ope = wt_pressure_containment_with_tol_ope + tol + corrosion_allowance
        min_wt_pressure_containment_sys_test = wt_pressure_containment_with_tol_sys_test + tol

    if fabrication_method == 'MWP':
        min_wt_pressure_containment_ope = wt_pressure_containment_with_tol_ope + tol + corrosion_allowance
        min_wt_pressure_containment_sys_test = wt_pressure_containment_with_Tol_sys_test + Tol

    min_wt_pressure_containment = max(min_wt_pressure_containment_ope,min_wt_pressure_containment_sys_test)
    return(min_wt_pressure_containment)


# print(cal_pressure_containment(steel_diameter=273.1,
#                                corrosion_allowance=4.1,
#                                fabrication_method='HFW',
#                                pipe_material='DNV415',
#                                max_design_temperature=75,
#                                supplimentary_d_fulfilled='yes',
#                                supplimentary_u_fulfilled='no',
#                                design_pressure=200,
#                                level=30,
#                                max_contents_density=325,
#                                sea_water_density=0,
#                                water_depth_for_bursting=122,
#                                contents_type='Non-flammable',
#                                operation_zone='Zone1'))