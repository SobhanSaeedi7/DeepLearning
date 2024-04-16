import os
import shutil
import xml.etree.ElementTree as ET

def DTRB_dataset_maker(path, zipped_data_path='/content/drive/MyDrive/PyLearn 7 Course/57.OCR/plate_img-'):
  datasets = ['train', 'test', 'validation']
  Fa_letters = ['الف', 'ب', 'پ', 'ت', 'ث',
                'ز', 'ش', 'ع', 'ف', 'ک',
                'گ', 'D', 'S', 'ج', 'د',
                'س', 'ص', 'ط', 'ق', 'ل',
                'م', 'ن', 'و', 'ه‍', 'ی',
                '۰', '۱', '۲', '۳', '۴',
                '۵', '۶', '۷', '۸', '۹', 
                'ویلچر', 'ژ (معلولین و جانبازان)']

  En_letters =  ['A', 'B', 'P', 'T', 'Y',
                 'Z', 'X', 'E', 'F', 'K',
                 'G', 'D', 'S', 'J', 'W',
                 'C', 'U', 'R', 'Q', 'L',
                 'M', 'N', 'V', 'H', 'I',
                 '0', '1', '2', '3', '4',
                 '5', '6', '7', '8', '9', 
                 '@', '#']

  for dataset in datasets:
    shutil.unpack_archive(zipped_data_path + dataset + '.zip',
                          path)

    plates = []
    for filename in os.listdir(path+'/'+dataset):
      if filename.split('.')[1] == 'xml':
        tree = ET.parse(path+'/'+dataset+'/'+filename)
        root = tree.getroot()
        plate = ''
        for obj in root.findall('.//object'):
          name = obj.find('name').text
          if name in Fa_letters:
            name = En_letters[Fa_letters.index(name)]
          plate += name
        plate_list = [dataset+'/'+filename.split('.')[0]+'.jpg', plate]
        plates.append(plate_list)
        os.remove(path+'/'+dataset+'/'+filename)

    with open(path+'/gt_'+dataset+'.txt', 'w') as file:
      for plate in plates:
          file.write(f'{plate[0]}\t{plate[1]}\n')