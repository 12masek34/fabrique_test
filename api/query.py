QUERY_ADD_CLIENT = '''insert into client (phone, code_phone, tag, time_zone)
                    values ($1, $2, $3, $4)'''

QUERY_SELECT_CLIENT = '''select id_client, phone, code_phone, tag,time_zone from client
                        where id_client=$1'''

QUERY_UPDATE_CLIENT = '''update client set
                        phone=$1, code_phone=$2, tag=$3, time_zone=$4
                        where id_client = $5 returning id_client, phone, code_phone, tag, time_zone'''

QUERY_DELETE_CLIENT = '''delete from client where id_client=$1 returning id_client'''

QUERY_ADD_MAILING = """insert into mailing (start_datetime, text, filter, end_datetime)
                        values ($1, $2, $3, $4) returning id_mailing"""

QUERY_GET_COMMON_STATISTIC = '''select ma.id_mailing, count(ms.*) as count_message, ms.status from mailing as ma
                                join message as ms on ma.id_mailing = ms.id_mailing
                                group by ms.status, ma.id_mailing
                                order by ma.id_mailing'''

QUERY_GET_EXACT_STATISTIC = '''select ms.id_mailing, ms.id_message, ms.id_client, ms.send_datetime,
                                ma.start_datetime as start_datetime_mailing,
                                ma.end_datetime as end_datetime_mailing, ms.status, ma.text, ma.filter,
                                c.phone, c.code_phone, c.tag, c.time_zone
                                from mailing as ma
                                join message as ms on ma.id_mailing = ms.id_mailing
                                join client as c on ms.id_client = c.id_client
                                where ma.id_mailing=$1'''

QUERY_SELECT_MAILING = '''select id_mailing, start_datetime, text, filter, end_datetime from mailing
                            where id_mailing = $1'''

QUERY_UPDATE_MAILING = '''update mailing set start_datetime=$1, text=$2,
                            filter=$3, end_datetime=$4
                            where id_mailing=$5'''

QUERY_DELETE_MAILING = '''delete from mailing where id_mailing=$1 returning id_mailing'''

QUERY_GET_MAILING_FROM_ID = '''select id_mailing, start_datetime, text, filter, end_datetime from mailing
                                where id_mailing=$1'''

QUERY_GET_MAILING_FROM_FILTER = """select id_client, phone, code_phone, tag, time_zone from client
                                   where  tag like $1 or code_phone like $1"""
