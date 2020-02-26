import eikon_import as ei


def create_data_files():
    ei.create_data_file('eurodollar_rics.csv', 'eurodollar_fields.csv', 'eurodollar_data.csv')
    ei.create_data_file('deposit_rics.csv', 'deposit_fields.csv', 'deposits_data.csv')
    ei.create_data_file('swap_rics.csv', 'swap_fields.csv', 'swaps_data.csv')
    ei.create_data_file('ois_rics.csv', 'ois_fields.csv', 'ois_data.csv')


if __name__ == '__main__':
    depos = ei.read_data('eurodollar_data.csv')
    ed = ei.read_data('deposits_data.csv')
    swaps = ei.read_data('swaps_data.csv')
    ois = ei.read_data('ois_data.csv')
