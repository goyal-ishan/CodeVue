const express=require('express');
const router=express.Router();
const authObj=require('../controllers/auth-controllers.js');


router.post('/register', authObj.registerUser);
router.post('/login', authObj.loginUser);

module.exports = router;