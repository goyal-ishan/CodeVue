const User=require('../models/user.js');
const bcrypt=require('bcryptjs');
const jwt=require('jsonwebtoken');


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

        return res.status(200).json({
            success: true,
            message: 'Login successful'
        });

    } catch (error) {
        return res.status(500).json({
            success: false,
            message: 'Something went wrong! Please try again'
        });
    }
};

module.exports={
    registerUser,
    loginUser,
}