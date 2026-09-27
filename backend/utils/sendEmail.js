const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.CODEVUEMAIL,
        pass: process.env.CODEVUEPASS
    }
});

const sendEmail = async (to, subject, text) => {
    await transporter.sendMail({
        from: process.env.CODEVUEMAIL,
        to: to,
        subject: subject,
        text: text
    });
};

module.exports = sendEmail;