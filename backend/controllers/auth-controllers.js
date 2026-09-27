const User=require('../models/user.js');
const bcrypt=require('bcryptjs');
const jwt=require('jsonwebtoken');
const sendMail=require('../utils/sendEmail.js');

const registerUser=async(req,res)=>{
      try{
        const {fullName, email, password, agreeToTerms} = req.body;
        const checkExistingUser=await User.findOne({email});
        if(checkExistingUser)
        {
           return res.status(400).json({
            success:false,
            message:'User already exists! Try to register with another email'
           })
        }
        if (!agreeToTerms) {
           return res.status(400).json({
               success: false,
               message: 'You must agree to the Terms of Service and Privacy Policy'
        });
        }
        const salt=await bcrypt.genSalt(10);
        const hashedPass=await bcrypt.hash(password,salt);
        
        const newUser=await User.create({
            fullName,
            email,
            password:hashedPass,
            agreeToTerms,
        });
        
        if(!newUser)
        {
           return res.status(400).json({
            success:false,
            message:'Unable To Register User'
           })
        }

        return res.status(201).json({
            success:true,
            message:'User is registered successfully',
        })
      }catch{
        return res.status(500).json({
            success:false,
            message:'Something went wrong! Please try again',
        })
      }
}

const loginUser = async (req, res) => {
    try {
        const { email, password } = req.body;

        const user = await User.findOne({ email });

        if (!user) {
            return res.status(400).json({
                success: false,
                message: 'Invalid email or password'
            });
        }

        const isPasswordCorrect = await bcrypt.compare(
            password,
            user.password
        );

        if (!isPasswordCorrect) {
            return res.status(400).json({
                success: false,
                message: 'Invalid email or password'
            });
        }
        const accessToken=jwt.sign({
            userId:user._id,
            userName:user.fullName,
            email:user.email,
        },process.env.JWT_SECRET_KEY,{
            expiresIn:'30m'
        })
        return res.status(200).json({
            success: true,
            message: 'Login successful',
            accessToken
        });

    } catch (error) {
        return res.status(500).json({
            success: false,
            message: 'Something went wrong! Please try again'
        });
    }
};
const forgotPassword=async (req,res)=>{
      try{
          const {email} = req.body;
          const user=await User.findOne({email});
          if(!user)
          {
            return res.status(404).json({
                success:false,
                message:'No account found with this email'
            })
          }
          const otp=Math.floor(100000 + Math.random()*900000).toString();
          const otpExpiry = new Date(Date.now() + 5*60*1000);
          user.resetPasswordOTP=otp;
          user.resetPasswordOTPExpiry=otpExpiry;
          user.resetPasswordOTPVerified=false;
          await user.save();
          await sendMail(
            user.email,
            'CodeVue password reset OTP',
            `Your CodeVue password reset OTP is ${otp}. It is valid for 5 minutes.`
          )

          return res.status(201).json({
            success:true,
            message:'OTP sent successfully to your registered mail'
          })
      }catch(e)
      {
          return res.status(500).json({
            success: false,
            message: 'Something went wrong! Please try again'
          });
      }
};
const verifyOTP = async (req, res) => {
    try {
        const { email, otp } = req.body;

        const user = await User.findOne({ email });

        if (!user) {
            return res.status(400).json({
                success: false,
                message: 'User not found'
            });
        }

        if (!user.resetPasswordOTP) {
            return res.status(400).json({
                success: false,
                message: 'No OTP was requested'
            });
        }

        if (user.resetPasswordOTPExpiry < new Date()) {
            return res.status(400).json({
                success: false,
                message: 'OTP has expired'
            });
        }

        if (user.resetPasswordOTP !== otp) {
            return res.status(400).json({
                success: false,
                message: 'Invalid OTP'
            });
        }

        user.resetPasswordOTPVerified = true;

        await user.save();

        return res.status(200).json({
            success: true,
            message: 'OTP verified successfully'
        });

    } catch (error) {
        console.log('Verify OTP error:', error);

        return res.status(500).json({
            success: false,
            message: 'Something went wrong! Please try again'
        });
    }
};
const resetPassword = async (req, res) => {
    try {
        const { email, newPassword } = req.body;

        const user = await User.findOne({ email });

        if (!user) {
            return res.status(400).json({
                success: false,
                message: 'User not found'
            });
        }

        if (!user.resetPasswordOTPVerified) {
            return res.status(400).json({
                success: false,
                message: 'Please verify OTP first'
            });
        }

        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(newPassword, salt);

        user.password = hashedPassword;

        user.resetPasswordOTP = null;
        user.resetPasswordOTPExpiry = null;
        user.resetPasswordOTPVerified = false;

        await user.save();

        return res.status(200).json({
            success: true,
            message: 'Password reset successfully'
        });

    } catch (error) {
        console.log('Reset password error:', error);

        return res.status(500).json({
            success: false,
            message: 'Something went wrong! Please try again'
        });
    }
};
module.exports={
    registerUser,
    loginUser,
    forgotPassword,
    verifyOTP,
    resetPassword,
}