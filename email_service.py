import os
import smtplib
import ssl
import mimetypes
import threading
import logging
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional

logger = logging.getLogger("email_service")

# -------------------------------------------------------------
# SMTP Configuration from Environment Variables
# -------------------------------------------------------------
def get_smtp_config():
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", os.getenv("SMTP_USERNAME", ""))
    password = os.getenv("SMTP_PASSWORD", os.getenv("SMTP_PASS", ""))
    sender = os.getenv("SMTP_FROM", os.getenv("SMTP_SENDER", user or "BioEdu Ta'lim Platformasi <no-reply@bioedu.uz>"))
    use_ssl = os.getenv("SMTP_USE_SSL", "").lower() in ("true", "1", "yes") or port == 465
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes") and not use_ssl

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "sender": sender,
        "use_ssl": use_ssl,
        "use_tls": use_tls
    }

def _send_mail_worker(
    to_emails: List[str],
    subject: str,
    html_content: str,
    text_content: str,
    attachment_path: Optional[str] = None,
    attachment_name: Optional[str] = None
):
    """
    Internal synchronous worker that sends the email.
    Wrapped in try/except so email failures never crash or bubble up.
    """
    if not to_emails:
        return

    config = get_smtp_config()
    if not config["host"]:
        logger.warning("SMTP_HOST is not configured; email notification skipped.")
        return

    # If no credentials provided, log notice and skip attempting to connect to external auth
    if not config["user"] or not config["password"]:
        logger.info(f"[Email Service] SMTP credentials not provided (SMTP_USER/SMTP_PASSWORD). Email notification for {to_emails} logged: '{subject}'")
        return

    for recipient in to_emails:
        if not recipient or "@" not in recipient or "." not in recipient:
            continue

        try:
            msg = MIMEMultipart("mixed")
            msg["Subject"] = subject
            msg["From"] = config["sender"]
            msg["To"] = recipient

            # Alternative part for text/plain and text/html
            alt_part = MIMEMultipart("alternative")
            alt_part.attach(MIMEText(text_content, "plain", "utf-8"))
            alt_part.attach(MIMEText(html_content, "html", "utf-8"))
            msg.attach(alt_part)

            # File attachment handling
            if attachment_path and os.path.isfile(attachment_path):
                file_size = os.path.getsize(attachment_path)
                # Keep attachment under 25MB for typical SMTP limits
                if file_size < 25 * 1024 * 1024:
                    ctype, encoding = mimetypes.guess_type(attachment_path)
                    if ctype is None or encoding is not None:
                        ctype = "application/octet-stream"
                    maintype, subtype = ctype.split("/", 1)

                    with open(attachment_path, "rb") as f:
                        part = MIMEBase(maintype, subtype)
                        part.set_payload(f.read())
                    encoders.encode_base64(part)

                    fname = attachment_name or os.path.basename(attachment_path)
                    part.add_header("Content-Disposition", f"attachment; filename=\"{fname}\"")
                    msg.attach(part)
                else:
                    logger.warning(f"Attachment {attachment_path} exceeds 25MB limit; skipped.")

            # Connect and send
            if config["use_ssl"]:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(config["host"], config["port"], context=context, timeout=15) as server:
                    if config["user"] and config["password"]:
                        server.login(config["user"], config["password"])
                    server.sendmail(config["sender"], [recipient], msg.as_string())
            else:
                with smtplib.SMTP(config["host"], config["port"], timeout=15) as server:
                    if config["use_tls"]:
                        context = ssl.create_default_context()
                        server.starttls(context=context)
                    if config["user"] and config["password"]:
                        server.login(config["user"], config["password"])
                    server.sendmail(config["sender"], [recipient], msg.as_string())

            logger.info(f"Email successfully sent to {recipient}: '{subject}'")

        except Exception as e:
            logger.warning(f"Failed to send email to {recipient}: {e}")

def send_email_async(
    to_emails: List[str],
    subject: str,
    html_content: str,
    text_content: str,
    attachment_path: Optional[str] = None,
    attachment_name: Optional[str] = None
):
    """
    Non-blocking async email trigger using a background daemon thread.
    """
    if not to_emails:
        return

    thread = threading.Thread(
        target=_send_mail_worker,
        args=(to_emails, subject, html_content, text_content, attachment_path, attachment_name),
        daemon=True
    )
    thread.start()

