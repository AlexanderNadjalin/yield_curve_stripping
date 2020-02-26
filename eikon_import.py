import eikon as ek
import configparser as cp
import pandas as pd
import os
from pathlib import Path
from loguru import logger


# Set global variables.
cfg = cp.ConfigParser()
cfg.read('eikon_cfg.cfg')
ek.set_app_key(cfg['eikon']['app_id'])


def get_data(rics: list, fields: list):
    """
    Eikon API call for data type file (not time series).
    Print any errors.
    :param rics: List of RIC:s to get.
    :param fields: List fields to get.
    :return: None.
    """
    data, err = ek.get_data(rics, fields)
    if err:
        logger.error(err)
    return data


def make_data(rics: list, fields: list, name: str) -> None:
    """
    Get data from Eikon API and save to .csv (not time series data).
    :param rics: List of RIC:s to get.
    :param fields: List fields to get.
    :param name: File name to save (including ".csv" suffix).
    :return: None.
    """
    df = get_data(rics, fields)
    df.index.name = 'ID'
    to_csv(df, name)


def to_csv(df: pd.DataFrame, name: str) -> None:
    """
    Save a Pandas DataFrame as a .csv file in the "eikon_data_files" directory.
    :param df: Data to save as a .csv file.
    :param name: File name (no suffix).
    :return: None.
    """
    abs_dir = os.path.dirname(__file__)
    rel_dir = os.path.join(abs_dir, 'eikon_data_files')
    path = ''.join([rel_dir, '/' + name])

    df.to_csv(path, encoding='utf-8')
    logger.info(' ')
    logger.info('File "' + name + '" saved in directory "eikon_data_files".')


def read_data(name: str) -> pd.DataFrame:
    """
    Read .csv file by name from directory "eikon_data_files".
    :param name: File name (including suffix).
    :return: Pandas DataFrame.
    """
    import_dir = Path.cwd().joinpath('eikon_data_files')

    path = Path.joinpath(import_dir, Path(name))
    if path.exists():
        return pd.read_csv(path, sep=',')
    else:
        logger.critical('File type "' + name + '.csv' + ' does not exist. Aborted.')
        quit()


def create_data_file(rics_conf: str, fields_conf: str, file_name: str) -> None:
    """
    Create .csv file with specified data from Eikon Python API and save in "/eikon_data_files".
    :param rics_conf: Name of config file (including ".csv" suffix) with Eikon RICs.
    :param fields_conf: Name of config file (including ".csv" suffix) with Eikon field names.
    :param file_name: Name of file to save with data.
    :return: None.
    """
    rics, fields = read_config(rics_conf, fields_conf)
    make_data(rics, fields, file_name)


def read_config(rics: str, fields):
    """
    Read config files from directory "eikon_config_files".
    :param rics: Name of .csv file with RICS to get.
    :param fields: Name of .csv file with fields to get.
    :return: List(s).
    """
    import_dir_rics = Path.cwd().joinpath('eikon_config_files')
    import_dir_fields = Path.cwd().joinpath('eikon_config_files')

    symb = []
    path_rics = Path.joinpath(import_dir_rics, Path(rics))

    if path_rics.exists():
        s = pd.read_csv(path_rics, sep=',')
        for column_name in s.columns:
            symb = s[column_name].tolist()
    else:
        logger.critical('File type "' + rics + '.csv' + '" does not exist. Aborted.')
        quit()

    flds = []
    path_fields = Path.joinpath(import_dir_fields, Path(fields))
    if path_fields.exists():
        f = pd.read_csv(path_fields, sep=',')
        for column_name in f.columns:
            flds = f[column_name].tolist()
    else:
        logger.critical('File type "' + fields + '.csv' + ' does not exist. Aborted.')
        quit()
    return symb, flds
