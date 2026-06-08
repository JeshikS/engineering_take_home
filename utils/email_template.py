def generate_email(company, contact):
    return f"""
    <html>
        <body>
            <p>Hi {contact['first_name']},</p>

            <p>
                I noticed you're working as
                <strong>{contact['position']}</strong>
                at <strong>{company['name']}</strong>.
            </p>

            <p>
                I'd love to connect and learn more about your work.
            </p>

            <p>
                Regards,<br>
                Jeshik
            </p>
        </body>
    </html>
    """