# -------------------------------------------------------------
# Clean HTML & Text Email Templates
# -------------------------------------------------------------
def build_homework_assigned_email(
    teacher_name: str,
    subject: str,
    hw_title: str,
    description: str,
    deadline: str,
    attachment_name: Optional[str] = None
) -> tuple:
    """Returns (subject, html_body, text_body)"""
    email_subject = f"Yangi uyga vazifa: {hw_title} ({subject})"

    has_attachment_html = ""
    if attachment_name:
        has_attachment_html = f"""
        <div style="margin-top: 16px; padding: 12px 16px; background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px;">
            <p style="margin: 0; font-size: 13px; color: #166534; font-weight: 600;">
                📎 Biriktirilgan fayl: <span>{attachment_name}</span> (ushbu xatga ilova qilingan)
            </p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>{email_subject}</title>
    </head>
    <body style="margin: 0; padding: 24px; background-color: #f8fafc; font-family: 'Helvetica Neue', Arial, sans-serif; color: #334155;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
        <!-- Header -->
        <tr>
          <td style="background: linear-gradient(135deg, #059669 0%, #0d9488 100%); padding: 32px 30px; text-align: left;">
            <span style="background-color: rgba(255,255,255,0.2); color: #ffffff; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px;">BioEdu Ta'lim</span>
            <h1 style="color: #ffffff; margin: 12px 0 4px 0; font-size: 22px; font-weight: 800;">Yangi Uyga Vazifa E'lon Qilindi</h1>
            <p style="color: #d1fae5; margin: 0; font-size: 13px;">Ustozingiz tomonidan yangi topshiriq biriktirildi</p>
          </td>
        </tr>

        <!-- Content -->
        <tr>
          <td style="padding: 30px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px;">
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">O'qituvchi:</td>
                <td style="padding-bottom: 12px; font-size: 14px; font-weight: 700; color: #0f172a; text-align: right;">{teacher_name}</td>
              </tr>
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">Fan:</td>
                <td style="padding-bottom: 12px; font-size: 14px; font-weight: 700; color: #059669; text-align: right;">{subject}</td>
              </tr>
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">Vazifa mavzusi:</td>
                <td style="padding-bottom: 12px; font-size: 14px; font-weight: 700; color: #0f172a; text-align: right;">{hw_title}</td>
              </tr>
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">Topshirish muddati:</td>
                <td style="padding-bottom: 12px; font-size: 14px; font-weight: 700; color: #d97706; text-align: right;">{deadline or "Belgilanmagan"}</td>
              </tr>
            </table>

            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; margin-top: 10px;">
              <p style="margin: 0 0 8px 0; font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.5px;">Topshiriq tavsifi va ko'rsatmalar:</p>
              <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #1e293b; white-space: pre-line;">{description or "Tafsilotlar platformada ko'rsatilgan."}</p>
            </div>

            {has_attachment_html}

            <div style="margin-top: 28px; text-align: center;">
              <p style="font-size: 13px; color: #64748b; margin-bottom: 16px;">Vazifani bajarib, platformada o'z kabinetingiz orqali topshiring:</p>
              <a href="/student/homework.html" style="display: inline-block; background-color: #059669; color: #ffffff; text-decoration: none; padding: 13px 32px; border-radius: 12px; font-weight: 700; font-size: 14px;">Vazifani Ko'rish va Topshirish</a>
            </div>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background-color: #f1f5f9; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0; font-size: 12px; color: #94a3b8;">
            Ushbu xabar BioEdu ta'lim platformasi orqali avtomatik yuborildi.
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    desc_fallback = description if description else "Tafsilotlar platformada ko'rsatilgan."
    att_text = f"Biriktirilgan fayl: {attachment_name} (ushbu xatga ilova qilingan)" if attachment_name else ""

    text = f"""
BioEdu Ta'lim Platformasi — Yangi Uyga Vazifa
=============================================

Hurmatli o'quvchi!
Ustozingiz {teacher_name} sizga yangi uyga vazifa yukladi.

O'qituvchi: {teacher_name}
Fan: {subject}
Mavzu: {hw_title}
Topshirish muddati: {deadline or 'Belgilanmagan'}

Topshiriq tavsifi:
{desc_fallback}

{att_text}

