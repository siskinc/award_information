# welfare_lottery_insert = \
#     "insert into welfarelottery_welfarelottery (name, trem, time, sale, pool, matchboll, bonus) " \
#     "values ('%s','%s','%s','%s','%s','%s','%s')"
# welfare_lottery_select_exit = \
#     "select count(*) from welfarelottery_welfarelottery where name = '%s' and trem = '%s'"
#
# high_frequency_lottery_insert = \
#     "insert into highfrequencylottery_highfrequencylottery (name, trem) values ('%s', '%s')"
#
# high_frequency_lottery_select_exit = \
#     "select count(*) from highfrequencylottery_highfrequencylottery where name = '%s' and trem = '%s'"
#
# meta_high_frequency_lottery_insert = \
#     "insert into highfrequencylottery_metahighfrequencylottery " \
#     "(trem, data_award, value3, value4, type_trem_id) " \
#     "values ('%s', '%s', '%s', '%s', %s)"
# meta_high_frequency_lottery_insert_value5 = \
#     "insert into highfrequencylottery_metahighfrequencylottery " \
#     "(trem, data_award, value3, value4, value5, type_trem_id) " \
#     "values ('%s', '%s', '%s', '%s', '%s', %s)"
#
# meta_high_frequency_lottery_select_exit = \
#     "select count(*) from highfrequencylottery_metahighfrequencylottery where " \
#     "trem = '%s' and type_trem_id = %s"
#
# high_frequency_lottery_select_id = \
#     "select id from highfrequencylottery_highfrequencylottery where " \
#     "name = '%s' and trem = '%s'"

welfare_lottery_insert = \
    "insert into WelfareLottery_welfarelottery (name, trem, time, sale, pool, matchboll, bonus) " \
    "values ('%s','%s','%s','%s','%s','%s','%s')"
welfare_lottery_select_exit = \
    "select count(*) from WelfareLottery_welfarelottery where name = '%s' and trem = '%s'"

high_frequency_lottery_insert = \
    "insert into HighFrequencyLottery_highfrequencylottery (name, trem) values ('%s', '%s')"

high_frequency_lottery_select_exit = \
    "select count(*) from HighFrequencyLottery_highfrequencylottery where name = '%s' and trem = '%s'"

meta_high_frequency_lottery_insert = \
    "insert into HighFrequencyLottery_metahighfrequencylottery " \
    "(trem, data_award, value3, value4, type_trem_id) " \
    "values ('%s', '%s', '%s', '%s', %s)"
meta_high_frequency_lottery_insert_value5 = \
    "insert into HighFrequencyLottery_metahighfrequencylottery " \
    "(trem, data_award, value3, value4, value5, type_trem_id) " \
    "values ('%s', '%s', '%s', '%s', '%s', %s)"

meta_high_frequency_lottery_select_exit = \
    "select count(*) from HighFrequencyLottery_metahighfrequencylottery where " \
    "trem = '%s' and type_trem_id = %s"

high_frequency_lottery_select_id = \
    "select id from HighFrequencyLottery_highfrequencylottery where " \
    "name = '%s' and trem = '%s'"