import eikon_import as ei


if __name__ == '__main__':
    ed_rics, ed_fields = ei.read_config('eurodollar_rics.csv', 'eurodollar_fields.csv')
    ed = ei.get_data(ed_rics, ed_fields)
    ei.create_data_file('eurodollar_rics.csv', 'eurodollar_fields.csv', 'eurodollar_data.csv')

    depo_rics, depo_fields = ei.read_config('deposits_rics.csv', 'deposits_fields.csv')
    depos = ei.get_data(depo_rics, depo_fields)
    ei.create_data_file('deposits_rics.csv', 'deposits_fields.csv', 'deposits_data.csv')
    print(depos)