Platformaga kirib topshiriqni bajaring: /student/homework.html
    """.strip()

    return email_subject, html, text

# -------------------------------------------------------------
# High-Level Notification Dispatchers
# -------------------------------------------------------------
def notify_students_new_homework(
    students: list,
    teacher_name: str,
    subject: str,
    hw_title: str,
    description: str,
    deadline: str,
    file_url: Optional[str] = None,
    file_name: Optional[str] = None,
    upload_dir: Optional[Path] = None
):
    """
    Finds all valid student emails and sends async notification with attachment.
    """
    to_emails = [s.email.strip() for s in students if getattr(s, "email", None) and "@" in s.email]
    if not to_emails:
        return

    # Resolve local file path if fileUrl is given
    attachment_path = None
    if file_url and upload_dir:
        filename = file_url.replace("/uploads/", "")
        candidate = upload_dir / filename
        if candidate.is_file():
            attachment_path = str(candidate)

    subj, html, text = build_homework_assigned_email(
        teacher_name=teacher_name,
        subject=subject,
        hw_title=hw_title,
        description=description,
        deadline=deadline,
        attachment_name=file_name
    )

    send_email_async(
        to_emails=to_emails,
        subject=subj,
        html_content=html,
        text_content=text,
        attachment_path=attachment_path,
        attachment_name=file_name
    )

def notify_student_homework_graded(
    student,
    teacher_name: str,
    subject: str,
    hw_title: str,
    grade: str,
    feedback: str,
    file_url: Optional[str] = None,
    file_name: Optional[str] = None,
    upload_dir: Optional[Path] = None
):
    """
    Sends async grading review notification to the specific student.
    """
    if not student or not getattr(student, "email", None) or "@" not in student.email:
        return

    to_emails = [student.email.strip()]

    attachment_path = None
    if file_url and upload_dir:
        filename = file_url.replace("/uploads/", "")
        candidate = upload_dir / filename
        if candidate.is_file():
            attachment_path = str(candidate)

    subj, html, text = build_homework_graded_email(
        teacher_name=teacher_name,
        subject=subject,
        hw_title=hw_title,
        grade=grade,
        feedback=feedback,
        attachment_name=file_name
    )

    send_email_async(
        to_emails=to_emails,
        subject=subj,
        html_content=html,
        text_content=text,
        attachment_path=attachment_path,
        attachment_name=file_name
    )

def build_homework_graded_email(
    teacher_name: str,
    subject: str,
    hw_title: str,
    grade: str,
    feedback: str,
    attachment_name: Optional[str] = None
) -> tuple:
    """Returns (subject, html_body, text_body)"""
    email_subject = f"Vazifangiz tekshirildi va baholandi: {hw_title} ({subject})"

    has_attachment_html = ""
    if attachment_name:
        has_attachment_html = f"""
        <div style="margin-top: 16px; padding: 12px 16px; background-color: #eef2ff; border: 1px solid #c7d2fe; border-radius: 12px;">
            <p style="margin: 0; font-size: 13px; color: #3730a3; font-weight: 600;">
                📎 Ustoz taqriz fayli: <span>{attachment_name}</span> (ushbu xatga ilova qilingan)
            </p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>{email_subject}</title>
    </head>
    <body style="margin: 0; padding: 24px; background-color: #f8fafc; font-family: 'Helvetica Neue', Arial, sans-serif; color: #334155;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
        <!-- Header -->
        <tr>
          <td style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); padding: 32px 30px; text-align: left;">
            <span style="background-color: rgba(255,255,255,0.2); color: #ffffff; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px;">BioEdu Baholash</span>
            <h1 style="color: #ffffff; margin: 12px 0 4px 0; font-size: 22px; font-weight: 800;">Vazifangiz Baholandi!</h1>
            <p style="color: #e0e7ff; margin: 0; font-size: 13px;">O'qituvchingiz topshirig'ingizni tekshirib, baho va taqriz qo'ydi</p>
          </td>
        </tr>

        <!-- Content -->
        <tr>
          <td style="padding: 30px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px;">
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">O'qituvchi:</td>
                <td style="padding-bottom: 12px; font-size: 14px; font-weight: 700; color: #0f172a; text-align: right;">{teacher_name}</td>
              </tr>
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">Fan:</td>
                <td style="padding-bottom: 12px; font-size: 14px; font-weight: 700; color: #4f46e5; text-align: right;">{subject}</td>
              </tr>
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">Vazifa:</td>
                <td style="padding-bottom: 12px; font-size: 14px; font-weight: 700; color: #0f172a; text-align: right;">{hw_title}</td>
              </tr>
              <tr>
                <td style="padding-bottom: 12px; font-size: 13px; color: #64748b;">Qo'yilgan Baho / Natija:</td>
                <td style="padding-bottom: 12px; text-align: right;">
                  <span style="display: inline-block; background-color: #10b981; color: #ffffff; font-weight: 800; font-size: 13px; padding: 4px 12px; border-radius: 10px;">
                    {grade or "Baholandi"}
                  </span>
                </td>
              </tr>
            </table>

            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; margin-top: 10px;">
              <p style="margin: 0 0 8px 0; font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.5px;">Ustoz taqrizi va tavsiyalari:</p>
              <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #1e293b; white-space: pre-line;">{feedback or "Izoh qoldirilmadi."}</p>
            </div>

            {has_attachment_html}

            <div style="margin-top: 28px; text-align: center;">
              <a href="/student/homework.html" style="display: inline-block; background-color: #4f46e5; color: #ffffff; text-decoration: none; padding: 13px 32px; border-radius: 12px; font-weight: 700; font-size: 14px;">Kabinetga Kirish</a>
            </div>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background-color: #f1f5f9; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0; font-size: 12px; color: #94a3b8;">
            Ushbu xabar BioEdu ta'lim platformasi orqali avtomatik yuborildi.
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    fb_fallback = feedback if feedback else "Izoh qoldirilmadi."
    att_text = f"Biriktirilgan fayl: {attachment_name} (ushbu xatga ilova qilingan)" if attachment_name else ""

    text = f"""
BioEdu Ta'lim Platformasi — Vazifangiz Baholandi
================================================

Hurmatli o'quvchi!
Ustozingiz {teacher_name} siz topshirgan uyga vazifani tekshirdi.

O'qituvchi: {teacher_name}
Fan: {subject}
Vazifa: {hw_title}
Baho / Natija: {grade or 'Baholandi'}

Ustoz taqrizi va izohi:
{fb_fallback}

{att_text}

Kabinetga kirish: /student/homework.html
    """.strip()

    return email_subject, html, text

