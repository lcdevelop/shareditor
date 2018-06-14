#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb

cur = None
conn = None


def construct_connection():
    global conn, cur
    conn = MySQLdb.connect(host='rm-2zesy2n7p6j20x2udo.mysql.rds.aliyuncs.com',
                           user='lichuang',
                           passwd='fucking@2Bh8j1@m@uG',
                           db='db_shareditor',
                           port=3306)
    cur = conn.cursor()


def get_ip_chats():
    ip_chats = {}
    sql = """
    SELECT client_ip, replace(message, '"', ''), talker FROM web_chat
    """
    cur.execute(sql)
    for row in cur.fetchall():
        client_ip = row[0]
        message = row[1]
        talker = row[2]
        if client_ip in ip_chats:
            ip_chats[client_ip].append({'message': message, 'talker': talker})
        else:
            ip_chats[client_ip] = [{'message': message, 'talker': talker}]
    return ip_chats


def get_corpus(ip_chats):
    for chats in ip_chats.values():
        last_chat = None
        for chat in chats:
            if last_chat and last_chat['talker'] == 0 and chat['talker'] == 1:
                save_corpus(last_chat['message'], chat['message'])
            last_chat = chat


def get_question_id(question):
    sql = """
        SELECT id FROM web_corpusquestion WHERE text="%s"
        """ % question
    cur.execute(sql)
    one = cur.fetchone()
    if one:
        return one[0]
    else:
        return None


def get_answer_id(answer, question_id):
    sql = """
        SELECT id FROM web_corpusanswer WHERE text="%s" AND question_id=%d
        """ % (answer, question_id)
    cur.execute(sql)
    one = cur.fetchone()
    if one:
        return one[0]
    else:
        return None


def get_question_id_or_insert(question):
    question_id = get_question_id(question)
    if question_id:
        return question_id
    else:
        sql = """
        INSERT INTO web_corpusquestion(text, bad, is_del) VALUES("%s", 0, 0)
        """ % question
        cur.execute(sql)
        conn.commit()
    return get_question_id(question)


def insert_answer(answer, question_id):
    answer_id = get_answer_id(answer, question_id)
    if answer_id:
        return answer_id
    else:
        sql = """
        INSERT INTO web_corpusanswer(text, `like`, is_del, question_id) VALUES("%s", 0, 0, %d)
        """ % (answer, question_id)
        cur.execute(sql)
        conn.commit()


def save_corpus(question, answer):
    question_id = get_question_id_or_insert(question)
    if question_id:
        insert_answer(answer, question_id)


def main():
    construct_connection()
    ip_chats = get_ip_chats()
    get_corpus(ip_chats)


if __name__ == '__main__':
    main()

    #
    # for ip, chats in ip_chats.items():
    #     last_chat = None
    #     for index, chat in enumerate(chats):
    #         if last_chat and last_chat.talker == 0 and chat.talker == 1:
    #             if last_chat.message + '|' + chat.message not in corpus_set:
    #                 print ip, last_chat.message, chat.message
    #                 Corpus.objects.update_or_create(defaults={}, question=last_chat.message, answer=chat.message)
    #             pass
    #         last_chat = chat