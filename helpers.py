def write_name(scs_file, **kwargs):
    scs_file.write(kwargs.get('system_name') + ' => nrel_main_idtf:' + '\n')
    scs_file.write('   [' + kwargs.get('name') + '](* <- lang_ru;; *);;' + '\n')


def write_zip_code(scs_file, **kwargs):
    scs_file.write(kwargs.get('system_name') + ' => nrel_zip_code:' + '\n')
    scs_file.write('   [' + kwargs.get('zip_code') + '](* <- lang_ru;; *);;' + '\n')


def write_address(scs_file, **kwargs):
    scs_file.write(kwargs.get('system_name') + ' => nrel_address:' + '\n')
    scs_file.write('   [' + kwargs.get('address') + '](* <- lang_ru;; *);;' + '\n')


def write_image(scs_file, **kwargs):
    scs_file.write(kwargs.get('system_name') + ' <- rrel_key_sc_element:' + '\n')
    scs_file.write('    ' + kwargs.get('system_name') + '_Image (*' + '\n')
    scs_file.write('    ' + '=> nrel_main_idtf:' + '\n')
    scs_file.write('    ' + ' [' + kwargs.get('name') + ' - Изображение](* <- lang_ru;; *);;' + '\n')
    scs_file.write('    ' + '<-sc_illustration;;' + '\n')
    scs_file.write('    ' + '<= nrel_sc_text_translation: ...' + '\n')
    scs_file.write(2 * '    ' + '(*' + '\n')
    scs_file.write(2 * '    ' + '->rrel_example:' + '"file://' + kwargs.get('image_name') + '"(* <-image;; *);;' + '\n')
    scs_file.write(2 * '    ' + '*);;' + '\n')
    scs_file.write('*);;' + '\n')


def write_geolocation(scs_file, **kwargs):
    scs_file.write('{0} => nrel_geographical_location: ...\n'.format(kwargs.get('system_name')))
    scs_file.write('    (*\n')
    scs_file.write('        <-concept_mapped_point;;\n')
    scs_file.write('        => nrel_WGS_84_translation: [{0}, {1}] (*\n'.format(kwargs.get('lat'), kwargs.get('lng')))
    scs_file.write('            -> ... (*\n')
    scs_file.write('                <- concept_coordinate;;\n')
    scs_file.write('                -> rrel_latitude: ... (* <= nrel_value: ... (* -> rrel_degree: [{0}] ;; *);; *);;\n'.format(kwargs.get('lat')))
    scs_file.write('                -> rrel_longitude: ... (* <= nrel_value: ... (* -> rrel_degree: [{0}] ;; *);; *);;\n'.format(kwargs.get('lng')))
    scs_file.write('                    *);;\n')
    scs_file.write('        *);;\n')
    scs_file.write('    *);;\n')
