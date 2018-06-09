def cal_prop_buckling(steel_diameter,
                corrosion_allowance,
                fabrication_method,
                pipe_material,
                max_design_temperature,
                supplimentary_d_fulfilled,
                supplimentary_u_fulfilled,
                sea_water_density,
                water_depth_for_collapse_and_prop_buckling,
                contents_type,
                operation_zone,
                gravity=9.807,
                material_factor=1.15,
                min_interal_pressure=0,
                max_pipe_ovaliaty=0.03):

    if supplimentary_d_fulfilled =='yes':
        if fabrication_method == 'SMLS':
            tol = 0.1 # 10%
        elif fabrication_method == 'HFW': # for 15mm < WT < 20mm
            tol = 0.8 # mm
        elif fabrication_method == 'MWP': # for 15mm < WT < 20mm
            tol = 0.8 # mm
    else:
        if fabrication_method == 'SMLS':
            tol = 0.125 # 12.5% for 10mm < WT < 25mm
        elif fabrication_method == 'HFW': # for  WT > 15mm
            tol = 1.0 # mm
        elif fabrication_method == 'MWP': # for  WT > 15mm
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
        derate_ys= 0
        derate_ts = 0
        if max_design_temperature>= 0 and max_design_temperature< 50:
            derate_ys= 0
            derate_ts = 0
        elif max_design_temperature>= 50 and max_design_temperature< 100:
            derate_ys= 0.6 * max_design_temperature- 30
            derate_ts = 0.6 * max_design_temperature- 30
        elif max_design_temperature>= 100 and max_design_temperature< 200:
            derate_ys= 0.4 * max_design_temperature- 10
            derate_ts = 0.4 * max_design_temperature- 10
        else:
            return('No Material Derating is defined')
    elif pipe_material == 'DNV22Cr' or 'DNV25Cr':
        derate_ys= 0
        derate_ts = 0
        if max_design_temperature>= 0 and max_design_temperature< 20:
            derate_ys= 0
            derate_ts = 0
        elif max_design_temperature>= 20 and max_design_temperature< 50:
            derate_ys= 4/3 * max_design_temperature- 80/3
            derate_ts = 4/3 * max_design_temperature- 80/3
        elif max_design_temperature>= 50 and max_design_temperature< 100:
            derate_ys=  max_design_temperature- 10
            derate_ts =  max_design_temperature- 10
        elif max_design_temperature>= 100 and max_design_temperature< 150:
            derate_ys= 0.6 * max_design_temperature+ 30
            derate_ys= 0.6 * max_design_temperature+ 30
        elif max_design_temperature>= 150 and max_design_temperature< 200:
            derate_ys= 0.4 * max_design_temperature+ 60
            derate_ys= 0.4 * max_design_temperature+ 60
        else:
            return('No Material Derating is defined')
    else:
        return('No Material Derating is defined')


    if supplimentary_u_fulfilled == 'yes':
        material_strength_factor = 1.0
    else:
        material_strength_factor = 0.96

    char_yield_stress = (smys - derate_ys)* material_strength_factor

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

        
    if fabrication_method == 'SMLS': #Table 5-5 of OS-F101
        fabrication_factor = 1.0
    elif fabrication_method == 'HFW':
        fabrication_factor = 0.93
    elif fabrication_method == 'MWP':
        fabrication_factor = 0.93
    else:
        return('No factication method is defined')
        

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
        
    if safety_class_ope == 'Low':   #Table 5-3 of OS-F101, Safety Classes for Pressure Containment and others are different
        safety_class_resistance_factor_others = 1.04
    elif safety_class_ope == 'Medium':
        safety_class_resistance_factor_others = 1.14
    elif safety_class_ope == 'High':
        safety_class_resistance_factor_others = 1.26
    else:
        return('No Safety Class for Others is defined')
        
    maximum_external_pressure = sea_water_density * gravity * water_depth_for_collapse_and_prop_buckling * 1.0e-6

    ppr = (maximum_external_pressure - min_interal_pressure) * material_factor * safety_class_resistance_factor_others

    min_wt_propgation_buckling_wo_cor = (ppr/(35*char_yield_stress*fabrication_factor))**(1/2.5)*steel_diameter

    min_wt_propgation_buckling = round((min_wt_propgation_buckling_wo_cor + corrosion_allowance),3)

    return(min_wt_propgation_buckling)

# print(cal_prop_buckling(steel_diameter=273.1,
#                 corrosion_allowance=4.1,
#                 fabrication_method='HFW',
#                 pipe_material='DNV415',
#                 max_design_temperature=75,
#                 supplimentary_d_fulfilled='yes',
#                 supplimentary_u_fulfilled='no',
#                 sea_water_density=1025,
#                 water_depth_for_collapse_and_prop_buckling=70,
#                 contents_type='Flammable',
#                 operation_zone='Zone1',
#                 gravity=9.807,
#                 material_factor=1.15,
#                 min_interal_pressure=0,
#                 max_pipe_ovaliaty=0.03))

