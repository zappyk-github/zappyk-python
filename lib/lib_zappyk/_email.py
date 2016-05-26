# -*- coding: utf-8 -*-
__author__ = 'zappyk'

import os, sys, html

from smtplib                import SMTP
from email                  import encoders
from email.mime.base        import MIMEBase
from email.mime.text        import MIMEText
from email.mime.multipart   import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils            import COMMASPACE, formatdate

###############################################################################
mail_Verbose = True
mail_DebugOn = False

mail__smtp__ = 'Xsmtp.gmail.com:587'
mailStartTLS = True
mailAuthUser = 'sysop@payroll.it'
mailAuthPswd = 's3rv1c3s'
mail__from__ =  mailAuthUser
mail___to___ = [mailAuthUser]
mail___cc___ = []
mail___ccn__ = []
mail_attachs = []
mail_subject = "<oggetto>"
mail_message = "<messaggio>"

mail_html_body_send   = True
mail_html_body_escape = True
mail_html_font_size   = '2' # (1|2|3|0=None)
mail_html_body_face   = "arial,helvetica,sans-serif"
mail_html_body_style  = "font-family: courier new,monospace;"
mail_html_body_layout = """\
<html>
<head></head>
<body><font face="%s" style="%s" size="%s">
<pre>
%s
</pre>
</font>
</body>
</html>\
"""

