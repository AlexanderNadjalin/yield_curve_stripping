import eikon_import as ei


if __name__ == '__main__':
    ed_rics, ed_fields = ei.read_config('eurodollar_rics.csv', 'eurodollar_fields.csv')
    ed = ei.get_data(ed_rics, ed_fields)
    print(ed)