# -------------------------------------------------------------
# High-Level Notification Dispatchers
# -------------------------------------------------------------
def notify_students_new_homework(
    students: list,
    teacher_name: str,
    subject: str,
    hw_title: str,
    description: str,
    deadline: str,
    file_url: Optional[str] = None,
    file_name: Optional[str] = None,
    upload_dir: Optional[Path] = None
):
    """
    Finds all valid student emails and sends async notification with attachment.
    """
    to_emails = [s.email.strip() for s in students if getattr(s, "email", None) and "@" in s.email]
    if not to_emails:
        return

    # Resolve local file path if fileUrl is given
    attachment_path = None
    if file_url and upload_dir:
        filename = file_url.replace("/uploads/", "")
        candidate = upload_dir / filename
        if candidate.is_file():
            attachment_path = str(candidate)

    subj, html, text = build_homework_assigned_email(
        teacher_name=teacher_name,
        subject=subject,
        hw_title=hw_title,
        description=description,
        deadline=deadline,
        attachment_name=file_name
    )

    send_email_async(
        to_emails=to_emails,
        subject=subj,
        html_content=html,
        text_content=text,
        attachment_path=attachment_path,
        attachment_name=file_name
    )

def notify_student_homework_graded(
    student,
    teacher_name: str,
    subject: str,
    hw_title: str,
    grade: str,
    feedback: str,
    file_url: Optional[str] = None,
    file_name: Optional[str] = None,
    upload_dir: Optional[Path] = None
):
    """
    Sends async grading review notification to the specific student.
    """
    if not student or not getattr(student, "email", None) or "@" not in student.email:
        return

    to_emails = [student.email.strip()]

    attachment_path = None
    if file_url and upload_dir:
        filename = file_url.replace("/uploads/", "")
        candidate = upload_dir / filename
        if candidate.is_file():
            attachment_path = str(candidate)

    subj, html, text = build_homework_graded_email(
        teacher_name=teacher_name,
        subject=subject,
        hw_title=hw_title,
        grade=grade,
        feedback=feedback,
        attachment_name=file_name
    )

    send_email_async(
        to_emails=to_emails,
        subject=subj,
        html_content=html,
        text_content=text,
        attachment_path=attachment_path,
        attachment_name=file_name
    )
