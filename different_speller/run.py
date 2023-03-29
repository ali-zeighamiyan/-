# import determine_probility

import traceback
import pathlib
import sys
import json


path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)
from src.predictor import get_name
# from src.normalizer.university import UniversityNormalizer
from src.config.logger import result_logger
# from src.config.logger import predictor_error

from src.broker.rabbitmq.main import RabbitMQ
from src.config.logger import logger
from src.config.envs import RMQ_CONFIG


# universityNormalizer = UniversityNormalizer()

rmq = RabbitMQ(config=RMQ_CONFIG, logger=logger)

# contoroller_dic = {'id': 10001, "persian_first_name": 'محمد' , "persian_last_name":'رضایی', "persian_full_name":'محمد رضایی', "persian_uni_name":'دانشگاه اردکان'}


def pretify(d):
    return json.dumps(d, sort_keys=False, indent=8, ensure_ascii=False)


def get_data_from_app(contoroller_dic, pid):

    person_id = contoroller_dic["id"]
    persian_firstname = contoroller_dic["persian_first_name"]
    persian_lastname = contoroller_dic["persian_last_name"]
    persian_fullname = contoroller_dic["persian_full_name"]
    persian_uniname = contoroller_dic["persian_uni_name"]
    different_firstnames = []
    different_lastnames = []
    different_fullnames = []

    # temprary
    # normal_uni_list = universityNormalizer.normalize_university_names(persian_uniname)
    normal_uni_list = [
        {"persian_uni_name": persian_uniname[0], "normal_uni_name": persian_uniname[0]}
    ]

    try:
        if person_id:
            status = True
            if persian_firstname and persian_lastname:
                (
                    different_firstnames,
                    different_lastnames,
                    different_fullnames,
                ) = get_name(
                    persian_fname=persian_firstname, persian_lname=persian_lastname
                )

            elif persian_fullname and len(persian_fullname.split()) >= 2:
                persian_firstname = persian_fullname.split()[0]
                persian_lastname = persian_fullname.split()[1:]
                (
                    different_firstnames,
                    different_lastnames,
                    different_fullnames,
                ) = get_name(
                    persian_fname=persian_firstname, persian_lname=persian_lastname
                )
        status = bool(different_fullnames) and status 
        result_dic_for_logger = {
        "status": status,
        "id": person_id,
        "persian_firstname": persian_firstname,
        "persian_lastname": persian_lastname,
        "persian_fullname": persian_fullname,
        "normal_uni_list": normal_uni_list,
        "different_firstnames": len(different_firstnames),
        "different_lastnames": len(different_lastnames),
        "different_fullnames": len(different_fullnames),
    }
    except:
        traceback.format_exc()
        error_explanation = traceback.format_exc()
        logger.debug(error_explanation)
        logger.debug("")
        status = False
        different_firstnames, different_lastnames, different_fullnames = (
            None,
            None,
            None,
        )
        status = bool(different_fullnames) and status 
        result_dic_for_logger = {
        "status": status,
        "id": person_id,
        "persian_firstname": persian_firstname,
        "persian_lastname": persian_lastname,
        "persian_fullname": persian_fullname,
        "normal_uni_list": normal_uni_list,
        }

    

    result_dic = {
        "status": status,
        "id": person_id,
        "normal_uni_list": normal_uni_list,
        "different_firstnames": different_firstnames,
        "different_lastnames": different_lastnames,
        "different_fullnames": different_fullnames,
    }

    result_logger.debug(pretify(result_dic_for_logger))

    res = rmq.send(
        pid=pid,
        data={"pid": pid, "msg": result_dic},
        routing_key="nef.dbc",
        content_type="bperson",
        wait_for_response=False,
    )

    return  status, result_dic


# contoroller_dic = {'id':1, "persian_first_name":'سیذ علی رضا', "persian_last_name":'مرتضوی', 'persian_full_name':'سیذ علی رضا مرتضوی','persian_uni_name':['دانشگاه اردکان']}
# get_data_from_app(contoroller_dic,1)
