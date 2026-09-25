require('dotenv').config();
const express=require('express');
const connectToDB=require('./models/user.js');

connectToDB();

const app=express();
const port=process.env.PORT||8080;


app.listen(port,()=>{
    console.log(`Server is listening on port ${port}`);
})