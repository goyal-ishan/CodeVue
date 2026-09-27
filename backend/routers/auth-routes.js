const express=require('express');
const router=express.Router();
const authObj=require('../controllers/auth-controllers.js');

router.post('/register', authObj.registerUser);
router.post('/login', authObj.loginUser);
router.post('/forgot-password', authObj.forgotPassword);
router.post('/verify-otp', authObj.verifyOTP);
router.post('/reset-pass', authObj.resetPassword);
module.exports = router;