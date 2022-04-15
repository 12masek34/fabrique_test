
QUERY_ADD_MESSAGE = '''insert into message (send_datetime, status, id_mailing, id_client)
                                 values ($1, $2, $3, $4) returning id_message'''

QUERY_UPDATE_MESSAGE = """update message set status='derived'
                          where id_message=$1"""