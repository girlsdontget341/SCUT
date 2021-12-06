import datetime

from grabqieman.Grab import MultiGrab,GrabQM
from grabdanjuan.Grab import GrabDJ,MultiGrabDJ
from dbcontroller.dbcontroller import dbcontrolle
from main_widget.main_widget import  main_widget



dbcontrolle().pid_is_in_list('000')
# nowtime = datetime.datetime.now()
# print(nowtime)
# dbcontrolle().get_user_record('A4-C3-F0-9F-2F-8A')
# url_list=[
#     "https://qieman.com/portfolios/ZH001798",
#     "https://qieman.com/portfolios/ZH012926",
#     "https://qieman.com/portfolios/ZH039471",
#     "https://qieman.com/portfolios/ZH010246",
#     "https://qieman.com/portfolios/ZH006498",
#     "https://qieman.com/portfolios/ZH000193",
#     "https://qieman.com/portfolios/ZH009664",
#     "https://qieman.com/portfolios/ZH030684",
#     "https://qieman.com/portfolios/ZH017252",
#     "https://qieman.com/portfolios/ZH007973",
#     "https://qieman.com/portfolios/ZH037807",
#     "https://qieman.com/portfolios/ZH007974",
#     "https://qieman.com/portfolios/ZH017409",
#     "https://qieman.com/portfolios/ZH035411",
#     "https://qieman.com/portfolios/ZH043108",
#     "https://qieman.com/portfolios/ZH043126"
# ]
# GrabQM(url_list).get_position()
# MultiGrabDJ().test()
# GrabDJ().update_base_message()


# a=MultiGrabDJ()
# a.start()