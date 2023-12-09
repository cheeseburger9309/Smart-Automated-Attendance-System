import datetime
import os
import pickle
import smtplib
import sqlite3
import threading
from os.path import dirname, join
import cv2
import face_recognition
import numpy as np
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)


gmail_user = os.environ.get("EMAIL")
gmail_app_password = os.environ.get("PASSWORD")
send_from = os.environ.get("EMAIL")


def send_mailer(sender, body, subject="Attendance Alert"):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(gmail_user, gmail_app_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(send_from, sender, message)
        print('Email sent!')
    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP authentication failed! Please check your credentials.")
    except smtplib.SMTPException as e:
        print(f"Error: Failed to send email. {e}")


@app.post('/sendmaillees')
def sendmail():
    conn = get_db_connection()
    result = conn.execute(
        'SELECT DISTINCT s.student_id, a.date FROM students s LEFT JOIN attendance a ON s.student_id = a.student_id').fetchall()

    unique_ids = set()
    unique_dates = set()

    for row in result:
        student_id = row['student_id']
        date = row['date']

        unique_ids.add(student_id)

        if date is not None:
            unique_dates.add(date)

    total_days = len(unique_dates)

    for student_id in unique_ids:
        result = conn.execute(
            'SELECT COUNT(*) AS count FROM attendance WHERE student_id = ?', (student_id,)
        ).fetchone()

        count = result['count']

        if count / total_days < 0.85:
            student = conn.execute(
                'SELECT * FROM students WHERE student_id = ?', (student_id,)
            ).fetchone()

            if student is not None:
                email = student['email']
                send_mailer(email, "Your attendance is less than 85%")

    conn.close()

    return {
        "message": "Mail sent successfully"
    }, 200


@app.post('/sendmailall')
def sendmail1():
    conn = get_db_connection()

    result = conn.execute(
        'SELECT DISTINCT s.student_id, a.date FROM students s LEFT JOIN attendance a ON s.student_id = a.student_id').fetchall()

    unique_ids = set()
    unique_dates = set()

    for row in result:
        student_id = row['student_id']
        date = row['date']

        unique_ids.add(student_id)

        if date is not None:
            unique_dates.add(date)

    total_days = len(unique_dates)

    for student_id in unique_ids:
        result = conn.execute(
            'SELECT COUNT(*) AS count FROM attendance WHERE student_id = ?', (student_id,)
        ).fetchone()

        count = result['count']

        student = conn.execute(
            'SELECT * FROM students WHERE student_id = ?', (student_id,)
        ).fetchone()

        if student is not None:
            email = student['email']
            send_mailer(
                email, f"Your attendance is {count * 100 / total_days:.2f}%")

    conn.close()

    return {
        "message": "Mail sent successfully"
    }, 200


@app.route('/getdata', methods=['GET'])
def getdata():
    conn = get_db_connection()
    result = conn.execute(
        'SELECT s.student_id, a.date FROM students s LEFT JOIN attendance a ON s.student_id = a.student_id').fetchall()

    unique_ids = set()
    unique_dates = set()

    data = {}

    for row in result:
        student_id = row['student_id']
        date = row['date']

        unique_ids.add(student_id)
        if date is not None:
            unique_dates.add(date)

        if student_id not in data:
            data[student_id] = set()
        if date is not None:
            data[student_id].add(date)

    conn.commit()
    conn.close()

    exportdata = [
        {
            "id": student_id,
            "dates": [1 if date in data[student_id] else 0 for date in unique_dates]
        }
        for student_id in unique_ids
    ]

    return {
        "data": exportdata,
        "ids": list(unique_ids),
        "unique_dates": list(unique_dates)
    }, 200