###############################################################################
class _email(object):
#CZ#def __init__(self, SystemId = None):
#CZ#    self.mailSystemId = SystemId
    ###########################################################################
    def __init__(self):
        assert type(mail___to___) == list
        assert type(mail___cc___) == list
        assert type(mail___ccn__) == list
        assert type(mail_attachs) == list

        self.mail_Verbose = mail_Verbose
        self.mail_DebugOn = mail_DebugOn

        self.mail__smtp__ = mail__smtp__
        self.mailStartTLS = mailStartTLS
        self.mailAuthUser = mailAuthUser
        self.mailAuthPswd = mailAuthPswd
        self.mail__from__ = mail__from__
        self.mail___to___ = mail___to___
        self.mail___cc___ = mail___cc___
        self.mail___ccn__ = mail___ccn__
        self.mail_attachs = mail_attachs
        self.mail_subject = mail_subject
        self.mail_message = mail_message

        self.mail_html_body_send   = mail_html_body_send
        self.mail_html_body_escape = mail_html_body_escape
        self.mail_html_font_size   = mail_html_font_size
        self.mail_html_body_face   = mail_html_body_face
        self.mail_html_body_style  = mail_html_body_style
        self.mail_html_body_layout = mail_html_body_layout
    ###########################################################################
    def _verbose(self, mail_Verbose):
        self.mail_Verbose = mail_Verbose
    ###########################################################################
    def _debug(self, mail_DebugOn):
        self.mail_DebugOn = mail_DebugOn

    ###########################################################################
    def _send(self):
        # Create message container - the correct MIME type is multipart/alternative.
        _header = MIMEMultipart('alternative')

        _header['Subject']  =                 self.mail_subject
        _header['From']     =                 self.mail__from__
        _header['Reply-to'] =                 self.mail__from__
        _header['To']       = COMMASPACE.join(self.mail___to___)
        _header['Cc']       = COMMASPACE.join(self.mail___cc___)
        _header['Ccn']      = COMMASPACE.join(self.mail___ccn__)
        _header['Date']     = formatdate(localtime=True)

        # Create the body of the message (a plain-text and an HTML version).
        _text = self.mail_message
        _hscp = _text
        if self.mail_html_body_escape:
            _hscp = html.escape(_text)
        #CZ#_hscp = html.escape(_text.replace('\r', '').replace('\n', '<br>\n'))
        _html = self.mail_html_body_layout % (self.mail_html_body_face,
                                              self.mail_html_body_style,
                                              self.mail_html_font_size,
                                              _hscp)

        # Record the MIME types of both parts - text/plain and text/html.
        _text_content = MIMEText(_text, 'plain')
        _html_content = MIMEText(_html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        _header.attach(_text_content)
        if self.mail_html_body_send:
            _header.attach(_html_content)

        # Attach files into message container.
        for mail_attach in self.mail_attachs:
            name_attach = os.path.basename(mail_attach)

            # This is the octet-stream part(The Attachment):
            _file_content = MIMEBase('application', 'octet-stream')
            _file_content.set_payload(open(mail_attach, 'rb').read())
            encoders.encode_base64(_file_content)
            _file_content.add_header('Content-Disposition', 'attachment; filename="%s"' % name_attach)
            _header.attach(_file_content)

            # This is the binary part(The Attachment):
        #CZ#_file_content = MIMEApplication(open(mail_attach, 'rb').read())
        #CZ#_file_content.add_header('Content-Disposition', 'attachment; filename="%s"' % name_attach)
        #CZ#_header.attach(_file_content)

        try:
            # The actual mail send
            if self.mail_DebugOn:
                print("* Send mail on %s:" % self.mail__smtp__)
            else:
                if self.mail_Verbose:
                    print("Send mail on %s ..." % self.mail__smtp__, end='', flush=True)
            #CZ#sys.stdout.flush()
            server = SMTP(self.mail__smtp__)

            if self.mailStartTLS:
                if self.mail_DebugOn:
                    print("* ...startTLS...")
                server.starttls()

            if self.mailAuthUser is not None:
                if self.mail_DebugOn:
                    print("* ...login...")
                server.login(self.mailAuthUser, self.mailAuthPswd)

            if self.mail_DebugOn:
                print("* ...sendmail to %s ..." % self.mail___to___)
            else:
                if self.mail_Verbose:
                    print("from %s to %s ..." % (self.mail__from__, self.mail___to___), end='', flush=True)
            #CZ#sys.stdout.flush()
            server.sendmail(self.mail__from__, self.mail___to___, _header.as_string())

            if self.mail_DebugOn:
                print("* ...quit...")
            server.quit()

            if self.mail_DebugOn:
                print("* Send done!")
            else:
                if self.mail_Verbose:
                    print("done!", flush=True)
            #CZ#sys.stdout.flush()
        except:
            if self.mail_DebugOn:
                print('', end='')
            else:
                if self.mail_Verbose:
                    print('')
            raise(Exception(sys.exc_info()))
    ###########################################################################
    def _setMailSmtp(self, mail__smtp__):
        self.mail__smtp__ = mail__smtp__
    #--------------------------------------------------------------------------
    def _getMailSmtp(self):
        return(self.mail__smtp__)
    ###########################################################################
    def _setMailFrom(self, mail__from__):
        self.mail__from__ = mail__from__
    #--------------------------------------------------------------------------
    def _getMailFrom(self):
        return(self.mail__from__)
    ###########################################################################
    def _setMailTo(self, mail___to___):
        self.mail___to___ = mail___to___
    #--------------------------------------------------------------------------
    def _getMailTo(self):
        return(self.mail___to___)
    ###########################################################################
    def _setMailCc(self, mail___cc___):
        self.mail___cc___ = mail___cc___
    #--------------------------------------------------------------------------
    def _getMailCc(self):
        return(self.mail___cc___)
    ###########################################################################
    def _setMailCcn(self, mail___ccn__):
        self.mail___ccn__ = mail___ccn__
    #--------------------------------------------------------------------------
    def _getMailCcn(self):
        return(self.mail___ccn__)
    ###########################################################################
    def _setMailAttachs(self, mail_attachs):
        self.mail_attachs = mail_attachs
    #--------------------------------------------------------------------------
    def _getMailAttachs(self):
        return(self.mail_attachs)
    ###########################################################################
    def _setMailSubject(self, mail_subject):
        self.mail_subject = mail_subject
    #--------------------------------------------------------------------------
    def _getMailSubject(self):
        return(self.mail_subject)
    ###########################################################################
    def _setMailMessage(self, mail_message):
        self.mail_message = mail_message
    #--------------------------------------------------------------------------
    def _getMailMessage(self):
        return(self.mail_message)
    ###########################################################################
    def _setMailHtmlBodySend(self, mail_html_body_send):
        self.mail_html_body_send = mail_html_body_send
    #--------------------------------------------------------------------------
    def _getMailHtmlBodySend(self):
        return(self.mail_html_body_send)
    ###########################################################################
    def _setMailHtmlBodyEscape(self, mail_html_body_escape):
        self.mail_html_body_escape = mail_html_body_escape
    #--------------------------------------------------------------------------
    def _getMailHtmlBodyEscape(self):
        return(self.mail_html_body_escape)
    ###########################################################################
    def _setMailHtmlFontSize(self, mail_html_font_size):
        self.mail_html_font_size = mail_html_font_size
    #--------------------------------------------------------------------------
    def _getMailHtmlFontSize(self):
        return(self.mail_html_font_size)
    ###########################################################################
    def _setMailHtmlBodyFace(self, mail_html_body_face):
        self.mail_html_body_face = mail_html_body_face
    #--------------------------------------------------------------------------
    def _getMailHtmlBodyFace(self):
        return(self.mail_html_body_face)
    ###########################################################################
    def _setMailHtmlBodyStyle(self, mail_html_body_style):
        self.mail_html_body_style = mail_html_body_style
    #--------------------------------------------------------------------------
    def _getMailHtmlBodyStyle(self):
        return(self.mail_html_body_style)
    ###########################################################################
    def _setMailHtmlFontLayout(self, mail_html_font_layout):
        self.mail_html_font_layoutt = mail_html_font_layout
    #--------------------------------------------------------------------------
    def _getMailHtmlFontLayout(self):
        return(self.mail_html_font_layout)
    ###########################################################################
    def _setMailStartTLS(self, mailStartTLS):
        self.mailStartTLS = mailStartTLS
    ###########################################################################
    def _setMailAuthUser(self, mailAuthUser):
        self.mailAuthUser = mailAuthUser
    ###########################################################################
    def _setMailAuthPswd(self, mailAuthPswd):
        self.mailAuthPswd = mailAuthPswd